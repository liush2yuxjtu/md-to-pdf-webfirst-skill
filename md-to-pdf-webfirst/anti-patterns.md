# McKinsey-Style PDF Anti-Patterns

Use this file as a consulting mentor review checklist before declaring a McKinsey-style PDF complete. The goal is McKinsey-inspired executive clarity, not visual imitation or branded cloning.

## Mentor Review From The Guizhou Yangfan PDF

The reviewed PDF was directionally stronger than a raw HTML printout: it added a clean cover, executive summary, issue map, section map, exhibit labels, and compact A4 tables. However, as a consulting intern deliverable, it still showed several classic anti-patterns that should be corrected in future runs.

## Anti-Patterns And Corrections

### 1. Styling Before Storyline

**Symptom:** The cover and page system look consulting-like, but the document can still read as a formatted report instead of a persuasive executive argument.

**Why it matters:** In consulting, polish supports the answer. It does not substitute for the answer.

**Correction:** Build the storyline first:

1. One-sentence answer.
2. Three supporting reasons.
3. Quantified business impact.
4. Recommended actions with owners and timing.
5. Evidence exhibits.

### 2. Summary Cards That Repeat Inputs Instead Of Making Decisions

**Symptom:** KPI cards show metrics such as IYA, YoY, and problem categories, but do not always translate them into a decision or management implication.

**Why it matters:** Executives need "so what" and "now what", not only "what".

**Correction:** Every summary metric should have an implication nearby:

- Metric: `RD IYA = 0.9689`
- So what: `overall business is below threshold`
- Now what: `prioritize recovery in Fabric / Hair / Oral and focus on the worst Hub-store execution breaks`

### 3. Weak Exhibit Takeaways

**Symptom:** Tables are labeled as exhibits, but some exhibits do not have a short `KEY TAKEAWAY` or `IMPLICATION` sentence.

**Why it matters:** A partner should not need to interpret the table from scratch.

**Correction:** Every major exhibit needs one sentence above or below it:

```text
KEY TAKEAWAY: Fabric, Hair, and Oral explain the negative YoY gap; recovery should start with the hubs contributing the largest absolute gap.
```

### 4. Decorative McKinsey Imitation

**Symptom:** A red bar, clean typography, and sparse cover make the page feel consulting-like, but the same visual treatment repeated everywhere can become cosmetic.

**Why it matters:** A consulting style is a reasoning style first. Layout should signal hierarchy, not decoration.

**Correction:** Use red only for section structure, risk, and priority. Avoid using it as generic ornament. Prefer thin gray rules, strong headlines, and disciplined whitespace.

### 5. Raw Report Flow Carried Into The PDF

**Symptom:** Source report sections are preserved in order, even when the executive answer would benefit from regrouping.

**Why it matters:** Source fidelity is important, but client-ready consulting output usually reorganizes evidence around the decision.

**Correction:** Preserve source content, but add a decision-oriented front matter:

- Executive answer.
- Issue tree.
- Priority actions.
- Evidence sections.
- Appendix / source trace.

### 6. Data Extraction Trust Failure

**Symptom:** A first pass accidentally placed health-status labels in metric cards instead of numeric values.

**Why it matters:** One wrong number on an executive page damages trust in the whole document.

**Correction:** Validate all executive-summary metrics against the original table before printing. If a derived metric is added, record its source row or formula in metadata or evaluation notes.

### 7. Exhibit Density Without Prioritization

**Symptom:** The document contains many tables and exhibit labels, but not all are ranked by importance.

**Why it matters:** Dense analysis must still guide attention.

**Correction:** Mark priority explicitly:

- `P1` for immediate management action.
- `P2` for follow-up investigation.
- `APPENDIX` for trace or completeness-only evidence.

### 8. Generic Action Language

**Symptom:** Phrases like "focus", "investigate", or "optimize" can appear without owner, timing, expected movement, or decision gate.

**Why it matters:** Consulting recommendations must be executable.

**Correction:** Convert actions into operating commitments:

```text
Action: Launch 14-day Fabric recovery sprint in Xingyi
Owner: Channel manager
Target: lift Fabric IYA from 0.226 to 0.50+
Decision gate: week 2 sales recovery and store execution audit
```

### 9. Pagination Treated As A Technical Check Only

**Symptom:** Page count, no clipping, and text extraction pass, but the narrative page rhythm is not reviewed.

**Why it matters:** A PDF can be technically valid and still feel like a report dump.

**Correction:** Inspect at least:

- Cover.
- Executive summary.
- First evidence page.
- One table-heavy page.
- Final recommendations page.

Each inspected page should have one clear job.

### 10. Passing The Rubric With A Known Caveat

**Symptom:** The evaluation can pass with "remaining recommendation: add takeaways to every exhibit."

**Why it matters:** If the caveat affects the core consulting standard, it should become a fix, not a footnote.

**Correction:** For McKinsey-style outputs, missing exhibit takeaways should cap `Exhibit Discipline` at 1 and should usually trigger one more revision when time allows.

## Pre-Ship Mentor Checklist

Before reporting success, answer these questions:

- Can I state the document's answer in one sentence?
- Does page 2 tell the executive what changed, why it matters, and what to do?
- Does every major exhibit have a takeaway?
- Are the top three actions specific enough for an owner to execute?
- Did I verify executive-page metrics against the source?
- Did I inspect at least one table-heavy page after PDF generation?
- Is anything styled only to look consulting-like without improving the decision?

If any answer is "no", revise before final delivery.
