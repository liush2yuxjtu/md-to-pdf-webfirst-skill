# Skill Comparison: best-practices.md

Source Markdown:

`examples/zh-cn-best-practices/best-practices.md`

Skill locations found in this Git repo:

- Current/new skill: `md-to-pdf-webfirst/SKILL.md`
- Current/new script: `md-to-pdf-webfirst/scripts/md_to_pdf_webfirst.py`
- Fix applied: default Markdown docs now use technical-documentation mode, not a consulting redline skin
- Fix applied: Markdown pipe tables, MDX-style callouts, and thematic breaks now render as PDF components instead of raw source syntax
- Fix applied: print pagination now hides decorative fixed footers and keeps subsection headings with their first content block
- Fix applied: v2 removes reader-facing build pipeline labels, parses Markdown inside blockquotes, and renders documentation snippets separately from executable code blocks
- Fix applied: v3 suppresses source-acquisition `Documentation Index` / `llms.txt` preambles before the real title
- Old skill/script source: Git commit `33d3321` (`Fix Pages example links`)

## Outputs

| Run | Skill version | PDF | Pages | First 3 pages text | PDF SHA-256 short |
| --- | --- | --- | ---: | ---: | --- |
| New skill v3 | `HEAD` / current `main` | `new-skill-v3/best-practices-new-skill-v3-20260611.pdf` | 19 | 1,089 chars | `d1cc5625ca6d333a` |
| New skill v2 | `HEAD` / current `main` | `new-skill-v2/best-practices-new-skill-v2-20260611.pdf` | 19 | 1,261 chars | `b196a30f2f6bf4cc` |
| New skill | `HEAD` / current `main` | `new-skill/best-practices-new-skill-20260611.pdf` | 20 | 1,323 chars | `3b1d17f64704f515` |
| Old skill | `33d3321` | `old-skill/best-practices-old-skill-33d3321-20260611.pdf` | 20 | 1,506 chars | `9797dd3208f9c72a` |

Each run also includes the generated HTML, metadata JSON, copied Markdown source, and PDF cover preview under its folder.
