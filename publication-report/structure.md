# Publication Structure Rules

## Page Rhythm

Alternate page jobs instead of printing one long stream:

- Cover with topic-relevant human/editorial visual, title, subtitle, date, and institution/authors
- Foreword / preface with intentional whitespace
- Designed table of contents with chapter spans
- One-page executive summary
- Infographic / editorial hero
- Chapter opener with portrait, human figure, or analytical editorial image when practical
- Body page
- Figure page
- Body page
- Figure page
- Appendix / references / related publications

Do not put five dense table/body pages in a row when the user asks for publication-grade output.
Do not leave a page mostly blank after a single table or short narrative block. Add evidence: a figure, heatmap, source-data excerpt, quantified callouts, or a clearly labeled implication box.
Do not use a plain centered-title cover, a plain bulleted contents page, or an unbroken prose preface when a report is intended to be publication-grade.

## Cover And Front Matter

The cover must establish the publication contract:

- topic-related human figure, portrait, field photograph, or restrained generated editorial visual
- main title and subtitle
- date or analysis period
- author/institution line; default to `Win-Channel AI Research Institute` when no publisher is supplied
- no source file paths, hashes, pipeline labels, or tool/process notes

The first front-matter pages should feel authored. Use an about/preface page with generous margins, a designed contents page, and a one-page summary that can stand alone.

## Chapter Interstitials

For long reports or multi-chapter business publications, separate chapters with an intentional opener. Use a topic-related portrait, human figure, line-art person, or photo/illustration crop when available. The opener should name the chapter, state the chapter question, and avoid becoming a blank spacer page.

## Running System

Every non-cover page should have:

- report name or shortened running title
- institution / publisher label
- page number
- section label when useful

Use normal-flow or safely reserved fixed headers/footers. Do not let running elements overlap content.

Reader-facing pages must not contain skill-development notes, pipeline labels, metadata references, tool failure messages, or instructions about Codex/API availability. Keep those details in metadata, evals, or handoff notes.

## Figure Discipline

Every figure must include:

- figure number such as `图 1`
- assertion title that states the judgment first
- visual evidence
- source note or data basis

Pattern:

```text
图 2：Oral、Hair、Fabric 是主要负增长压力源
Evidence visual
注：基于源报告表格重新绘制；金额单位按源表保留。
```

When the source provides only a few key numbers, do not print them as a sparse list or tiny table. Build a number-in-figure page: large key number, short implication, supporting mini-chart, and source note.

## Footnotes And Sources

Use concise source notes under figures and tables. If the source is generated from an HTML report, say so plainly:

```text
来源：贵州扬帆 2026年5月全维度业务诊断报告源 HTML；图表为 PDF webfirst 重新绘制。
```

When a claim would benefit from external credibility and the user allows browsing, web-search for a small number of relevant cases or public references and cite them. Do not invent cases. If browsing is unavailable, label evidence as source-only and avoid overstating credibility.

## Related Publications

If prior generated reports, gallery entries, or relevant public references are available, include a related-publications or references page. Use it to make the report feel like part of a research series, not an isolated conversion artifact.

## Chapter Spans

The table of contents should show chapter names and approximate page spans when final page numbers are known. If exact numbers are not available before print, use section-order spans in the generated metadata and update after verification when practical.
