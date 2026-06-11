# Impeccable Design Rules For Publication PDFs

This file copies and adapts the needed parts of the local `impeccable` skill for PDF publication design.

## Typography

- Pick fonts as a physical design decision, not a default. For Chinese publication PDFs, use a heavy serif/Song-style title face when available and a highly readable sans face for body/table text.
- Keep font families to at most three:
  - display/title
  - body/table
  - mono/numeric
- Use strong hierarchy through scale and weight. Body/table text must remain readable at A4 size.
- Body/list print floor: `>= 11px`.
- Normal table floor: `>= 10px`.
- Dense/wide table floor: `>= 9.5px`.
- Use `font-variant-numeric: tabular-nums` for metrics and tables.
- Use balanced or pretty wrapping on headings where supported.

Recommended macOS stacks:

```css
--font-display: "Songti SC", "STSong", "Noto Serif CJK SC", "Source Han Serif SC", serif;
--font-body: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
--font-brand: "Avenir Next Condensed", "Avenir Next", "Helvetica Neue", sans-serif;
--font-mono: "SF Mono", "Menlo", monospace;
```

## Color

- Choose color strategy before values. Publication reports should usually be restrained or committed, not rainbow.
- Use deep navy / ink as the dominant identity color, white as the reading surface, red/crimson as rare analytical emphasis, and cyan/teal only for secondary positive or contrast signals.
- Use OKLCH when authoring new design tokens.
- Body text contrast must pass WCAG AA in print-like preview.
- Do not use beige/cream as the default body background.
- Do not use generic purple-blue gradients.

Recommended tokens:

```css
--ink: oklch(17% 0.025 255);
--navy: oklch(23% 0.08 255);
--blue: oklch(43% 0.14 252);
--red: oklch(48% 0.18 25);
--teal: oklch(48% 0.12 185);
--paper: oklch(99% 0 0);
--soft: oklch(96% 0.006 255);
--line: oklch(86% 0.012 255);
```

## Layout

- Use imagery when the report is publication-grade. Zero imagery is a bug unless the user asks for no images.
- Avoid side-stripe cards. Use full borders, figure blocks, rules, or numbered exhibits instead.
- Avoid decorative shadows and oversized rounded cards.
- Build pages around a clear editorial job: answer, figure, evidence, implication.
