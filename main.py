import yaml

from tracker import create_app


def load_config(path: str = "config.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main() -> None:
    config = load_config()
    app = create_app(config)

    host = config["server"].get("host", "0.0.0.0")
    port = int(config["server"].get("port", 5000))
    debug = bool(config["server"].get("debug", True))

    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    main()
