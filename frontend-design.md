# Frontend Design Pass For PDF

Use this file when a PDF request also invokes `frontend-design`, asks for strong visual polish, or asks for McKinsey-style output that should feel more intentionally designed than a plain report printout.

The PDF surface is still a web page first. Design it like a production frontend whose final viewport is A4 paper.

## Design Direction

For McKinsey-style business PDFs, use a restrained but memorable direction:

**Boardroom redline system**

- White paper, charcoal type, sharp red accent, quiet gray rules, and occasional blue only for hierarchy.
- Asymmetric grid: a strong left or top redline on cover/front matter, then disciplined 12-column evidence pages.
- Executive answer visible in the first viewport/page, not buried after metadata.
- Tables treated as exhibits with labels, takeaways, and implications.
- A small number of memorable visual moves, repeated consistently: redline, exhibit eyebrow, issue map, operating agenda.

This is intentionally not a generic dashboard, marketing page, or decorative magazine layout.

## Typography

Avoid default-feeling stacks such as plain Arial, Roboto, Inter, or generic system-only declarations when the request explicitly invokes frontend design.

Good print-safe stacks on macOS:

```css
--font-display: "Avenir Next Condensed", "Avenir Next", "PingFang SC", "Microsoft YaHei", sans-serif;
--font-body: "Avenir Next", "PingFang SC", "Microsoft YaHei", sans-serif;
--font-mono: "SF Mono", "Menlo", monospace;
```

Use display typography for cover and section openers. Use body typography for tables and dense evidence.

## Layout Requirements

- Build a cover with a strong answer-first headline or conclusion, not just the report title.
- Add an executive summary page with metrics, so-what, and now-what.
- Add an issue map or operating agenda before the raw evidence.
- Convert major tables into exhibit blocks with `EXHIBIT`, `KEY TAKEAWAY`, and `IMPLICATION`.
- Keep visual density high but readable. Avoid card-heavy page layouts.
- Use exact A4 print CSS and inspect generated PDF previews, not only browser HTML.

## Avoid

- Decorative gradients, soft blobs, shadows, rounded-card dashboards, stock imagery, or playful illustration.
- A red bar pasted onto an otherwise unchanged report.
- Centered cover text with no decision content.
- Huge white gaps caused by over-aggressive page breaks.
- Tiny table text that only works in browser zoom, not in a real PDF preview.

## Frontend-Design Evaluation

A frontend-design pass is successful when:

- The PDF has a clear aesthetic point of view.
- The first page is memorable and answer-first.
- Typography choices are intentional and not generic.
- Repeated visual motifs support hierarchy and decision flow.
- Tables, issue maps, and action agendas feel purpose-built for the report.
- PDF previews prove the design survives print rendering.
