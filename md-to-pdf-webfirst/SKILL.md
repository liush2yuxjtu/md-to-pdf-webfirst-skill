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

## When To Use

Use this skill when the user asks for any of these:

- Convert a `.md` file, Markdown URL, or report HTML file to PDF.
- Make the PDF look better, more polished, more designed, or more readable.
- Use `frontend-design` for the PDF itself.
- Generate a PDF-friendly web page first, then convert to PDF.
- Produce evidence, preview images, hashes, page counts, or a `talk-html` report for the conversion.

If the user only wants a quick plain PDF, still consider this skill when quality matters or when the output will be shared.

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

For local HTML reports, keep the original file untouched and extract the report body into a new PDF-friendly HTML shell. Preserve source headings, tables, strong text, and business content. Do not print the original web preview directly unless it already passes the print-quality checks below.

Collect basic source metadata:

- line count
- byte size
- SHA-256 short hash
- heading counts
- code fence count

### 3. Design The PDF-Friendly Web Page

Treat the HTML as the PDF design surface.

Use a strong but print-safe visual direction. Good defaults:

- Editorial technical manual
- Archive/index card
- Dense but readable documentation booklet
- Monochrome with one or two sharp accent colors

Avoid generic web-app landing pages. This is not a marketing page; it is a printable document.

#### Default Technical Documentation Mode

Use this mode for ordinary Markdown docs such as tutorials, best-practices guides, API notes, workflow references, and code-heavy documentation:

- Prefer a documentation booklet aesthetic over a consulting deck aesthetic.
- Optimize for comprehension: section map, stable chapter hierarchy, readable paragraphs, strong code-block contrast, and CJK-safe cover/title layout.
- Use warm paper, restrained grid/rule details, and one or two accents when useful.
- Preserve authoring structure: Markdown pipe tables must render as real tables, MDX-style callouts must render as designed callout boxes, and thematic breaks must render as rules instead of raw syntax.
- Prevent page-bottom collisions: do not print fixed footers unless the content area reserves a real bottom safe zone, and do not leave headings or heading-callout pairs orphaned at the bottom of a page.
- Keep production notes out of reader-facing pages: cover pages must not show pipeline labels such as `DESIGNED HTML FIRST` or `PRINTED TO PDF WITH CHROME`; those belong in metadata or evals, not the PDF body.
- Parse Markdown inside blockquotes and documentation snippets enough to avoid raw authoring syntax such as `## Heading` leaking into the PDF.
- Distinguish runnable code from documentation excerpts. Fenced `markdown`, `mdx`, or prose examples should render as light documentation snippets, not black terminal/code blocks.
- Render business diagnosis chains, issue trees, and root-cause paths as light flow/chain components. Do not print `→`, `├──`, or `└──` narrative chains as black executable code blocks.
- Suppress source-acquisition preambles such as `Documentation Index`, `llms.txt`, and "discover all available pages" blocks when they appear before the real document title.
- Do not add executive-summary pages, issue maps, or McKinsey-style redline systems unless the user explicitly requests that tone.
- Review `anti-patterns.md`, especially the warning against applying a consulting skin to non-consulting documents.

#### McKinsey-Style Consulting Mode

Use this mode whenever the user asks for `麦肯锡 style`, `McKinsey style`, consulting style, board-report style, or executive strategy PDF polish. Treat it as McKinsey-inspired consulting presentation craft, not a branded clone:

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
python ~/.codex/skills/md-to-pdf-webfirst/scripts/md_to_pdf_webfirst.py \
  --input <markdown-file-or-url> \
  --slug <slug> \
  --out-dir outputs
```

The script creates:

- `<slug>.md`
- `<slug>.html`
- `<slug>.pdf`
- `<slug>-meta.json`
- `previews/<slug>-pdf-cover.png`

For McKinsey-style requests, prefer a slug suffix such as `mckinsey`, `consulting`, or `final`, and create a companion `<slug>-evals.md` using `evals.md`.

After running it, still inspect the preview yourself. If the preview shows browser headers, wrong pagination, or obvious layout problems, fix the HTML/CSS and rerun.

## Quality Bar

The output is successful only when:

- The PDF was created from a designed HTML page, not direct plain Markdown conversion.
- For McKinsey-style requests, the design passes the `evals.md` rubric.
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
