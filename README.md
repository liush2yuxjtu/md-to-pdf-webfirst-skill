# md-to-pdf-webfirst

A Codex skill for converting Markdown files or Markdown URLs into polished PDFs by designing a PDF-friendly HTML document first, then printing that HTML to PDF with Chrome.

## What it does

The final workflow is:

1. Fetch or read Markdown.
2. Generate a print-friendly A4 HTML document.
3. Apply frontend design to the HTML as the PDF layout surface.
4. Print the HTML to PDF with headless Chrome.
5. Verify page count and text extraction.
6. Generate a real PDF cover preview.

## Install

Copy the skill directory into your Codex skills folder:

```bash
cp -R md-to-pdf-webfirst ~/.codex/skills/md-to-pdf-webfirst
```

## Run the helper script

```bash
python ~/.codex/skills/md-to-pdf-webfirst/scripts/md_to_pdf_webfirst.py \
  --input https://code.claude.com/docs/en/common-workflows.md \
  --slug common-workflows-webfirst \
  --out-dir outputs
```

## Outputs

The script creates:

- `<slug>.md`
- `<slug>.html`
- `<slug>.pdf`
- `<slug>-meta.json`
- `previews/<slug>-pdf-cover.png`

## Examples

This repository includes real generated examples:

- [`examples/zh-cn-best-practices/best-practices.md`](examples/zh-cn-best-practices/best-practices.md)
- [`examples/zh-cn-best-practices/best-practices.pdf`](examples/zh-cn-best-practices/best-practices.pdf)
- [`examples/common-workflows/common-workflows.md`](examples/common-workflows/common-workflows.md)
- [`examples/common-workflows/common-workflows.pdf`](examples/common-workflows/common-workflows.pdf)

Landing page:

https://liush2yuxjtu.github.io/md-to-pdf-webfirst-skill/

## Requirements

- Python with `pypdf`
- Google Chrome, Chromium, or Microsoft Edge for headless PDF printing
- macOS `qlmanage` for cover preview generation, optional

## Notes

This skill is designed for shared, readable PDFs. If the PDF quality matters, prefer this web-first workflow over direct plain Markdown-to-PDF conversion.
