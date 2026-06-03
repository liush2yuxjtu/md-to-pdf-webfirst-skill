---
name: md-to-pdf-webfirst
description: Convert Markdown files or Markdown URLs into polished PDFs by designing a PDF-friendly web page first, then printing that page to PDF. Use this skill whenever the user asks to convert .md or Markdown to PDF, wants a better-looking PDF, asks for frontend-design to improve PDF output, mentions "web first", "PDF-friendly web", "HTML then PDF", or wants proof/reporting around a Markdown-to-PDF workflow.
---

# Markdown to PDF, Web First

Use this skill to turn Markdown into a designed, readable PDF by following the final workflow:

1. Get the Markdown source.
2. Build a print-friendly HTML page from the Markdown.
3. Apply frontend design to the HTML as the PDF layout surface.
4. Print the HTML to PDF with Chrome.
5. Verify the PDF and create preview evidence.
6. If requested, report the result with `talk-html`.

This skill exists because direct Markdown-to-PDF conversion often produces plain text pages. The better route is to make the PDF layout as a web page first, then print that page.

## When To Use

Use this skill when the user asks for any of these:

- Convert a `.md` file or Markdown URL to PDF.
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

The HTML should include:

- cover page
- section map / table of contents
- clear heading hierarchy
- print-friendly A4 CSS
- code blocks with strong contrast
- readable lists and callouts
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
python /Users/liushiyuwin/.codex/skills/md-to-pdf-webfirst/scripts/md_to_pdf_webfirst.py \
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

After running it, still inspect the preview yourself. If the preview shows browser headers, wrong pagination, or obvious layout problems, fix the HTML/CSS and rerun.

## Quality Bar

The output is successful only when:

- The PDF was created from a designed HTML page, not direct plain Markdown conversion.
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
