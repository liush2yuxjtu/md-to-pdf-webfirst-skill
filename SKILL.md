---
name: md-to-pdf-webfirst
description: Convert Markdown files, Markdown URLs, or report HTML into polished PDFs by designing a PDF-friendly web page first, then printing that page to PDF. Use this skill whenever the user asks to convert .md/HTML to PDF, wants a better-looking PDF, asks for frontend-design to improve PDF output, mentions "web first", "PDF-friendly web", "HTML then PDF", asks for consulting/McKinsey-style PDF polish, or wants proof/reporting around a Markdown-to-PDF workflow.
---

# Markdown to PDF, Web First

Use this skill to turn Markdown into a designed, readable PDF by following the final workflow:

1. Get the Markdown or report HTML source.
2. Build a print-friendly HTML page from the Markdown.
3. Apply frontend design to the HTML as the PDF layout surface.
4. Print the HTML to PDF with Chrome.
5. Verify the PDF and create preview evidence.
6. If requested, report the result with `talk-html`.

This skill exists because direct Markdown-to-PDF conversion often produces plain text pages. The better route is to make the PDF layout as a web page first, then print that page.

Default output contract: always produce a McKinsey-inspired publication report, not a generic booklet. Every output, including technical documentation, must use the same executive-report visual family as the best business overview examples: dark editorial cover, sharp red/navy/teal system, section map, answer-first front matter, clear chapters, evidence/examples, source trace, preview/contact sheet, and eval. Do not provide a plain/quick booklet fallback or a separate low-polish documentation aesthetic.

## When To Use

Use this skill when the user asks for any of these:

- Convert a `.md` file, Markdown URL, or report HTML file to PDF.
- Make the PDF look better, more polished, more designed, or more readable.
- Use `frontend-design` for the PDF itself.
- Generate a PDF-friendly web page first, then convert to PDF.
- Produce evidence, preview images, hashes, page counts, or a `talk-html` report for the conversion.

If the user asks for a quick PDF, still use the publication-report route and keep the report concise rather than switching to a generic booklet.

## Final Workflow

### 1. Prepare Names

Create stable output names with a unique slug:

```text
<slug>.md
<slug>.html
<slug>.pdf
<slug>-meta.json
previews/<slug>-pdf-cover.png
previews/<slug>-html.png
```

For repeated attempts, use a fresh suffix such as `webfirst`, `final`, or a timestamp. Do not overwrite earlier versions unless the user explicitly asks.

### 2. Fetch Or Read Markdown

For URL input:

```bash
curl -L --fail --silent --show-error "$URL" -o outputs/<slug>.md
```

For local input, copy or read the existing Markdown path and keep the original untouched.

For local HTML reports or generated web pages, keep the original file untouched and preserve it as `<slug>-source.html`. Never treat the raw HTML file as Markdown text. Strip `head`, `style`, `script`, `svg`, `nav`, and browser/page chrome, extract the readable title/body/headings/tables/cards into reader Markdown, then render that through the same McKinsey-style publication-report shell. The PDF body must not show `<!doctype html>`, `<html>`, `<style>`, CSS variables, selectors, or raw DOM/CSS source.

For local business diagnosis HTML reports, automatically use publication-report mode even when the prompt does not explicitly say `McKinsey`, `MGI`, or `publication`. Trigger this when the source contains business-report signals such as `RD`, `Hub`, `IYA`, `YoY`, `GIV`, `品类`, `诊断`, `行动`, multiple tables, and an executive/diagnosis title. A plain prompt like `$md-to-pdf-webfirst file:///...业务诊断报告.html` must produce a reader-ready publication PDF, not a lightly styled source-table dump.

For local business overview Markdown reports, also automatically use publication-report mode when the source contains signals such as `IYA`, `PS`, `品类`, `门店`, `同比`, `环比`, `总体判断`, `值得表扬`, `有提升空间`, `Low Base`, `建议`, a business/diagnosis/overview title, or a Markdown table headed by `品类`. A plain prompt like `Md to PDF Webfirst @总览.md` must produce the same class of artifacts as business HTML mode: designed HTML, PDF, metadata, cover preview, contact sheet, and eval. Do not hand-code a one-off HTML page when the helper script can route this case. If the prompt is a non-interactive Codex verification prompt, run the bundled helper script first and treat a generic/manual converter as a skill failure.

Collect basic source metadata:

- line count
- byte size
- SHA-256 short hash
- heading counts
- code fence count

