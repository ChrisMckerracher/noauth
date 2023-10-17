import json
from typing import Any, Dict


def load_and_modify(path: str, replacement_vals: Dict[str, Any] | None = None):
    with open(path, "r") as file:
        data = json.load(file)
        data.update(replacement_vals) if replacement_vals else None
    return data
