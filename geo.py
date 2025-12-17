import requests


def geo_lookup(ip: str, api_base_url: str) -> dict | None:
    """Lookup geo info for an IP using a GeoIP HTTP API.

    api_base_url example: "http://ip-api.com/json"
    Returns dict with at least: country, regionName, city, query (IP) or None.
    """
    try:
        url = f"{api_base_url.rstrip('/')}/{ip}?fields=status,country,regionName,city,lat,lon,isp,query"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if data.get("status") == "success":
            return data
    except Exception:
        pass
    return None
