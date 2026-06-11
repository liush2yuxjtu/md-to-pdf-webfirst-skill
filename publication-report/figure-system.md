# Figure System

Rebuild figures from source tables whenever the source contains enough numeric structure.

## Recommended Figure Types

- Category health table -> sorted horizontal bar chart or lollipop chart.
- YoY gap table -> contribution bar chart or waterfall-like gap display.
- Hub x category matrix -> heatmap.
- Action plan table -> priority timeline or owner/action matrix.
- Diagnosis chain -> issue tree or flow map.

## Rules

- Keep the original table available somewhere if precision matters, but lead with a visual figure.
- Use one assertion title per figure. The title should say what the reader should conclude.
- Label values directly on bars or cells so the figure survives print.
- Do not rely on hover, tooltips, or interactivity.
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
