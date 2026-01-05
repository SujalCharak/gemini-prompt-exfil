#!/usr/bin/env python3
import os, json, argparse, csv, glob

def load_secret(path):
    with open(path,'r') as f:
        return f.read().strip()

def find_matches(secret, trials_dir="trials"):
    results = []
    files = sorted(glob.glob(os.path.join(trials_dir, "attacker_response_*.json")))
    for f in files:
        with open(f,'r') as fh:
            data = fh.read()
        matched = secret in data
        snippet = ""
        if matched:
            i = data.find(secret)
            start = max(0, i-60)
            end = min(len(data), i+len(secret)+60)
            snippet = data[start:end].replace("\n","\\n")
        trial_id = os.path.basename(f).replace("attacker_response_","").replace(".json","")
        results.append((trial_id, "yes" if matched else "no", snippet))
    return results

def write_csv(results, out="matches.csv"):
    with open(out,'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["trial_id","matched","snippet"])
        for r in results:
            writer.writerow(r)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token-file", required=True, help="path to local secret token file (do not share)")
    parser.add_argument("--trials-dir", default="trials")
    args = parser.parse_args()
    secret = load_secret(args.token_file)
    results = find_matches(secret, args.trials_dir)
    write_csv(results)
    for r in results:
        print(r[0], r[1])
    print("Wrote matches.csv (local). If any rows show 'yes', inspect matches.csv for snippet details.")