### 3. Design The PDF-Friendly Web Page

Treat the HTML as the PDF design surface.

Use a strong but print-safe McKinsey-inspired publication direction. Good defaults:

- Executive advisory report
- Research-institute field guide
- Dense but readable consulting report
- Dark editorial cover with red/navy/teal accents

Avoid generic web-app landing pages. This is not a marketing page; it is a printable document.

#### Default McKinsey-Style Publication Mode

Use this publication-report mode for ordinary Markdown docs such as tutorials, best-practices guides, API notes, workflow references, and code-heavy documentation:

- Use the same McKinsey-style visual family as business overview PDFs. Technical documents should be consulting-grade publications, not plain documentation booklets.
- Still produce a publication report. Do not fall back to a plain generic booklet with only cover, table of contents, and dumped Markdown body.
- Optimize for comprehension: section map, stable chapter hierarchy, readable paragraphs, strong code-block contrast, and CJK-safe cover/title layout.
- Use white paper interiors, strong dark cover, restrained gray rules, red/navy/teal accents, stable folios, and exhibit-like evidence blocks.
- Preserve authoring structure: Markdown pipe tables must render as real tables, MDX-style callouts must render as designed callout boxes, and thematic breaks must render as rules instead of raw syntax.
- Prevent page-bottom collisions: do not print fixed footers unless the content area reserves a real bottom safe zone, and do not leave headings or heading-callout pairs orphaned at the bottom of a page.
- Keep production notes out of reader-facing pages: cover pages must not show pipeline labels such as `DESIGNED HTML FIRST` or `PRINTED TO PDF WITH CHROME`; those belong in metadata or evals, not the PDF body.
- Parse Markdown inside blockquotes and documentation snippets enough to avoid raw authoring syntax such as `## Heading` leaking into the PDF.
- Distinguish runnable code from documentation excerpts. Fenced `markdown`, `mdx`, or prose examples should render as light documentation snippets, not black terminal/code blocks.
- Render business diagnosis chains, issue trees, and root-cause paths as light flow/chain components. Do not print `→`, `├──`, or `└──` narrative chains as black executable code blocks.
- Suppress source-acquisition preambles such as `Documentation Index`, `llms.txt`, and "discover all available pages" blocks when they appear before the real document title.
- Do not invent business recommendations for non-business documents. Instead, translate the source into consulting-style guide structure: "what matters", "how to use it", "evidence/examples", and "review checklist".
- Review `anti-patterns.md`, especially weak covers, raw source leakage, sparse pages, and eval false positives.

#### McKinsey-Style Consulting Mode

Use this mode whenever the user asks for `麦肯锡 style`, `McKinsey style`, consulting style, board-report style, or executive strategy PDF polish. Treat it as McKinsey-inspired consulting presentation craft, not a branded clone:

- Also use this mode automatically for business diagnosis HTML or business overview Markdown inputs with RD/Hub/IYA/YoY/PS/category/action signals, even if the user only asks for basic conversion. Business diagnosis reports and L1 business overview Markdown files are decision documents by default, not generic documentation.
- If the user asks for MGI-style, research-institute-style, full publication report, editorial hero, generated imagery, figure rebuilds, stable page numbers, footnotes, or references, load `publication-report/README.md` and its referenced files before designing. That module cites local adapters in `supporting-skills/` for image generation, typography, and color. Keep publication-specific rules in subfolders instead of expanding this main skill file.
- When the user also invokes `frontend-design`, read `frontend-design.md` and apply a real frontend design pass to the PDF HTML. Commit to an aesthetic direction before coding, then verify it in PDF previews.
- Use a crisp executive-consulting visual system: white paper, black/charcoal text, restrained gray rules, one sharp red accent, and optional deep blue only for secondary emphasis.
- Put the "so what" first: cover, executive one-page, issue map, and then chaptered evidence.
- Prefer dense but readable exhibit pages over decorative layouts. Use exhibit labels such as `EXHIBIT 1`, `KEY TAKEAWAY`, `IMPLICATION`, and `ACTION`.
- Use sans-serif typography, strong hierarchy, compact tables, numbered sections, thin dividers, and generous whitespace around headlines.
- Avoid beige editorial themes, decorative textures, shadows, rounded cards, gradients, stock imagery, and playful styling.
- Make tables consulting-ready: compact but readable type, strong header rows, zebra striping only when useful, right-aligned numeric columns where practical, and no row splitting when avoidable.
- Do not shrink body or table text below readable print sizes to control page count. Prefer adding pages, splitting wide tables, or repeating context headers over using tiny typography.
- Minimum readable A4 print sizes: body/list text `>= 11px`, normal tables `>= 10px`, dense/wide tables `>= 9.5px`, notes/callouts `>= 10px`, code/documentation snippets `>= 9.5px`.
- Run a page-by-page display review before delivery. Fix orphaned headings, detached exhibit labels, short continuation fragments, and mostly blank tail pages before calling the PDF final.
- Keep headings with their first evidence block. A heading such as `6.3 行动效果预期` must never appear alone at the bottom of one page while its table starts on the next page.
- Keep compact subsections together when possible. If a small `h3` analysis block spills only two or three lines onto a new page, move the whole subsection to the next page or rebalance spacing.
- Size issue trees and diagnosis-chain exhibits for scanning. They should read as business exhibits, not tiny footnotes or cramped diagrams.
- Review against `anti-patterns.md` before final delivery. Fix the obvious consulting anti-patterns, especially weak storyline, missing exhibit takeaways, unverifiable executive metrics, and generic actions.
- Add an evaluation artifact for the produced PDF using `evals.md` before reporting success.

