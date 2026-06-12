# Test Inputs And Human Review Loop

Use this file to choose Markdown/HTML inputs for regression runs and to collect human review that improves future PDF output. The goal is not to maximize page count or score; the goal is to expose layout, readability, source-fidelity, and publication-quality failures before users see them.

## Required Review Packet Per Test Input

For every selected input, generate outputs from a clear context:

- Use a fresh subagent or non-interactive Codex execution when the regression follows a skill update.
- Use a clearly named clean workdir such as `/tmp/md-to-pdf-webfirst-regression/<date>-<slug>/`.
- Pass the updated skill path explicitly: `/Users/liushiyuwin/.codex/skills/md-to-pdf-webfirst/SKILL.md`.
- Pass the raw input path explicitly.
- Do not hand-fix the raw input, generated HTML, or generated PDF to make the review pass.
- Do not run from a crowded repo/worktree where stale outputs can be mistaken for fresh artifacts.

For every selected input, the fresh output folder must contain:

- `<slug>.html`
- `<slug>.pdf`
- `<slug>-meta.json`
- `<slug>-evals.md`
- `<slug>-evals.html`
- `previews/<slug>-pdf-cover.png`
- `previews/<slug>-contact-sheet.png` when image dependencies are available

When a human reviews the output, ask for comments in these buckets:

- Display defects: overlap, clipping, tiny type, blank pages, bad page breaks, unreadable tables, weak chart sizing.
- Reader readiness: whether the PDF feels like a publication report instead of a source dump.
- Evidence quality: whether conclusions have visible data/table/figure support.
- Source fidelity: whether headings, metrics, tables, code, callouts, and links survived conversion.
- Anti-patterns: whether any issue belongs in `anti-patterns.md`.
- Eval quality: whether `<slug>-evals.md/html` accurately caught or missed the problem.

Human comments should feed back into one of these places:

- `anti-patterns.md` for recurring visual or reasoning failures.
- `evals.md` for rubric/checklist gaps.
- `scripts/md_to_pdf_webfirst.py` for parser, routing, metadata, or generic publication-output defects.
- `scripts/business_html_publication.py` for business HTML diagnosis reports.
- `scripts/business_markdown_publication.py` for business overview Markdown.
- `publication-report/` for publication structure, figure, color, typography, image, or editorial-system guidance.

## Existing Repo Inputs

These files already exist in this skill repo and should remain safe to run in public regression tests.

