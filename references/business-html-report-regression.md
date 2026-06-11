# Business HTML Report Regression Reference

Use this reference when a plain prompt such as:

```text
$md-to-pdf-webfirst file:///.../贵州扬帆2026年5月全维度业务诊断报告_20260610_165113.html
```

produces a PDF that is technically valid but not reader-ready.

## Regression Observed

Local bad artifact:

```text
/Users/liushiyuwin/.codex/worktrees/f5e0/win-brain-contribute/outputs/guizhou-yangfan-2026-05-webfirst.pdf
```

Observed properties:

- 15 pages.
- Clean cover and tables, but no editorial/research-framework visual.
- No true publication rhythm: cover, foreword, TOC, executive answer, infographic, figure pages, chapter openers, evidence pages, references.
- Heavy source-table flow; many pages read like a styled HTML dump.
- Eval claimed `14 / 14 Pass`, but the contact sheet did not support that score.

## Skill Lesson

Business diagnosis HTML is not ordinary documentation. If the source contains RD, Hub, IYA, YoY, GIV, 品类, 诊断, 行动, and many tables, the default route must be publication-report mode even when the user does not explicitly ask for McKinsey/MGI style.

## Required Fix Pattern

- Detect business-report HTML before Markdown parsing.
- Preserve the source as `<slug>-source.html`.
- Generate a reader-ready publication shell.
- Rebuild at least one figure from tables before long table sections.
- Include a research-framework or editorial visual page.
- Add a full contact sheet or representative page previews to the eval evidence.
- Fail the eval if the contact sheet looks like a table dump, even when text extraction and page count pass.

## Privacy Note

Do not commit private business PDFs or source HTML into this public skill repository. Keep private examples as local artifacts and commit only generalized lessons, checks, and non-sensitive references.