The HTML should include:

- cover page
- executive one-page summary when the source is a business report
- issue map or operating agenda when the source contains diagnostics/actions
- editorial research-framework page when the source is a business diagnosis HTML report or short business overview Markdown
- at least one rebuilt figure/chart page before long source tables when the source has enough numeric table data
- for short business overview Markdown, do not force 20 pages; generate a compact publication report with enough pages to cover cover, executive answer, table of contents, research framework, rebuilt figure(s), source table, actions, and source notes without blank filler
- section map / table of contents
- clear heading hierarchy
- print-friendly A4 CSS
- code blocks with strong contrast
- readable lists and callouts
- real table markup for Markdown pipe tables
- no leaked source-only tags such as `<Callout>` or `</Callout>`
- print CSS that prevents fixed footers from overlapping flowing content
- print CSS that preserves readable minimum type sizes; never use tiny table text as a pagination hack
- no reader-facing build pipeline labels on the cover
- no raw Markdown heading markers inside blockquotes
- prose/documentation snippets visually distinct from executable code blocks
- business diagnosis chains rendered as readable flow components instead of terminal-style code
- no source-acquisition preambles such as `Documentation Index` / `llms.txt` printed as reader content
- no orphaned heading/exhibit labels at page bottoms
- no detached continuation pages containing only a small tail fragment
- no false-positive eval pass where a table-heavy source dump is scored as consulting/publication-ready without editorial hero, figure rhythm, or full-page visual review
- no raw HTML/CSS source leakage when the input is an existing `.html` page; generic HTML must be semantically extracted before publication rendering
- `@page { size: A4; margin: ... }`
- explicit page breaks for cover and major sections
- `@media print` rules that remove shadows and browser-only effects

Use CSS like:

```css
@page { size: A4; margin: 14mm 16mm 15mm; }
.page { break-after: page; page-break-after: always; }
.chapter { break-before: page; page-break-before: always; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; break-inside: avoid; }
```

### 4. Convert HTML To PDF

Prefer Chrome when available:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new \
  --disable-gpu \
  --disable-background-networking \
  --disable-component-update \
  --disable-sync \
  --no-first-run \
  --no-default-browser-check \
  --user-data-dir="$PWD/work/chrome-profile-<slug>" \
  --no-pdf-header-footer \
  --print-to-pdf="$PWD/outputs/<slug>.pdf" \
  "file://$PWD/outputs/<slug>.html"
```

Important:

- Use `--no-pdf-header-footer`; otherwise Chrome may add date, title, URL, and page numbers.
- Delete or move the old PDF before rerunning, so you do not accidentally validate a stale file.
- If Chrome hangs after writing the file, stop only the temporary profile process and keep the written PDF.

### 5. Verify The PDF

Verify with `pypdf`:

```python
from pypdf import PdfReader

