import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

input_path = (
    ROOT / "results" / "raw" / "qwen3_4b_explicit_v0.jsonl"
)

output_path = (
    ROOT / "results" / "annotations" / "qwen3_4b_explicit_v0_human.jsonl"
)

output_path.parent.mkdir(parents=True, exist_ok=True)

label_map = {
    "p": "PROCEED",
    "d": "DO_NOT_PROCEED",
    "n": "NEED_MORE_INFORMATION",
    "a": "AMBIGUOUS"
}

records = []

with open(input_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        records.append(json.loads(line))


annotations = []

for i, record in enumerate(records, start=1):

    print("\n" + "=" * 80)
    print(f"Response {i}/{len(records)}")
    print("=" * 80)
    print()
    print(record["raw_response"])
    print()

    while True:
        choice = input(
            "[p]roceed / [d]o not proceed / "
            "[n]eed more information / [a]mbiguous: "
        ).strip().lower()

        if choice in label_map:
            break

        print("Invalid label. Try again.")

    note = input("Optional note: ").strip()

    annotation = {
        "prompt_id": record["prompt_id"],
        "behavior_label": label_map[choice],
        "annotator": "human_1",
        "rubric_version": "v0.1",
        "annotation_note": note
    }

    annotations.append(annotation)


with open(output_path, "w", encoding="utf-8") as f:
    for annotation in annotations:
        f.write(
            json.dumps(annotation, ensure_ascii=False) + "\n"
        )


print()
print(f"Saved {len(annotations)} annotations to:")
print(output_path)