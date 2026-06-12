# McKinsey-Style PDF Evaluation

Use this rubric after generating any PDF requested as `麦肯锡 style`, `McKinsey style`, consulting style, board-report style, or executive strategy PDF polish.

The goal is McKinsey-inspired consulting clarity, not a branded clone. Do not use McKinsey logos, proprietary templates, or exact brand assets.

Before scoring, review `anti-patterns.md`. Do not pass a PDF that has an obvious storyline problem, a trust-breaking metric extraction issue, missing takeaways on major exhibits, or generic recommendations with no owner/timing/target.

If `frontend-design` was invoked, also review `frontend-design.md` and add the Frontend Design Pass dimension below.

Hard fail any PDF that exposes raw input syntax or implementation code as reader content, including `<!doctype html>`, `<html>`, `<head>`, `<style>`, `</style>`, CSS variables, selectors such as `body {`, or rules such as `box-sizing`. Existing HTML pages must be semantically extracted before publication rendering; they must not be printed as source. For Markdown/rubric documents that intentionally discuss these strings, classify them as source-authored examples and still review their formatting, but do not call them raw-source leakage.

Hard fail weak generic covers that expose converter boilerplate such as `PDF-friendly web edition`, `Markdown Document`, or source/debug tables on page 1. A publication cover must use a reader-facing title/subtitle derived from the source or from neutral report language.

For publication-report, MGI-style, or business-report outputs, hard fail a cover that lacks reader-facing publication metadata: title, subtitle, report date/period, and author/institution. When no publisher is supplied, the expected default institution is `Win-Channel AI Research Institute`.

## Required Evidence

Record these facts in the output evaluation file:

- Source path or URL
- Designed HTML path
- PDF path
- Cover preview path
- Page count
- First three pages text extraction character count
- PDF byte size and short SHA-256 hash
- Whether Chrome default headers/footers are absent
- Whether the cover preview was visually inspected
- Whether a full contact sheet or representative page set was visually inspected, not only the cover
- Raw source leakage scan for HTML/CSS/Markdown authoring syntax in extracted PDF text
- Source-authored raw syntax examples, if any, kept separate from leakage
- Weak generic cover scan for converter boilerplate
- Cover metadata check: topic-relevant visual/human cue, title, subtitle, date/period, institution/authors
- Front-matter check: designed contents page and one-page executive summary when the report is long or business-oriented
- Figure vocabulary check: whether sparse numbers, percentages, before/after data, ordinal categories, geography, and part-to-whole data were mapped to suitable exhibit types when present
- Evidence system check: figure numbers, source notes, footnotes/references, and related-publication page when available

## Evaluation Artifact Menu

Every publication-report run must produce at least one Markdown evaluation file. HTML evaluation files are optional reviewer/gallery surfaces, but should be produced whenever the user asks for a gallery, changelog, browser-review page, GitHub Pages update, or a non-technical review handoff.

## Skill Regression Eval Boards

Whenever `SKILL.md` changes, the regression requirement is stronger than a single PDF eval. Run every input in `eval-inputs.md` with a fresh subagent or non-interactive Codex execution, then create consolidated eval boards:

`<suite-slug>-eval-board.md`

`<suite-slug>-eval-board.html`

The board must show one row per input with source path, output directory, PDF path, contact sheet path, eval paths, mode, page count, PDF hash, hard-fail scan status, human review status, and follow-up owner/file.

Human review status must be one of:

- `PASS`
- `FAIL`
- `PENDING HUMAN REVIEW`

Do not mark a `SKILL.md` update complete until the eval boards are shown to the human reviewer. If the board contains `FAIL`, or if the human marks a defect that the eval missed, update `anti-patterns.md`, this rubric, and any relevant script/template before rerunning the full `eval-inputs.md` suite.

### Required Markdown Eval

`<slug>-evals.md`

- Primary machine-readable and human-readable scorecard.
- Must include Required Evidence, rubric scores, hard-fail scan, decision, fixes made, and remaining recommendations.
- Must be generated for `publication-report`, `business-html-publication`, and `business-markdown-publication` modes.
- Must be referenced from metadata as `evals`.

### Recommended HTML Eval

`<slug>-evals.html`