| Input | Type | What it tests | Human review focus |
| --- | --- | --- | --- |
| `examples/common-workflows/common-workflows.md` | Markdown documentation | Long technical manual, sections, lists, code-ish workflow content. | Navigation, documentation-publication rhythm, code/example semantics, table of contents usefulness. |
| `examples/common-workflows/common-workflows.html` | Generated HTML | Browser-to-PDF stability for existing generated HTML. | Whether regenerated PDF preserves publication structure and avoids stale styling regressions. |
| `examples/zh-cn-best-practices/best-practices.md` | Markdown documentation | Chinese/English mixed docs, pipe tables, callouts, code/documentation snippets, thematic breaks. | Raw Markdown leakage, CJK typography, code-vs-prose snippet classification, footer/page-boundary collisions. |
| `examples/zh-cn-best-practices/best-practices.html` | Generated HTML | Existing documentation HTML regression. | Whether HTML input still prints as a polished report and not a browser dump. |
| `examples/zh-cn-best-practices/skill-comparison/old-skill/best-practices-old-skill-33d3321-20260611.md` | Markdown old-run fixture | Historical comparison against old skill behavior. | Confirm current skill does not reintroduce old failures. |
| `examples/zh-cn-best-practices/skill-comparison/old-skill/best-practices-old-skill-33d3321-20260611.html` | HTML old-run fixture | Historical generated HTML. | Identify which visual defects were inherited from old HTML and should be repaired. |
| `examples/zh-cn-best-practices/skill-comparison/new-skill/best-practices-new-skill-20260611.md` | Markdown regression fixture | First new-skill attempt. | Confirm callout/tag, table, and cover-label anti-patterns stay fixed. |
| `examples/zh-cn-best-practices/skill-comparison/new-skill/best-practices-new-skill-20260611.html` | HTML regression fixture | First new-skill generated HTML. | Compare PDF rendering defects against later attempts. |
| `examples/zh-cn-best-practices/skill-comparison/new-skill-v2/best-practices-new-skill-v2-20260611.md` | Markdown regression fixture | Second attempt after anti-pattern fixes. | Confirm source preambles, blockquotes, and prose snippets remain fixed. |
| `examples/zh-cn-best-practices/skill-comparison/new-skill-v2/best-practices-new-skill-v2-20260611.html` | HTML regression fixture | Second generated HTML. | Human review of persistent heading/callout visual defects. |
| `examples/zh-cn-best-practices/skill-comparison/new-skill-v3/best-practices-new-skill-v3-20260611.md` | Markdown regression fixture | Third attempt after preamble suppression. | Ensure documentation mode stays publication-ready without consulting skin. |
| `examples/zh-cn-best-practices/skill-comparison/new-skill-v3/best-practices-new-skill-v3-20260611.html` | HTML regression fixture | Third generated HTML. | Confirm current helper can supersede v3 quality. |
| `examples/guizhou-yangfan-l1-overview/guizhou-yangfan-202605-l1-overview-webfirst-20260611-214738.md` | Business overview Markdown | Short Chinese business overview with IYA/category/action signals. | Auto-route to business-markdown-publication, answer-first pages, rebuilt figure, source table, action page, no blank filler. |
| `examples/guizhou-yangfan-l1-overview/guizhou-yangfan-202605-l1-overview-webfirst-20260611-214738.html` | Business overview HTML | Existing generated business overview HTML. | Whether reprocessing HTML preserves decision-document quality. |
| `examples/prompts.md` | Short Markdown prompt catalog | Very short source with little content. | Compact publication report without fake filler or empty pages. |
| `examples/zh-cn-best-practices/skill-comparison/README.md` | Markdown comparison table | Small table-heavy project note. | Real table rendering, link readability, and no over-designed cover. |
| `README.md` | Markdown product docs | Public README, product positioning, links. | Documentation-publication clarity and concise front matter. |
| `CHANGELOG.md` | Markdown changelog | Release history and bullet-heavy timeline. | Changelog/gallery style, chronology, compact but readable bullets. |
| `PRODUCT.md` | Markdown product brief | Product-positioning document. | Executive summary, audience clarity, and publication rhythm without overclaiming. |
| `SKILL.md` | Markdown skill instructions | Long operational instruction doc. | Dense instruction readability, headings, code blocks, and no raw authoring syntax. |
| `anti-patterns.md` | Markdown checklist | Long checklist and correction patterns. | Checklist hierarchy, examples, warning density, page breaks. |
| `evals.md` | Markdown rubric | Evaluation rubric with tables and templates. | Table rendering, template formatting, hard-fail visibility. |
| `frontend-design.md` | Markdown design guidance | Design instruction document. | Visual hierarchy and design-token readability. |
| `publication-report/README.md` | Markdown module docs | Publication-report module entry. | Cross-reference clarity and concise module presentation. |
| `publication-report/structure.md` | Markdown structure guidance | Report architecture rules. | Chapter/section-page rhythm, no orphaned headings. |
| `publication-report/figure-system.md` | Markdown figure guidance | Exhibit and figure rules. | Figure/table examples and exhibit labels. |
| `publication-report/imagegen.md` | Markdown image guidance | Image-generation guidance. | Clear caveats without reader-facing tool noise. |
| `publication-report/impeccable-design.md` | Markdown typography/color guidance | Typography and color system. | Font hierarchy, color contrast, and palette restraint. |
| `supporting-skills/imagegen-adapter.md` | Markdown adapter docs | Supporting skill adapter. | Short technical doc handling. |
| `supporting-skills/impeccable-publication-design.md` | Markdown adapter docs | Typography/color adapter. | Dense design guidance readability. |
| `references/business-html-report-regression.md` | Markdown regression reference | Private business HTML lesson without private source. | Whether regression lessons become visible in eval and anti-pattern review. |
| `docs/index.html` | GitHub Pages HTML | Landing/gallery HTML. | HTML input handling and whether page chrome becomes inappropriate PDF content. |
| `docs/changelog.html` | GitHub Pages HTML | Changelog/gallery page HTML. | Gallery/card content extraction, McKinsey-style publication cover, and hard fail if raw `<!doctype` / `<style>` / CSS source prints as PDF text. |

