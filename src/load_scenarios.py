import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
path = ROOT / "data" / "pilot" / "auth_scenarios_v0.jsonl"

scenarios = []
with open(path, "r") as f:
    for line_number, line in enumerate(f, start=1):
        line = line.strip()

        if not line:
            continue

        try:
            scenario = json.loads(line)
        except json.JSONDecodeError:
            print(f"Invalid JSON on line {line_number}:")
            print(line)
            raise
        scenarios.append(scenario)

print(len(scenarios))
print(scenarios[0])
        