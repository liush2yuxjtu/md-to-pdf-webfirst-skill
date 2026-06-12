# Publication Report Mode

Use this module when the user asks for a McKinsey-style, MGI-style, research-institute-style, or publication-grade PDF.

Also use it automatically for local business diagnosis HTML reports when the source contains signals such as `RD`, `Hub`, `IYA`, `YoY`, `GIV`, `品类`, `诊断`, `行动`, and multiple source tables. The user does not need to say "McKinsey" for these inputs; business diagnosis reports should become reader-ready decision publications by default.

Publication report mode is stronger than ordinary consulting polish. It should create a complete research-report reading experience:

1. Full-bleed or image-led cover.
2. Cover metadata: title, subtitle, report date, and author/institution line.
3. Foreword / preface with deliberate whitespace, not a dense wall of text.
4. Designed table of contents with visible chapter span.
5. One-page executive summary.
6. Editorial hero or infographic page.
7. Alternating chapter openers, body pages, figure pages, and appendix pages.
8. Topic-relevant portrait/human/editorial visuals on the cover and between major chapters when assets or generation are available.
9. Stable running header/footer with report name, institution label, page number, source notes, and figure numbering.
10. Figures rebuilt from tables, not only copied tables.
11. References / methodology / related publications page when available.

For generated reports that do not provide a publisher, use `Win-Channel AI Research Institute` as the default institution label. Keep the label reader-facing; do not expose skill names, Codex runtime notes, API caveats, hashes, or generation failures in the PDF body.

## Required References

- `structure.md`: page sequence, running headers, figure system, source notes.
- `figure-system.md`: how to convert tables into figures.
- `imagegen.md`: generated image rules and fallbacks.
- `impeccable-design.md`: typography and color rules copied/adapted from the local impeccable skill.
- `../supporting-skills/imagegen-adapter.md`: local copy of the image generation workflow constraints that this skill can cite directly.
- `../supporting-skills/impeccable-publication-design.md`: local copy of the font, color, and readability rules used for publication PDFs.

## Output Standard

The result should feel like a Chinese business research publication, not a browser export or a slide deck pasted into PDF.

If the output looks like a lightly styled table dump, the publication mode failed even if the PDF has a cover, page count, and passing text extraction.
