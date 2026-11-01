"""Add a Risk Radar snapshot to the public site.
Usage: python3 tools/add_snapshot.py path/to/snapshot.json
Removes private fields, writes data/snapshots/<date>.json and updates data/manifest.json."""
import json, sys, os
PRIVATE = {"flocean"}          # fields never published
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def strip(x):
    if isinstance(x, dict): return {k: strip(v) for k, v in x.items() if k not in PRIVATE}
    if isinstance(x, list): return [strip(v) for v in x]
    return x
snap = strip(json.load(open(sys.argv[1], encoding="utf-8")))
date = snap["date"]; assert len(date) == 10
out = os.path.join(ROOT, "data", "snapshots", date + ".json")
json.dump(snap, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
mp = os.path.join(ROOT, "data", "manifest.json")
m = json.load(open(mp)) if os.path.exists(mp) else {"snapshots": []}
m["snapshots"] = sorted(set(m["snapshots"]) | {date})
m["latest"] = m["snapshots"][-1]
json.dump(m, open(mp, "w"), indent=1)
print("added", date, "->", len(m["snapshots"]), "snapshots")
