import json, math

def jsnum(x):
    return int(x) if isinstance(x, float) and x == int(x) else x
def plural(n, word, form=None): return str(jsnum(n)) + " " + (word if n == 1 else (form or word + "s"))
def fmt(x): return str(jsnum(x))
def round1(x): return jsnum(math.floor(x * 10 + 0.5) / 10)

def slab_plan(runCm, slabCm):
    if not (runCm > 0) or not (slabCm > 0):
        return {"error": "the run and the labeled slab must be positive"}
    slabs = math.ceil(runCm / slabCm)
    seams = slabs - 1
    leftover = round1(slabs * slabCm - runCm)
    if slabs == 1: verdict = "a seamless run"
    elif slabs == 2: verdict = "a one-seam run"
    else: verdict = "a multi-seam run"
    return {"slabs": slabs, "seams": seams, "leftover": leftover, "verdict": verdict}

def overhang_plan(overhangCm, runCm):
    if not (overhangCm > 0) or not (runCm > 0):
        return {"error": "the overhang and the run must be positive"}
    if overhangCm <= 15: supports, verdict = 0, "a free span"
    elif overhangCm <= 30: supports, verdict = math.ceil(runCm / 60) - 1, "a bracket job"
    else: supports, verdict = max(2, math.ceil(runCm / 120)), "a post job"
    return {"supports": supports, "verdict": verdict}

def cutout_plan(sinkCm, counterCm):
    if not (sinkCm > 0) or not (counterCm > 0):
        return {"error": "the sink and the counter must be positive"}
    if sinkCm >= counterCm:
        return {"error": "the sink is wider than the counter"}
    margin = round1((counterCm - sinkCm) / 2)
    if margin < 10: verdict = "tight ends"
    elif margin <= 30: verdict = "working ends"
    else: verdict = "generous ends"
    return {"margin": margin, "verdict": verdict}

def render_slab(r, runCm, slabCm):
    return ("A run " + fmt(runCm) + " cm on labeled " + fmt(slabCm) + " cm slabs takes " + plural(r["slabs"], "slab")
            + " with " + plural(r["seams"], "seam") + " and " + fmt(r["leftover"]) + " cm of slab left over - " + r["verdict"] + ".")

def render_overhang(r, overhangCm, runCm):
    if r["supports"] == 0:
        return ("An overhang " + fmt(overhangCm) + " cm on a " + fmt(runCm) + " cm run is a free span - no supports asked.")
    if r["verdict"] == "a bracket job":
        return ("An overhang " + fmt(overhangCm) + " cm on a " + fmt(runCm) + " cm run takes " + plural(r["supports"], "bracket")
                + " at the labeled 60 cm spacing - a bracket job.")
    return ("An overhang " + fmt(overhangCm) + " cm on a " + fmt(runCm) + " cm run takes " + plural(r["supports"], "post")
            + " at the labeled 120 cm spacing - a post job.")

def render_cutout(r, sinkCm, counterCm):
    return ("A sink " + fmt(sinkCm) + " cm in a " + fmt(counterCm) + " cm counter leaves " + fmt(r["margin"])
            + " cm at each end - " + r["verdict"] + ".")

cases = []
def add(fn, f, rf, args):
    r = f(*args)
    c = {"fn": fn, "args": args, "result": r}
    if "error" not in r: c["render"] = rf(r, *args)
    cases.append(c)

for a in [[300,250],[250,250],[0,250],[300,0],[240,250],[600,250],[125,250],[301.5,250],[500,250],[1000,300]]:
    add("slabPlan", slab_plan, render_slab, a)
for a in [[20,240],[10,240],[0,240],[20,0],[40,300],[15,240],[16,120],[30,240],[31,240],[25,180]]:
    add("overhangPlan", overhang_plan, render_overhang, a)
for a in [[50,120],[0,120],[50,0],[130,120],[120,120],[100,120],[60,120],[76.5,120],[40,60],[55,120]]:
    add("cutoutPlan", cutout_plan, render_cutout, a)
json.dump(cases, open("expected.json", "w"), separators=(",", ":"))
print(len(cases), "cases")
