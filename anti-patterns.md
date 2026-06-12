# McKinsey-Style PDF Anti-Patterns

Use this file as a consulting mentor review checklist before declaring a McKinsey-style PDF complete. The goal is McKinsey-inspired executive clarity, not visual imitation or branded cloning.

## Mentor Review From The Guizhou Yangfan PDF

The reviewed PDF was directionally stronger than a raw HTML printout: it added a clean cover, executive summary, issue map, section map, exhibit labels, and compact A4 tables. However, as a consulting intern deliverable, it still showed several classic anti-patterns that should be corrected in future runs.

## Anti-Patterns And Corrections

### 0. Fake Consulting Skin Instead Of A Real Publication Report

**Symptom:** A tutorial, API guide, workflow manual, best-practices document, or business report gets a superficial red/navy skin, but the PDF still feels like a plain source dump or a generic booklet.

**Why it matters:** The required standard is McKinsey-inspired publication quality for every output. That means strong cover, clear executive/reader promise, section rhythm, evidence blocks, readable exhibits, and source trace. A decorative skin without structure is worse than honest documentation because it claims authority without earning it.

**Correction:** Use one report visual family for all outputs:

- All outputs use McKinsey-style publication structure by default.
- Business reports use answer, evidence, implication, action.
- Technical docs use what matters, how to use it, examples, checklist.
- Never invent unsupported business recommendations for non-business source material.
- Never downgrade to a plain technical-manual/booklet aesthetic.

### 0.0.1 Business Diagnosis HTML Treated As Generic Documentation

**Symptom:** A local business diagnosis HTML report with RD, Hub, IYA, YoY, category, action-plan, and many tables is converted into a clean but plain table booklet because the user did not explicitly say `McKinsey` or `publication`.

**Why it matters:** Business diagnosis reports are decision documents. If the converter treats them as generic documentation, the output can pass basic PDF checks while failing the actual reader job: quick executive understanding.

**Correction:** Auto-route these inputs to publication-report mode. Add cover, foreword, research framework, executive summary, infographic, rebuilt figures, chapter rhythm, source notes, and references. Preserve source tables later in the report, but do not lead with table dumps.

### 0.0.2 False-Positive Eval Pass For A Table Dump

**Symptom:** The eval gives a high or perfect score because the PDF has page count, no Chrome headers, readable tables, and source fidelity, while the contact sheet clearly shows a plain source-table report with no editorial hero, figure rhythm, or publication-grade evidence pages.

**Why it matters:** A rubric that can pass a bad-looking output teaches the skill the wrong lesson.

**Correction:** Treat this as a hard fail. The evaluator must inspect a contact sheet or representative page set and cap/zero the relevant dimensions when a business report lacks publication rhythm, rebuilt figures, and visual evidence pages.

### 0.0.3 Business Overview Markdown Treated As Generic Documentation

**Symptom:** A short Markdown file such as `总览.md` contains `总体判断`, `IYA`, `PS 门店`, `品类`, `Low Base`, `建议`, and a category table, but the converter renders it as a generic Markdown booklet or a hand-coded one-off page because the prompt did not explicitly say `McKinsey`.

**Why it matters:** L1 business overview Markdown is still a decision document. The reader needs an answer-first executive overview, rebuilt figures, source table, and action page. A plain Markdown conversion can look neat while missing the core consulting job.

**Correction:** Auto-route business overview Markdown to `business-markdown-publication` mode. Generate designed HTML, PDF, metadata, cover preview, contact sheet, and eval. The output should be compact rather than padded to 20 pages, but it must include cover, executive answer, table of contents, research framework, at least one rebuilt figure, source table, action page, and source notes.

### 0.0.4 Generic Booklet Fallback Instead Of Publication Report

**Symptom:** The helper handles an input by producing a generic Markdown booklet: cover, table of contents, and a mostly linear source dump, with `mode: markdown-booklet` or equivalent behavior.

**Why it matters:** The skill promise is web-first publication output. A booklet fallback can pass technical PDF checks while failing the expected artifact level: editorial structure, page rhythm, source trace, visual evidence, contact sheet, and eval.

**Correction:** Default every conversion to publication-report output. Technical documents can use a documentation-publication style, while business reports use consulting/publication style. Do not allow a plain booklet fallback.

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

**Symptom:** The cover includes internal production copy such as `DESIGNED HTML FIRST`, `PRINTED TO PDF WITH CHROME`, `Publication report / web first`, or other generator-facing labels.

**Why it matters:** The PDF reader needs the document, not the converter's self-description. Pipeline proof belongs in metadata, evals, or delivery notes.

**Correction:** Keep reader-facing covers clean. Move pipeline labels, Chrome proof, hashes, and generation notes into `<slug>-meta.json`, evals, gallery copy, or the final response.

### 0.6.1 Weak Cover That Is Not Publication Level

**Symptom:** The cover has a centered title on a decorative grid, generic vertical bars, or a sparse template look. It may be technically clean, but it does not feel like a serious consulting/publication report.

