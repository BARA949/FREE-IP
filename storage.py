import json
import os
from typing import List, Dict, Any


def load_visits(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_visits(path: str, visits: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(visits, f, ensure_ascii=False, indent=2)
