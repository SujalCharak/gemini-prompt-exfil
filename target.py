# target.py
from typing import List, Dict
import importlib, pathlib, yaml

CFG = yaml.safe_load(open(pathlib.Path(__file__).with_name("aix.yaml")))

def respond(history: List[Dict]) -> str:
    name = CFG["provider"]["name"]
    mod = importlib.import_module(f"providers.{name}")
    return mod.respond(history, CFG)