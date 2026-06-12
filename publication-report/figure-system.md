# Figure System

Rebuild figures from source tables whenever the source contains enough numeric structure.

## Recommended Figure Types

- Category health table -> sorted horizontal bar chart or lollipop chart.
- YoY gap table -> contribution bar chart or waterfall-like gap display.
- Hub x category matrix -> heatmap.
- Action plan table -> priority timeline or owner/action matrix.
- Diagnosis chain -> issue tree or flow map.
- One to six important numbers -> big-number / number-in-figure exhibit, not a sparse table.
- Percentage or share comparison -> unit-block display, stacked bar, or donut/pie when part-to-whole is the point.
- Current vs future, before vs after, or baseline vs target -> paired before/after frame.
- Ordered categories such as low / middle / high / xhigh / max -> bubble or circle-size matrix instead of repeated category labels.
- Geography by city/province/store region -> map or schematic map with small-to-large bubbles.

## Rules

- Keep the original table available somewhere if precision matters, but lead with a visual figure.
- Use one assertion title per figure. The title should say what the reader should conclude.
- Label values directly on bars or cells so the figure survives print.
- Do not rely on hover, tooltips, or interactivity.
- Highlight one key number in the left margin or as a large callout when the surrounding text needs an anchor.
- When using unit blocks, state the unit clearly, for example `1 square = 5M` or `1 block = 5 stores`.
- Use pie/donut charts only for part-to-whole relationships; do not use them for trend or ranking data.
- Use bubble sizes only when the size has a clear numeric or ordered meaning and a visible legend.
- Preserve enough white space around complex figures so labels do not collide, but avoid pages that are mostly blank.
- Use color semantically:
  - deep navy for baseline evidence
  - red/crimson for risk or negative gap
  - teal/green for resilience or positive performance
  - amber for watch items
- Include a source note below every figure.

## Anti-Patterns

- A table copied directly from source and called a figure.
- Figure labels too small to read.
- Color-only status encoding without labels.
- Decorative charts without data basis.
- Six numbers printed as six plain cards when an infographic would explain the relationship.
- A sparse page with a few raw metrics and no visual argument.
- Low/middle/high/xhigh/max values printed as text-only rows when circle size would make the pattern scannable.
- Geographic values printed as a table when a map or map-like bubble exhibit would reveal the spatial pattern.