- Browser-friendly companion to `<slug>-evals.md`.
- Use for gallery/changelog pages, non-technical review, or side-by-side PDF QA.
- Must link or name the PDF, designed HTML, cover preview, contact sheet, and metadata.
- Must not contain internal process excuses, Codex/API caveats, or fallback notes as reader-facing content.
- Should be referenced from metadata as `evals_html` when generated.

### Optional Focused Markdown Evals

Use these only when the run needs deeper inspection, or when a prior review comment targets the relevant failure class:

| File | Purpose | When to create |
| --- | --- | --- |
| `<slug>-page-review.md` | Page-by-page display QA. | Long reports, repeated visual defects, or user asks for page-by-page review. |
| `<slug>-source-fidelity.md` | Source-to-output metric and table trace. | Business reports, executive metrics, or suspected extraction mistakes. |
| `<slug>-anti-pattern-review.md` | Explicit scan against `anti-patterns.md`. | McKinsey/consulting polish, publication redesigns, or regression reviews. |
| `<slug>-readability.md` | Typography, table size, whitespace, and A4 readability check. | Any complaint about tiny text, blank pages, cramped charts, or unreadable tables. |
| `<slug>-gallery-entry.md` | Short changelog/gallery summary. | GitHub Pages gallery or changelog updates. |

### Optional Focused HTML Evals

HTML variants should mirror the Markdown file names when a reviewer needs a browser surface:

| File | Purpose | When to create |
| --- | --- | --- |
| `<slug>-page-review.html` | Visual reviewer page with page thumbnails and comments. | Page-by-page design review, gallery QA, or stakeholder review. |
| `<slug>-source-fidelity.html` | Browser-readable evidence trace. | Metric-heavy reports where trust depends on source lineage. |
| `<slug>-anti-pattern-review.html` | Anti-pattern checklist with pass/fail badges. | Skill regression review or consulting mentor review. |
| `<slug>-readability.html` | Readability inspection surface. | Typography/table-size fixes or mobile/browser preview checks. |
| `<slug>-gallery-entry.html` | Embeddable gallery/changelog card. | GitHub Pages gallery and changelog pages. |

### Naming And Metadata Rules

- Put eval artifacts beside the generated PDF unless the gallery/changelog system has a dedicated folder.
- Do not overwrite prior evals for a materially different PDF; use a fresh slug or timestamp.
- Metadata must at minimum point to `<slug>-evals.md`; add `evals_html` and focused eval paths when present.
- The eval artifact must describe what was inspected, not only what the generator intended.
- If a hard-fail condition is present, the eval must say `Fail` even if the numeric subtotal looks good.

## Scoring

Score each dimension from 0 to 2.

`0` means missing or materially weak.
`1` means present but needs polish.
`2` means strong enough to share with an executive reviewer.

### 1. Executive Narrative

- The cover names the client/topic, period, and report type clearly.
- Page 2 or the first content page states the core finding, business impact, and next actions.
- Section order moves from answer to evidence, not from raw detail to conclusion.

### 2. Consulting Visual System

- White paper, charcoal text, restrained gray rules, one sharp red accent, and optional deep blue secondary emphasis.
- Cover and chapter system match the accepted McKinsey-style business overview family: dark editorial cover, red/navy/teal accents, stable folio, and serious publication rhythm.
- Publication covers include topic-relevant human/editorial imagery plus title, subtitle, date/period, and institution/authors.
- Long reports use designed contents, one-page summary, and chapter-opener visual rhythm where practical.
- No weak template covers, decorative grids, reader-facing source/debug tables, playful styling, rounded card-heavy layouts, or generic booklet aesthetics.
- Typography is sans-serif, compact, and hierarchical.

### 3. Exhibit Discipline

- Major tables or analytic blocks are labeled as exhibits.
- Each major exhibit has a short takeaway or implication nearby.
- Tables are compact, scannable, and avoid avoidable row splitting.
- Sparse numeric pages become number-in-figure exhibits rather than raw metric lists.
- Data shape drives chart choice: unit blocks/stacked bars for percentages, before/after frames for baseline-target data, bubble/circle matrices for ordered categories, pie/donut for part-to-whole, and map bubbles for geography.
- Missing exhibit takeaways should cap this score at `1`, even if the tables look clean.

