import json
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM

MODEL_NAME = "Qwen/Qwen3-4B"
MAX_NEW_TOKENS = 1024

ROOT = Path(__file__).resolve().parent.parent

prompt_path = (
    ROOT / "data" / "pilot" / "auth_prompts_explicit_v0.jsonl"
)

output_path = (
    ROOT / "results" / "raw" / "qwen3_4b_explicit_v0.jsonl"
)

output_path.parent.mkdir(parents=True, exist_ok=True)


# -------------------------
# Load prompts
# -------------------------

prompt_records = []

with open(prompt_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        prompt_records.append(json.loads(line))


# -------------------------
# Load model
# -------------------------

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.bfloat16,
    device_map="auto"
)

model.eval()


# -------------------------
# Run experiment
# -------------------------

with open(output_path, "w", encoding="utf-8") as out_f:

    for i, record in enumerate(prompt_records, start=1):

        prompt = record["prompt_text"]

        messages = [
            {"role": "user", "content": prompt}
        ]

        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
            enable_thinking=False
        ).to(model.device)

        input_token_count = inputs["input_ids"].shape[-1]

        with torch.inference_mode():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False
            )

        generated_ids = output_ids[0][input_token_count:]

        output_token_count = len(generated_ids)

        response = tokenizer.decode(
            generated_ids,
            skip_special_tokens=True
        )

        result = {
            **record,

            "model": MODEL_NAME,
            "dtype": "bfloat16",
            "thinking": False,
            "do_sample": False,
            "max_new_tokens": MAX_NEW_TOKENS,

            "input_token_count": input_token_count,
            "output_token_count": output_token_count,
            "hit_max_new_tokens": (
                output_token_count >= MAX_NEW_TOKENS
            ),

            "raw_response": response
        }

        out_f.write(
            json.dumps(result, ensure_ascii=False) + "\n"
        )

        out_f.flush()

        print(
            f"[{i}/{len(prompt_records)}] "
            f"{record['prompt_id']} | "
            f"in={input_token_count} "
            f"out={output_token_count} "
            f"maxed={result['hit_max_new_tokens']}"
        )


print()
print(f"Saved results to:")
print(output_path)