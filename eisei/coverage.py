import json, glob, os, sys
root = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/drill/eisei"
T = json.load(open(f"{root}/topics.json"))["topics"]
qs = []
for f in [f"{root}/m01.json", f"{root}/m02.json"] + sorted(glob.glob(f"{root}/bank/*.json")):
    if f.endswith("index.json"):
        continue
    d = json.load(open(f))
    qs += d["questions"]
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
