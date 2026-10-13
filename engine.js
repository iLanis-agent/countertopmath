(function (root) {
  "use strict";
  function plural(n, word, form) { return n + " " + (n === 1 ? word : (form || word + "s")); }
  function round1(x) { return Math.round(x * 10) / 10; }

  function slabPlan(runCm, slabCm) {
    if (!(runCm > 0) || !(slabCm > 0)) return { error: "the run and the labeled slab must be positive" };
    var slabs = Math.ceil(runCm / slabCm);
    var seams = slabs - 1;
    var leftover = round1(slabs * slabCm - runCm);
    var verdict;
    if (slabs === 1) verdict = "a seamless run";
    else if (slabs === 2) verdict = "a one-seam run";
    else verdict = "a multi-seam run";
    return { slabs: slabs, seams: seams, leftover: leftover, verdict: verdict };
  }

  function overhangPlan(overhangCm, runCm) {
    if (!(overhangCm > 0) || !(runCm > 0)) return { error: "the overhang and the run must be positive" };
    var supports, verdict;
    if (overhangCm <= 15) { supports = 0; verdict = "a free span"; }
    else if (overhangCm <= 30) { supports = Math.ceil(runCm / 60) - 1; verdict = "a bracket job"; }
    else { supports = Math.max(2, Math.ceil(runCm / 120)); verdict = "a post job"; }
    return { supports: supports, verdict: verdict };
  }

  function cutoutPlan(sinkCm, counterCm) {
    if (!(sinkCm > 0) || !(counterCm > 0)) return { error: "the sink and the counter must be positive" };
    if (sinkCm >= counterCm) return { error: "the sink is wider than the counter" };
    var margin = round1((counterCm - sinkCm) / 2);
    var verdict;
    if (margin < 10) verdict = "tight ends";
    else if (margin <= 30) verdict = "working ends";
    else verdict = "generous ends";
    return { margin: margin, verdict: verdict };
  }

  function renderSlab(r, runCm, slabCm) {
    return "A run " + runCm + " cm on labeled " + slabCm + " cm slabs takes " + plural(r.slabs, "slab") + " with " + plural(r.seams, "seam") + " and " + r.leftover + " cm of slab left over - " + r.verdict + ".";
  }

  function renderOverhang(r, overhangCm, runCm) {
    if (r.supports === 0) return "An overhang " + overhangCm + " cm on a " + runCm + " cm run is a free span - no supports asked.";
    if (r.verdict === "a bracket job") return "An overhang " + overhangCm + " cm on a " + runCm + " cm run takes " + plural(r.supports, "bracket") + " at the labeled 60 cm spacing - a bracket job.";
    return "An overhang " + overhangCm + " cm on a " + runCm + " cm run takes " + plural(r.supports, "post") + " at the labeled 120 cm spacing - a post job.";
  }

  function renderCutout(r, sinkCm, counterCm) {
    return "A sink " + sinkCm + " cm in a " + counterCm + " cm counter leaves " + r.margin + " cm at each end - " + r.verdict + ".";
  }

  var api = { slabPlan: slabPlan, overhangPlan: overhangPlan, cutoutPlan: cutoutPlan, renderSlab: renderSlab, renderOverhang: renderOverhang, renderCutout: renderCutout };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.CountertopMath = api;
})(this);
