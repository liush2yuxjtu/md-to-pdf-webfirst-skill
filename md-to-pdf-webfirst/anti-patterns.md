# McKinsey-Style PDF Anti-Patterns

Use this file as a consulting mentor review checklist before declaring a McKinsey-style PDF complete. The goal is McKinsey-inspired executive clarity, not visual imitation or branded cloning.

## Mentor Review From The Guizhou Yangfan PDF

The reviewed PDF was directionally stronger than a raw HTML printout: it added a clean cover, executive summary, issue map, section map, exhibit labels, and compact A4 tables. However, as a consulting intern deliverable, it still showed several classic anti-patterns that should be corrected in future runs.

## Anti-Patterns And Corrections

### 0. Consulting Skin Applied To Non-Consulting Documents

**Symptom:** A normal tutorial, API guide, workflow manual, or best-practices document is given a McKinsey-style redline cover, executive tone, or boardroom visual system even though the source is not a business diagnosis.

**Why it matters:** Consulting polish is not universally better. For technical documentation, the job is comprehension, navigation, code readability, and trust. A boardroom skin can make a guide feel pretentious, sparse, and harder to read.

**Correction:** Choose the mode from the source and the user request:

- Use `technical manual` mode for guides, docs, tutorials, workflow references, API notes, and best-practices pages.
- Use `McKinsey-style consulting` mode only when the user explicitly asks for consulting, board-report, executive strategy, or business diagnosis output.
- Do not let a prior McKinsey-style request pollute the default Markdown-to-PDF script.
- For technical docs, prioritize CJK-safe title layout, readable code blocks, section map, compact chapter pages, and a documentation aesthetic.

### 0.1 Tail Appendix Forced Onto Its Own Page

**Symptom:** A short final section such as `Related resources`, `Next steps`, or `References` is forced onto a separate mostly empty page because every second-level heading gets an unconditional page break.

**Why it matters:** Page count is not quality. A technically valid PDF can still feel sloppy if the last page is mostly whitespace caused by mechanical pagination.

**Correction:** For default technical-documentation mode, allow the final chapter/appendix to continue after the previous section when it is short. Keep strong page breaks for major chapters, but do not blindly force a mostly empty tail page.

### 0.2 Markdown Table Flattened Into Paragraph Soup

**Symptom:** A Markdown table appears in the PDF as one long paragraph with pipe characters, repeated dashes, and inline links smashed together.

**Why it matters:** This is one of the fastest ways to make a PDF feel broken. Tables are structural content, not prose; flattening them destroys comparison, scanning, and trust.

**Correction:** Parse Markdown pipe tables into real `<table>` markup before printing. Use compact table typography, visible header rows, cell borders, and `overflow-wrap:anywhere` for long links or examples. If a table is too wide, reduce type modestly and preserve row/column structure rather than flattening it.

### 0.3 MDX Or HTML Callout Tags Leaking Into The PDF

**Symptom:** Source-only tags such as `<Callout>`, `</Callout>`, `<Tip>`, or custom MDX wrappers appear verbatim in the PDF body.

**Why it matters:** Raw authoring tags tell the reader the converter failed. They also create ugly, confusing blocks that look like broken code instead of documentation.

**Correction:** Normalize known MDX/documentation tags into designed print components before Markdown parsing. `<Callout>` should become a real callout box; closing tags must never appear as literal text. Add a preview check that searches extracted PDF text for leaked tag names.

### 0.4 Thematic Breaks Printed As Asterisks

**Symptom:** Markdown separators such as `***`, `---`, or `___` appear as literal characters in the PDF.

**Why it matters:** Literal separator syntax is authoring scaffolding, not reader-facing content. It makes the document feel mechanically dumped.

**Correction:** Convert thematic breaks into horizontal rules with print-safe spacing.

### 0.5 Fixed Footer Colliding With Page Content

**Symptom:** A repeated footer line or note crosses over a heading, callout, or paragraph near the bottom of a PDF page.

**Why it matters:** Overlap at the page boundary instantly reads as broken print layout. It also hides the document hierarchy when a new subsection title is stranded at the bottom.

**Correction:** Do not use `position: fixed` footers in printed PDFs unless the page model reserves a bottom safe zone. Prefer hiding decorative footers in print, or use normal-flow footers. Add `break-after: avoid` to headings and keep heading-callout pairs together so a section does not begin inside the footer area.

### 0.6 Build Pipeline Label Printed On The Cover

**Symptom:** The cover includes internal production copy such as `DESIGNED HTML FIRST` or `PRINTED TO PDF WITH CHROME`.

**Why it matters:** The PDF reader needs the document, not the converter's self-description. Pipeline proof belongs in metadata, evals, or delivery notes.

**Correction:** Keep reader-facing covers clean. Move pipeline labels, Chrome proof, hashes, and generation notes into `<slug>-meta.json`, evals, gallery copy, or the final response.

### 0.7 Raw Markdown Syntax Inside Blockquotes

**Symptom:** A blockquote prints raw authoring syntax such as `## Documentation Index` instead of rendering the heading text.

**Why it matters:** Raw Markdown markers make the document feel mechanically dumped and raise doubts about what else was not parsed.

**Correction:** Group consecutive `>` lines into one blockquote and parse basic nested Markdown inside it: headings, paragraphs, lists, inline code, links, bold, and emphasis. The reader should see `Documentation Index`, not `## Documentation Index`.

### 0.8 Prose Snippet Misclassified As Code

**Symptom:** A documentation excerpt or prompt snippet is rendered as a black executable code block even though it is explanatory prose or Markdown content.

**Why it matters:** Code styling is a semantic claim. Mislabeling prose as code makes pages heavy and confuses what the reader is expected to run.

**Correction:** Treat fenced `markdown`, `mdx`, `text`, and documentation-like snippets as light documentation examples. Reserve dark code blocks for executable commands, program code, terminal output, or genuinely code-like source.

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
