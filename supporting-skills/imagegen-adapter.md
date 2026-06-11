# Imagegen Adapter for Publication PDFs

Use this local adapter when a report asks for generated imagery, editorial heroes, visual chapter openers, or infographic assets.

This adapter is for the Codex App environment only. Do not assume the same `imagegen` tool is available to GPT-5.5 API calls or other non-Codex runtimes. API-facing usage must either provide its own image-generation integration or use a non-imagegen fallback.

## Required behavior

- Attempt image generation for at least one major editorial asset when the user explicitly requests imagegen.
- Prefer assets with no embedded words, logos, UI chrome, fake report titles, or fake company names; all final text must stay in HTML/CSS so it is editable and crisp in PDF.
- Generate or place images as local files under the output artifact folder, for example `assets/cover-hero.png`.
- If image generation fails, create an intentional fallback raster/SVG/PNG asset and disclose the fallback in metadata or eval artifacts. Do not silently ship a blank hero.
- Use images for structure, not decoration: cover hero, foreword/section visual, infographic backdrop, or simple line-art human/business system illustration.
- Never print Codex-only notes, API limitations, generation failures, tool names, or fallback explanations in reader-facing PDF pages unless the user explicitly asks for a technical production appendix.

## Prompt Pattern

Ask for:

- documentary or editorial business-report imagery,
- abstracted retail/distribution networks,
- restrained navy/ink/red/teal palette,
- high contrast with clean negative space,
- no text and no logos.

Avoid:

- generic glowing gradients,
- cartoon dashboards,
- dense text inside the image,
- stock-photo people smiling at laptops,
- visual metaphors that do not connect to the report evidence.
