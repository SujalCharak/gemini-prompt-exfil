"""
Research-only scenario runner.

Used for controlled evaluation under owned accounts.
Not an exploit. Not for third-party systems.
"""


#!/usr/bin/env python3
# Simple safe attacker harness (placeholder payload)
import os
import json
import uuid
import argparse
import datetime
import csv
import requests

API_ENDPOINT = os.environ.get("MODEL_API_ENDPOINT", "https://api.vendor.example/v1/generate")
API_KEY = os.environ.get("MODEL_API_KEY", "")
MODEL_NAME = os.environ.get("MODEL_NAME", "model-name-placeholder")

OUT_DIR = "trials"
os.makedirs(OUT_DIR, exist_ok=True)

def make_payload_gemini():
    # Gemini (AI Studio) expects 'contents' with user text parts
    user_text = "USER_INPUT_PLACEHOLDER — replace locally if needed"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_text}]
            }
        ],
        "generationConfig": {
            "temperature": float(os.environ.get("AIXT_TEMP","0.2")),
            "maxOutputTokens": 256
        }
    }
    return payload

def make_payload():

    # Replace the "input" value locally if you later choose to run a test against your owned accounts.
    if 'generativelanguage.googleapis.com' in os.environ.get('MODEL_API_ENDPOINT',''):
        return make_payload_gemini()
    payload = {
        "model": MODEL_NAME,
        "input": "USER_INPUT_PLACEHOLDER — replace locally if needed",
        "temperature": float(os.environ.get("AIXT_TEMP","0.2")),
        "max_tokens": 256
    }
    return payload

def send_request(payload):
    headers = {
        "Authorization": f"Bearer {API_KEY}" if API_KEY else "Bearer <MISSING>",
        "Content-Type": "application/json"
    }
    # Generic POST; replace with vendor SDK if needed.
    resp = requests.post(API_ENDPOINT, headers=headers, json=payload, timeout=60)
    provider_req_id = resp.headers.get("x-request-id") or resp.headers.get("request-id") or ""
    return resp.status_code, resp.text, provider_req_id

def save_json(path, obj):
    with open(path, "w") as f:
        json.dump(obj, f, indent=2)

def append_csv_row(csv_path, row):
    header = ["trial_id","timestamp","model","temperature","max_tokens","system_prompt_present","ocr_used","attacker_output_contains_secret","secret_sha256_match","local_request_id","provider_request_id","notes"]
    exists = os.path.exists(csv_path)
    with open(csv_path, "a", newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(header)
        writer.writerow(row)

def main(trial):
    ts = datetime.datetime.utcnow().isoformat() + "Z"
    trial_id = f"trial-{int(trial):03d}-{uuid.uuid4().hex[:8]}"
    payload = make_payload()

    # Save request BEFORE sending
    req_path = os.path.join(OUT_DIR, f"attacker_request_{trial_id}.json")
    save_json(req_path, {"timestamp": ts, "payload": payload})

    # Send
    status, resp_text, provider_req_id = send_request(payload)

    # Save response
    resp_path = os.path.join(OUT_DIR, f"attacker_response_{trial_id}.json")
    try:
        resp_obj = json.loads(resp_text)
    except Exception:
        resp_obj = {"raw_text": resp_text}
    # capture provider-returned headers (if any) for triage
    provider_headers = {}
    try:
        # resp variable exists in the outer scope returned by send_request; if not, keep empty
        provider_headers = getattr(globals().get('resp', None), 'headers', {}) or {}
    except Exception:
        provider_headers = {}
    save_json(resp_path, {"timestamp": ts, "status": status, "response": resp_obj, "provider_headers": dict(provider_headers)})

    # Save meta
    meta = {
        "trial_id": trial_id,
        "timestamp": ts,
        "model": payload.get("model"),
        "temperature": payload.get("temperature"),
        "max_tokens": payload.get("max_tokens"),
        "system_prompt_present": os.environ.get("AIXT_SYS","unknown"),
        "ocr_used": os.environ.get("AIXT_OCR","unknown"),
        "local_request_id": os.path.basename(req_path),
        "provider_request_id": provider_req_id,
        "provider_headers": dict(provider_headers) if isinstance(provider_headers, dict) else {}
    }
    meta_path = os.path.join(OUT_DIR, f"trial_meta_{trial_id}.json")
    save_json(meta_path, meta)

    # Append CSV row (attacker_output and sha fields left blank for manual review)
    csv_row = [trial_id, ts, meta["model"], meta["temperature"], meta["max_tokens"], meta["system_prompt_present"], meta["ocr_used"], "", "", meta["local_request_id"], meta["provider_request_id"], ""]
    append_csv_row("repro_trials_summary.csv", csv_row)

    print("Saved request:", req_path)
    print("Saved response:", resp_path)
    print("Saved meta:", meta_path)
    print("Appended row to repro_trials_summary.csv")
    print("Trial complete:", trial_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial", type=int, default=1)
    args = parser.parse_args()
    main(args.trial)
