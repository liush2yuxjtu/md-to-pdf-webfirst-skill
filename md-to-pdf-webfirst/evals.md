# McKinsey-Style PDF Evaluation

Use this rubric after generating any PDF requested as `麦肯锡 style`, `McKinsey style`, consulting style, board-report style, or executive strategy PDF polish.

The goal is McKinsey-inspired consulting clarity, not a branded clone. Do not use McKinsey logos, proprietary templates, or exact brand assets.

Before scoring, review `anti-patterns.md`. Do not pass a PDF that has an obvious storyline problem, a trust-breaking metric extraction issue, missing takeaways on major exhibits, or generic recommendations with no owner/timing/target.

If `frontend-design` was invoked, also review `frontend-design.md` and add the Frontend Design Pass dimension below.

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
- No gradients, shadows, beige editorial textures, playful styling, rounded card-heavy layouts, or decorative imagery.
- Typography is sans-serif, compact, and hierarchical.

### 3. Exhibit Discipline

- Major tables or analytic blocks are labeled as exhibits.
- Each major exhibit has a short takeaway or implication nearby.
- Tables are compact, scannable, and avoid avoidable row splitting.
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
- The PDF has no editorial hero, research-framework page, infographic, rebuilt figure/chart page, or chapter rhythm.
- The eval claims a perfect score while the contact sheet shows dense table pages with little visual hierarchy.
- The output includes reader-facing pipeline/tooling notes, fallback messages, metadata references, or Codex/API caveats.
- A page contains only a short narrative/table fragment with excessive blank space and no evidence block.

For business diagnosis HTML inputs, a passing eval must cite at least one full contact sheet or multiple page previews and must name the pages checked.