reader = PdfReader("outputs/<slug>.pdf")
text = "".join((page.extract_text() or "") for page in reader.pages[:3])
print(len(reader.pages), len(text))
```

Record:

- page count
- first 3 pages extracted text length
- PDF bytes
- PDF SHA-256 short hash

### 6. Generate Visual Evidence

Create a real PDF cover preview:

```bash
qlmanage -t -s 1400 -o work/preview outputs/<slug>.pdf
cp work/preview/<slug>.pdf.png outputs/previews/<slug>-pdf-cover.png
```

Inspect the preview:

- no blank page
- no browser default header/footer
- cover does not leak the next page unless intentionally designed
- text is readable
- code and section styling are visible in later pages when possible

### 6.5 Evaluate The PDF

When the user asks for consulting/McKinsey-style output, add an evaluation file beside the output using the rubric in `evals.md`.

Before scoring, run the mentor checklist in `anti-patterns.md`. If the PDF has a known high-impact anti-pattern, revise instead of only mentioning it as a limitation.

When `frontend-design` is invoked, also score the frontend-design dimension from `frontend-design.md`.

The evaluation must include:

- output PDF path, HTML path, and preview path
- page count and text extraction result
- score for each McKinsey-style dimension
- pass/fail decision
- concrete fixes made or still recommended

The PDF is not done until obvious McKinsey-style failures are fixed and the rerun passes the rubric.

### 7. Report With Talk Html

If the user asks for a report, use the `talk-html` skill after the conversion is complete.

The report should focus on proof, not decoration:

- show the real PDF cover preview
- list Markdown, HTML, PDF, preview, and metadata paths
- state the pipeline: `Markdown -> PDF-friendly HTML -> Chrome print-to-PDF`
- include page count and extracted text verification
- include source URL or source file
- include limitations, such as custom MDX tags being simplified

Publish unless the user says local-only.

## Script

This skill includes a reusable helper:

```bash
python3 ~/.codex/skills/md-to-pdf-webfirst/scripts/md_to_pdf_webfirst.py \
  --input <markdown-file-or-url> \
  --slug <slug> \
  --out-dir outputs
```

For plain Codex CLI prompts such as `Md to PDF Webfirst @总览.md`, use this helper as the first implementation step. Do not create an ad hoc `scripts/build-*.mjs` or one-off converter in the source folder when the helper can process the file. If the helper returns a generic booklet for a business overview Markdown source, fix the skill's detector/template first, then rerun.

The script creates:

- `<slug>.md`
- `<slug>.html`
- `<slug>.pdf`
- `<slug>-meta.json`
- `previews/<slug>-pdf-cover.png`
- `previews/<slug>-contact-sheet.png` when image dependencies are available
- `<slug>-evals.md` for all publication-report modes
- `<slug>-evals.html` as a browser-friendly companion when generated by the helper or requested for reviewer/gallery use

For McKinsey-style requests, prefer a slug suffix such as `mckinsey`, `consulting`, or `final`, and create a companion `<slug>-evals.md` using `evals.md`. Use the Evaluation Artifact Menu in `evals.md` to decide whether to also create focused Markdown/HTML evals such as page review, source fidelity, anti-pattern review, readability review, or gallery entries.

The helper defaults to publication-report output. For business diagnosis HTML inputs, it switches to a business publication report template and writes `<slug>-source.html` beside the output. For business overview Markdown inputs such as `总览.md`, it switches to `business-markdown-publication` mode and creates an eval beside the output. For non-business Markdown, it still uses publication-report mode with a documentation-optimized structure. If any route returns a generic booklet or hand-authored one-off converter, stop and fix the skill before accepting the PDF.

After running it, still inspect the preview yourself. If the preview shows browser headers, wrong pagination, or obvious layout problems, fix the HTML/CSS and rerun.

For skill regression work, choose representative Markdown/HTML inputs from `test-inputs.md`. After a skill update, run the updated skill through a fresh subagent or non-interactive Codex execution in a clean, clearly named workdir, with the updated skill path and raw input path passed explicitly. Generate the full review packet, let a human review the output, and feed repeated defects back into `anti-patterns.md`, `evals.md`, or the relevant script/template before accepting the change.

## Quality Bar

The output is successful only when:

- The PDF was created from a designed HTML page, not direct plain Markdown conversion.
- The design uses publication-report structure.
- For McKinsey-style or business-report requests, the design passes the `evals.md` rubric.
- The PDF opens and has a real page count.
- Text extraction works for at least the first few pages.
- A real cover preview exists.
- The cover preview has no Chrome default header/footer.
- The generated HTML and PDF paths are reported clearly.
- Existing earlier attempts are preserved unless the user asked to overwrite.

## Example Prompt

```text
Convert https://example.com/file.md into a polished PDF. First design a PDF-friendly web page, then print it to PDF, and show me a talk-html report.
```
