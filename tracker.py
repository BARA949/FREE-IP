from datetime import datetime, timezone
from typing import Any, Dict

from flask import Flask, jsonify, redirect, render_template, request

from geo import geo_lookup
from storage import load_visits, save_visits


def create_app(config: Dict[str, Any]) -> Flask:
    app = Flask(__name__)

    visits_path = config["storage"]["visits_path"]
    ip_api = config["tracking"]["ip_info_api"]
    default_target = config["tracking"]["default_target_url"]

    @app.route("/t/<token>")
    def track_click(token: str):
        """Tracking endpoint.

        - Reads visitor IP
        - Looks up geo info
        - Appends record to visits storage
        - Redirects user to a real target URL
        """
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip and "," in ip:
            ip = ip.split(",")[0].strip()

        geo = geo_lookup(ip, ip_api) or {}

        record = {
            "time": datetime.now(timezone.utc).isoformat(),
            "ip": ip,
            "country": geo.get("country"),
            "region": geo.get("regionName"),
            "city": geo.get("city"),
            "lat": geo.get("lat"),
            "lon": geo.get("lon"),
            "isp": geo.get("isp"),
            "token": token,
            "user_agent": request.headers.get("User-Agent"),
        }

        visits = load_visits(visits_path)
        visits.append(record)
        save_visits(visits_path, visits)

        target_url = request.args.get("next") or default_target
        return redirect(target_url)

    @app.route("/visits", methods=["GET"])
    def list_visits():
        """Simple API to see stored visits (for testing)."""
        return jsonify(load_visits(visits_path))

    @app.route("/dashboard", methods=["GET"])
    def dashboard():
        """HTML dashboard showing visits in a table."""
        visits = load_visits(visits_path)
        return render_template("dashboard.html", visits=visits)

    return app