### 4. Information Density And Readability

- Pages feel dense but not cramped.
- Headlines, section labels, tables, and body text are readable in the PDF preview.
- Numeric and status columns are easy to compare.

### 5. Print And Pagination Quality

- A4 print CSS is explicit.
- Cover and major chapters have intentional page breaks.
- No Chrome default header/footer appears.
- No obvious clipping, overlap, orphaned section headings, or blank first page.

### 6. Source Fidelity

- Original business content, headings, and tables are preserved unless intentionally summarized.
- Any added executive summary is clearly derived from source content.
- Metadata records source file/hash and output hashes.
- Executive-page metrics are checked against the source table or recorded derivation.
- External cases or public references are cited when browsing was used for credibility; otherwise the eval explicitly says evidence is source-only.

### 7. Mentor Anti-Pattern Scan

- The PDF has been checked against `anti-patterns.md`.
- Any high-impact anti-pattern found during review was fixed before final scoring.
- Remaining caveats are low-impact and explicitly listed.

### 8. Frontend Design Pass

Use this dimension only when `frontend-design` is invoked.

- The PDF has a clear aesthetic point of view, not only a McKinsey-colored skin.
- Typography is intentional and avoids generic default stacks where practical.
- The cover/front matter is memorable and answer-first.
- Repeated visual motifs support hierarchy, exhibits, and action flow.
- PDF previews confirm the design survives print rendering.

## Pass Criteria

The PDF passes when:

- Total score is at least 12 out of 14.
- If `frontend-design` is invoked, total score is at least 14 out of 16.
- No dimension scores 0.
- Required evidence is complete.
- Visual preview has been inspected and obvious layout defects were fixed.

## Output Template

```markdown
# PDF Evaluation

## Evidence

- Source:
- HTML:
- PDF:
- Preview:
- Pages:
- First three pages extracted text:
- PDF bytes:
- PDF SHA-256 short:
- Chrome headers/footers absent:
- Cover preview inspected:

## McKinsey-Style Rubric

| Dimension | Score | Notes |
| --- | ---: | --- |
| Executive Narrative |  |  |
| Consulting Visual System |  |  |
| Exhibit Discipline |  |  |
| Information Density And Readability |  |  |
| Print And Pagination Quality |  |  |
| Source Fidelity |  |  |
| Mentor Anti-Pattern Scan |  |  |
| Frontend Design Pass |  | Only score when frontend-design was invoked. |

## Decision

Pass/Fail:

Total:

Fixes made:

Remaining recommendations:
```

## Hard Fail Conditions

The evaluation must be `Fail` regardless of numeric subtotal when any of these are true:

- A business diagnosis HTML report is mostly a source-table dump with only light styling.
- A business overview Markdown report with IYA/PS/category/action signals is converted as a generic Markdown booklet instead of `business-markdown-publication`.
- Any conversion falls back to a generic booklet mode instead of publication-report output.
- The cover is not publication level: generic centered title, decorative grid, weak vertical bars, source/debug table on page 1, or reader-facing pipeline label.
- A publication/business cover lacks subtitle, report date/period, or author/institution.
- The PDF has no editorial hero, research-framework page, infographic, rebuilt figure/chart page, or chapter rhythm.
- A long/business report lacks a designed table of contents or one-page executive summary.
- Sparse data pages print a handful of numbers or small tables without a number-in-figure, big-number callout, or suitable exhibit.
- Obvious data shapes are not visualized: percentages without share/unit-block treatment, ordinal low/middle/high data without bubbles/circles, geographic data without map/bubble treatment when location is central, or current/future data without a comparison frame.
- The eval claims a perfect score while the contact sheet shows dense table pages with little visual hierarchy.
- The output includes reader-facing pipeline/tooling notes, fallback messages, metadata references, or Codex/API caveats.
- A page contains only a short narrative/table fragment with excessive blank space and no evidence block.
- The final reader-facing page is an internal process note instead of references, methodology, related publications, or a deliberate closing page.

For business diagnosis HTML inputs, a passing eval must cite at least one full contact sheet or multiple page previews and must name the pages checked.
