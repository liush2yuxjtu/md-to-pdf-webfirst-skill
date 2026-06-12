# Mandatory Eval Inputs For Skill Regression

Use this file as the required regression suite whenever `SKILL.md` changes. `test-inputs.md` is the larger candidate pool; this file is the always-run set.

The goal is one-shot reliability: after a skill update, the next ordinary user prompt should produce a reader-ready McKinsey-style publication PDF without hand repair.

## Non-Negotiable Rule

Every `SKILL.md` update must be followed by a fresh subagent or non-interactive Codex run for **all** inputs listed in the Mandatory Suite below.

Do not mark a `SKILL.md` change complete until the run produces:

- one clean output directory per input
- PDF, designed HTML, metadata, cover preview, contact sheet, eval Markdown, and eval HTML
- one consolidated regression eval board in Markdown
- one consolidated regression eval board in HTML
- human review notes or an explicit `PENDING HUMAN REVIEW` marker for every output

If the human review finds a visible display defect that the eval missed, the skill update is not done. Add the missed defect to `anti-patterns.md` and `evals.md`, update the implementation if needed, then rerun the full Mandatory Suite with a fresh output directory.

## Required Clean Context

For each input:

- Use a fresh subagent unless the user explicitly says not to use subagents.
- Work in a clear directory such as `/tmp/md-to-pdf-webfirst-regression/<yyyymmdd>-<suite-name>/`.
- Pass the updated skill path explicitly: `/Users/liushiyuwin/.codex/skills/md-to-pdf-webfirst/SKILL.md`.
- Pass the raw input path explicitly.
- Do not edit raw inputs.
- Do not hand-edit generated HTML/PDF to pass review.
- Do not reuse an earlier PDF, preview, contact sheet, or eval.

## Mandatory Suite

| ID | Input | Type | Required purpose | Human review focus |
| --- | --- | --- | --- | --- |
| `doc-long-cn` | `examples/zh-cn-best-practices/best-practices.md` | Markdown documentation | Long mixed Chinese/English documentation with callouts, tables, snippets, and headings. | CJK typography, raw Markdown leakage, code-vs-prose snippets, page breaks, publication-level cover. |
| `doc-long-en` | `examples/common-workflows/common-workflows.md` | Markdown documentation | Long English technical workflow document. | Documentation-publication rhythm, code/example semantics, section map, readable body pages. |
| `business-overview-md` | `examples/guizhou-yangfan-l1-overview/guizhou-yangfan-202605-l1-overview-webfirst-20260611-214738.md` | Business Markdown | Short decision document with IYA/category/action signals. | Auto-route to business publication mode, answer-first summary, figure/table/action pages, no blank filler. |
| `html-changelog` | `docs/changelog.html` | Generic HTML | Existing web/gallery page. | No raw `<!doctype`, `<style>`, CSS variables, DOM/CSS source, or generic booklet cover. |
| `html-landing` | `docs/index.html` | Generic HTML | GitHub Pages landing/gallery page with navigation chrome. | Strip nav/page chrome, preserve readable content, publication cover, no source leakage. |
| `rubric-md` | `evals.md` | Markdown rubric | Dense tables and hard-fail rubric text. | Table rendering, warning hierarchy, hard-fail visibility, no cramped pages. |
| `skill-md` | `SKILL.md` | Markdown instruction doc | The skill instructions themselves. | Long instruction readability, code blocks, lists, no raw authoring syntax, no weak generic cover. |

## Private Mandatory Add-On When Available

Run these in addition to the public suite when the files exist locally:

| ID | Input class | Example handle | Required purpose | Human review focus |
| --- | --- | --- | --- | --- |
| `business-diagnosis-html-private` | Business diagnosis HTML | `.../贵州扬帆2026年5月全维度业务诊断报告_20260610_165113.html` | Real business HTML report auto-routing. | Evidence pages, figures from tables, source-fidelity, no table dump, no tiny text. |
| `business-overview-md-private` | Business overview Markdown | local `总览.md` | Real short business overview auto-routing. | Compact decision-document quality, no filler, no blank tail pages. |

Private inputs must not be committed. Commit only generalized lessons.

## Required Eval Board

The consolidated eval board must include one row per input:

| Field | Required contents |
| --- | --- |
| Input ID | ID from the Mandatory Suite. |
| Source path | Raw input path. |
| Output dir | Fresh clean output directory. |
| PDF | Absolute PDF path. |
| Contact sheet | Absolute contact sheet path. |
| Eval | Absolute eval Markdown and HTML paths. |
| Mode | `publication-report`, `business-html-publication`, or `business-markdown-publication`. |
| Pages | PDF page count. |
| Hash | PDF SHA-256 short hash. |
| Hard-fail scan | Pass/fail for raw source leakage, Chrome headers, overlap/clipping, tiny text, blank pages, weak generic cover. |
| Human review | `PASS`, `FAIL`, or `PENDING HUMAN REVIEW`. |
| Follow-up | Anti-pattern/eval/script file to update if the human catches a miss. |

The HTML board should show cover previews/contact sheets as images when practical. The Markdown board should be readable in terminal or GitHub review.

## Acceptance Gate

A skill regression passes only when:

- every Mandatory Suite input produced a fresh full review packet
- the consolidated eval board exists in Markdown and HTML
- the eval board has no hard-fail rows
- human review has no unresolved display defect
- any human-found eval miss has been converted into `anti-patterns.md` and `evals.md`
- the suite was rerun after the fix that addressed the miss

Never accept a `SKILL.md` update based on one sample, a single cover preview, or an eval that has not been checked against human-visible output.