**Why it matters:** The cover sets the quality contract. If page 1 looks like a default template, the reader will not trust later claims of "publication report" or "McKinsey style".

**Correction:** Every cover should use the same high-quality report family as the accepted business overview PDF: dark editorial field, sharp red/navy/teal system, strong title block, meaningful eyebrow, visual motion/figure cue, stable folio, and no source/debug table on the cover. Put source paths, hashes, and generation notes in metadata/evals, not page 1.

### 0.7 Raw Markdown Syntax Inside Blockquotes

**Symptom:** A blockquote prints raw authoring syntax such as `## Documentation Index` instead of rendering the heading text.

**Why it matters:** Raw Markdown markers make the document feel mechanically dumped and raise doubts about what else was not parsed.

**Correction:** Group consecutive `>` lines into one blockquote and parse basic nested Markdown inside it: headings, paragraphs, lists, inline code, links, bold, and emphasis. The reader should see `Documentation Index`, not `## Documentation Index`.

### 0.8 Prose Snippet Misclassified As Code

**Symptom:** A documentation excerpt or prompt snippet is rendered as a black executable code block even though it is explanatory prose or Markdown content.

**Why it matters:** Code styling is a semantic claim. Mislabeling prose as code makes pages heavy and confuses what the reader is expected to run.

**Correction:** Treat fenced `markdown`, `mdx`, `text`, and documentation-like snippets as light documentation examples. Reserve dark code blocks for executable commands, program code, terminal output, or genuinely code-like source.

### 0.9 Documentation Index Preamble Printed As Content

**Symptom:** A source-acquisition preamble such as `Documentation Index`, `llms.txt`, or "discover all available pages" appears at the start of the PDF body.

**Why it matters:** These blocks help the crawler or reader discover source pages; they are not part of the report or guide. Printing them makes the PDF feel like a scraped intermediate artifact.

**Correction:** When a `Documentation Index` / `llms.txt` block appears before the real document title, suppress it from reader-facing output. Record the suppression in metadata if useful, but start the PDF body with the actual document.

### 0.10 Business Diagnosis Chain Rendered As Terminal Code

**Symptom:** A root-cause chain, issue tree, or business diagnosis path with arrows such as `门店层 → Hub层 → 品类层 → RD整体` is rendered as a black terminal-style code block.

**Why it matters:** A diagnosis chain is a reasoning exhibit, not executable code. Black code styling makes it look like a command/output artifact and hides the business logic the reader should scan.

**Correction:** Detect narrative chains containing arrows and tree glyphs (`→`, `├──`, `└──`) and render them as a light diagnosis-flow component with visible steps. Reserve dark code blocks for commands, source code, logs, or terminal output.

### 0.11 Heading Or Exhibit Label Orphaned At Page Bottom

**Symptom:** A heading or exhibit label appears at the bottom of a page, while the table, diagram, or first paragraph it introduces begins on the next page.

**Why it matters:** This breaks the reader's scanning flow and makes the next page feel detached. In consulting PDFs, an exhibit label without its exhibit reads as unfinished page composition.

**Correction:** Keep headings with their first evidence block using a wrapper such as `keep-block`, `subsection`, or `heading-table-group` with `break-inside: avoid`. If there is not enough room left on the page, move the heading and evidence block together to the next page.

### 0.12 Short Continuation Fragment Page

**Symptom:** A new page contains only the final few bullets, rows, or one short paragraph from the previous analysis block, followed by a large blank area.

**Why it matters:** The PDF may be technically valid, but the page rhythm feels accidental. A partner-style review expects each page to have a clear job, not leftover fragments.

**Correction:** Keep compact subsections together, rebalance spacing, or move the subsection start to the next page. If a continuation is unavoidable, repeat a small continuation header so the page remains self-explanatory.

### 0.13 Diagnosis Or Issue-Tree Exhibit Too Small To Scan

**Symptom:** A causality map, issue tree, or diagnosis-flow exhibit is present but rendered as tiny boxes with cramped text.

**Why it matters:** The exhibit is supposed to clarify the logic. If it reads as a footnote, it loses the value of turning prose into a visual.

**Correction:** Give diagnosis-flow components enough padding, larger node text, and wrapping room. Split long chains into rows or grouped branches instead of forcing the full tree into one narrow line.

### 0.14 Tiny Typography Used To Control Page Count

**Symptom:** Body text, table cells, or wide-table rows are shrunk until the PDF fits a target page count, for example body text below `11px`, normal tables below `10px`, or wide tables below `9.5px`.

**Why it matters:** A PDF that looks tidy in thumbnails can become unreadable on A4. Consulting polish is not fewer pages; it is fast comprehension at real reading size.

**Correction:** Do not trade readability for page count. Increase the page count, split wide tables, simplify columns, or repeat context headers. As a default floor, use body/list text `>= 11px`, normal tables `>= 10px`, dense/wide tables `>= 9.5px`, notes/callouts `>= 10px`, and code/documentation snippets `>= 9.5px`.

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
