# Image Generation Rules

Use generated images when a publication-grade report needs editorial imagery and no approved local assets exist.

This workflow is available only inside Codex App sessions that expose the `imagegen` tool. Do not describe it as available for GPT-5.5 API calls or other runtimes unless that runtime has its own image-generation integration.

## What To Generate

- Cover hero: abstract or photographic editorial image related to the domain, preferably including a topic-relevant human figure or portrait-like subject when appropriate.
- Infographic accent: line-art people, operating network, channel map, or analytical scene.
- Section visual: restrained image or illustration that supports the chapter.
- Chapter interstitial: portrait, worker, customer, analyst, field scene, or line-art human composition that signals the chapter topic.

## Prompt Rules

- Ask for no text, no logos, and no readable brand names in generated images.
- Specify A4 portrait or wide banner aspect ratio.
- Use professional publication language: editorial, restrained, high contrast, deep navy, precise red analytical accents.
- Do not imitate a specific copyrighted report page. Use "consulting research publication" as style guidance, not brand cloning.
- Do not request a real named person's likeness unless the user supplies rights-cleared source imagery. Prefer generic topic-relevant people.
- Leave enough negative space for title overlays on covers, but do not generate blank filler.

## Fallback

If image generation fails, create a local raster or SVG asset using abstract geometry, line-art, and data-driven motifs. The fallback must still be an intentional visual asset, not a blank colored rectangle.

Keep generation failures, Codex-only caveats, and fallback notes out of reader-facing PDF pages. Put those details in metadata, evals, or the delivery note.

The `imagegen` workflow is a Codex App capability only. The PDF must never explain this limitation to readers. If the report is generated in a runtime without imagegen, use a designed local fallback and record the limitation in eval metadata.

## Verification

- Image appears in the PDF, not only HTML.
- Image is not blurred, cropped badly, or too dark for the text overlay.
- No generated fake text appears inside the image.