## Private Or Local Regression Inputs

Do not commit these files into the public skill repo. Use them locally as high-value regression tests and commit only generalized lessons.

| Input class | Example handle | What it tests | Required human review |
| --- | --- | --- | --- |
| Business diagnosis HTML | `.../贵州扬帆2026年5月全维度业务诊断报告_20260610_165113.html` | Business HTML auto-routing to `business-html-publication`. | Full contact sheet, evidence pages, source-fidelity spot checks, no table-dump pass. |
| Business overview Markdown | Local `总览.md` files with IYA/PS/category/action signals. | Business Markdown auto-routing to `business-markdown-publication`. | Compact publication rhythm, no blank filler, figure/table/action page quality. |
| Previously bad PDFs converted back to review notes | User-annotated PDF comments and screenshots. | Anti-pattern extraction. | Add generalizable defects to `anti-patterns.md`, not one-off patches to raw outputs. |
| McKinsey/MGI reference PDFs | Public reference reports only as visual/style reference. | Publication density, section rhythm, editorial hero, figures, footnotes. | Use inspiration for structure and quality bar, not branded cloning. |

## Test Inputs To Add

Add synthetic files under `examples/regression-inputs/` when a failure appears more than once.

| Proposed file | Type | Failure class it should test |
| --- | --- | --- |
| `examples/regression-inputs/callout-tags.md` | Markdown | `<Callout>`, `</Callout>`, MDX tags, blockquote parsing, thematic breaks. |
| `examples/regression-inputs/wide-tables.md` | Markdown | Wide and dense tables without tiny typography. |
| `examples/regression-inputs/code-vs-doc-snippets.md` | Markdown | Distinguish executable code from prose/Markdown examples. |
| `examples/regression-inputs/cjk-long-headings.md` | Markdown | Chinese title wrapping, heavy headlines, no overlap. |
| `examples/regression-inputs/tail-appendix.md` | Markdown | Avoid mostly blank final pages. |
| `examples/regression-inputs/business-overview-mini.md` | Markdown | Short decision document with IYA/PS/category/action signals. |
| `examples/regression-inputs/business-diagnosis-mini.html` | HTML | Public anonymized business HTML shape with tables and diagnosis sections. |
| `examples/regression-inputs/gallery-page.html` | HTML | GitHub Pages/gallery page print handling. |
| `examples/regression-inputs/browser-chrome-noise.html` | HTML | Suppress web navigation/footer/sidebar from PDF body. |

## Human Review Cadence

Run this loop before accepting a skill change:

1. Pick at least one documentation Markdown input.
2. Pick at least one business Markdown input.
3. Pick at least one HTML input.
4. Start a fresh subagent or non-interactive Codex run in a clean, clearly named workdir.
5. Give that run only the updated skill path, the selected raw input path, and the output directory.
6. Generate PDF, metadata, preview/contact sheet, `<slug>-evals.md`, and `<slug>-evals.html`.
7. Ask a human reviewer to mark display defects and eval misses.
8. Convert repeated or severe comments into `anti-patterns.md` and `evals.md`.
9. Update scripts/templates only after the anti-pattern/eval wording is clear.
10. Rerun the same input through a fresh subagent or non-interactive Codex run in a new output directory and compare contact sheets.

Minimum acceptance: the eval must catch the human's top visible concern. If the human says "this looks bad" and the eval still passes perfectly, the eval is wrong and must be fixed before the template is called done.
