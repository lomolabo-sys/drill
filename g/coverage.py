import json, glob, sys
root = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/drill/g"
T = json.load(open(f"{root}/topics.json", encoding="utf-8"))["topics"]
sets = json.load(open(f"{root}/sets.json", encoding="utf-8"))["sets"]
files = [f"{root}/{s['file']}" for s in sets] + sorted(glob.glob(f"{root}/bank/*.json"))
qs = []
for f in files:
    if f.endswith("index.json"):
        continue
    qs += json.load(open(f, encoding="utf-8"))["questions"]
cnt = {}
for t in T:
    n = 0
    for q in qs:
        if q["r"] != t["r"]:
            continue
        text = q["q"] + "".join(q["c"])
        if any(k in text for k in t["kw"]):
            n += 1
    cnt[t["t"]] = n
print("total", len(qs))
for t in sorted(T, key=lambda t: (t["r"], cnt[t["t"]])):
    print(t["r"], f"{cnt[t['t']]:4d}", t["t"])
miss = [q["q"][:40] for q in qs if not any(q["r"] == t["r"] and any(k in q["q"] + "".join(q["c"]) for k in t["kw"]) for t in T)]
if miss:
    print("\nどの論点にも当たらない問題:")
    for m in miss:
        print(" -", m)
