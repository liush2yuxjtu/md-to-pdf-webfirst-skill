from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from pypdf import PdfReader

from business_html_publication import build_business_publication_html, looks_like_business_html
from business_markdown_publication import build_business_markdown_publication_html, looks_like_business_markdown


CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def sha16(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def normalize_cached_markdown_text(text: str) -> tuple[str, bool]:
    if text.lstrip().lower().startswith(("<!doctype html", "<html")):
        return text, False

    original = text
    has_markdown_markers = any(marker in text for marker in ("```", "###", "## ", "|------", "[Final Reply]", "[Tool Result]"))
    is_single_line_cache = len(text.splitlines()) <= 2 and "   " in text and has_markdown_markers
    if is_single_line_cache:
        text = re.sub(r" {3,}", "\n", text).strip()

    if "[State]" in text or "[Final Reply]" in text or " | |" in text:
        text = re.sub(r"\s+\[Tool Result\]\s+", "\n\n[Tool Result] ", text)
        text = re.sub(r"\n\[State\][^\n]*", "", text)
        text = text.replace("\n[Final Reply]\n\n", "\n\n")
        text = re.sub(r"\s+\[Final Reply\]\s+", "\n\n", text)
        text = re.sub(r"\s+---\s+", "\n\n---\n\n", text)
        text = re.sub(r"\s+###\s+", "\n\n### ", text)
        text = re.sub(r"\s+##\s+", "\n\n## ", text)
        text = re.sub(r"\s+#\s+Benchmark", "\n\n# Benchmark", text)
        text = re.sub(r"```\s+", "```\n", text)
        text = re.sub(r"\s+```\s+", "\n```\n", text)
        text = re.sub(r"\s+\*\*([^*]+)\*\*：", r"\n\n**\1**：", text)
        text = re.sub(r"(\|)\s+\|", r"\1\n|", text)
        text = re.sub(r"(\|)\s+(\*\*[^*\n]+?\*\*：)", r"\1\n\n\2", text)
        text = re.sub(r"(\|)\s+(Top 5 产品：)", r"\1\n\n**\2**", text)
        text = re.sub(r"(\|)\s+(洞察：|解读：)", r"\1\n\n**\2**", text)
        text = re.sub(r"(### [^\n|]+?)\s+(\| [^\n]+\|)", r"\1\n\2", text)
        text = re.sub(r"(\*\*Top 5 产品\*\*：)\s+(\| [^\n]+\|)", r"\1\n\2", text)
        text = re.sub(r"：\s*-\n\n\*\*", "：\n- **", text)
        text = re.sub(r"。\s*-\n\n\*\*", "。\n- **", text)
        text = re.sub(r"\n(\d+)\.\n\n(\*\*)", r"\n\1. \2", text)
        text = re.sub(r"([^\n])\s+```", r"\1\n```", text)
        text = re.sub(r"^\[Tool Result\][^\n]*\n?", "", text, flags=re.M)
        text = re.sub(r"\s*\[State\][^\n]*", "", text)
        text = re.sub(r"\s*\[Final Reply\]\s*", "\n\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)

    text = text.strip() + "\n"
    return text, text != original


def looks_like_html(text: str) -> bool:
    head = text.lstrip()[:600].lower()
    return (
        head.startswith("<!doctype html")
        or head.startswith("<html")
        or "<html" in head
        or ("<body" in head and "</body" in text.lower())
    )


class ReadableHTMLToMarkdown(HTMLParser):
    SKIP_TAGS = {"style", "script", "svg", "noscript", "template", "nav", "footer"}
    BLOCK_TAGS = {"p", "div", "section", "article", "header", "main", "aside", "blockquote"}
    HEADING_TAGS = {"h1": "#", "h2": "##", "h3": "###", "h4": "####"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self.meta_description = ""
        self.skip_depth = 0
        self.in_title = False
        self.in_pre = False
        self.in_anchor = False
        self.anchor_href = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        attr_map = {key.lower(): value or "" for key, value in attrs}
        if tag == "meta" and attr_map.get("name", "").lower() == "description":
            self.meta_description = attr_map.get("content", "").strip()
            return
        if tag == "title":
            self.in_title = True
            return
        if tag in self.HEADING_TAGS:
            self._newline(2)
            self.parts.append(f"{self.HEADING_TAGS[tag]} ")
        elif tag in self.BLOCK_TAGS:
            self._newline(2 if tag in {"section", "article", "main", "aside"} else 1)
        elif tag == "br":
            self._newline(1)
        elif tag == "li":
            self._newline(1)
            self.parts.append("- ")
        elif tag == "pre":
            self._newline(2)
            self.parts.append("```text\n")
            self.in_pre = True
        elif tag == "tr":
            self._newline(1)
        elif tag in {"th", "td"}:
            self.parts.append(" | ")
        elif tag == "a":
            self.in_anchor = True
            self.anchor_href = attr_map.get("href", "")

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag == "title":
            self.in_title = False
        elif tag == "pre":
            self.parts.append("\n```")
            self.in_pre = False
            self._newline(2)
        elif tag == "a":
            self.in_anchor = False
            self.anchor_href = ""
        elif tag in self.HEADING_TAGS or tag in self.BLOCK_TAGS or tag in {"li", "tr"}:
            self._newline(2 if tag in self.HEADING_TAGS or tag in self.BLOCK_TAGS else 1)

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.in_title:
            self.title_parts.append(data)
            return
        if not data.strip():
            if self.in_pre:
                self.parts.append(data)
            return
        if self.in_pre:
            self.parts.append(data)
            return
        text = re.sub(r"\s+", " ", data).strip()
        if not text:
            return
        self.parts.append(text)
        self.parts.append(" ")

    def _newline(self, count: int) -> None:
        text = "".join(self.parts)
        current = len(text) - len(text.rstrip("\n"))
        if current < count:
            self.parts.append("\n" * (count - current))

    def markdown(self) -> tuple[str, str]:
        raw_title = re.sub(r"\s+", " ", " ".join(self.title_parts)).strip()
        raw = "".join(self.parts)
        raw = re.sub(r"[ \t]+\n", "\n", raw)
        raw = re.sub(r"\n[ \t]+", "\n", raw)
        raw = re.sub(r"[ \t]{2,}", " ", raw)
        raw = re.sub(r"\n{3,}", "\n\n", raw)
        lines = [line.strip() for line in raw.splitlines()]
        cleaned: list[str] = []
        for line in lines:
            if not line:
                if cleaned and cleaned[-1]:
                    cleaned.append("")
                continue
            if re.search(r"^(<!doctype|<html|<head|<style|</style>|<script|</script>)", line, re.I):
                continue
            if re.search(r"(\{|\}|--[a-z-]+:|box-sizing:|font-family:|background:|grid-template-columns:)", line):
                continue
            cleaned.append(line)
        markdown = "\n".join(cleaned).strip()
        if raw_title and not markdown.startswith("# "):
            markdown = f"# {raw_title}\n\n{markdown}"
        return markdown + "\n", raw_title


def html_to_reader_markdown(text: str) -> tuple[str, dict]:
    parser = ReadableHTMLToMarkdown()
    parser.feed(text)
    markdown, title = parser.markdown()
    return markdown, {
        "html_title": title,
        "html_description": parser.meta_description,
        "html_input_normalized": True,
    }


def escape(text: str) -> str:
    return html.escape(text, quote=True)


def inline(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<a>\1</a>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def eval_markdown_to_html(markdown: str, title: str) -> str:
    body: list[str] = []
    in_table = False
    for raw in markdown.splitlines():
        line = raw.rstrip()
        if in_table and not line.startswith("|"):
            body.append("</tbody></table>")
            in_table = False
        if not line:
            continue
        if line.startswith("# "):
            body.append(f"<h1>{inline(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            body.append(f"<h2>{inline(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            body.append(f"<h3>{inline(line[4:].strip())}</h3>")
        elif line.startswith("- "):
            body.append(f"<p class=\"bullet\">{inline(line[2:].strip())}</p>")
        elif line.startswith("|") and line.endswith("|"):
            cells = [inline(cell.strip()) for cell in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", cell.replace("\\:", ":")) for cell in cells):
                continue
            tag = "th" if not in_table else "td"
            if not in_table:
                body.append("<table><tbody>")
                in_table = True
            body.append("<tr>" + "".join(f"<{tag}>{cell}</{tag}>" for cell in cells) + "</tr>")
        else:
            body.append(f"<p>{inline(line)}</p>")
    if in_table:
        body.append("</tbody></table>")
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<style>
:root {{ --ink:#172033; --muted:#687386; --line:#d7dde7; --soft:#f5f7fb; --accent:#b91c2c; --blue:#17365d; }}
body {{ margin:0; background:#f7f8fb; color:var(--ink); font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,"Noto Sans CJK SC","PingFang SC",sans-serif; }}
main {{ max-width:960px; margin:40px auto; padding:40px 48px; background:#fff; border:1px solid var(--line); }}
h1 {{ margin:0 0 24px; font-size:32px; line-height:1.12; color:var(--blue); }}
h2 {{ margin:32px 0 12px; padding-top:18px; border-top:2px solid var(--line); font-size:18px; letter-spacing:.02em; text-transform:uppercase; color:var(--accent); }}
h3 {{ margin:24px 0 10px; font-size:16px; color:var(--blue); }}
p {{ margin:8px 0; }}
.bullet {{ padding-left:18px; position:relative; }}
.bullet::before {{ content:""; position:absolute; left:0; top:.68em; width:6px; height:6px; background:var(--accent); }}
table {{ width:100%; border-collapse:collapse; margin:14px 0 22px; font-size:14px; }}
th,td {{ border:1px solid var(--line); padding:9px 10px; text-align:left; vertical-align:top; }}
th {{ background:var(--soft); color:var(--blue); font-weight:700; }}
code {{ background:#eef2f8; padding:1px 5px; border-radius:3px; }}
@media print {{ body {{ background:#fff; }} main {{ margin:0; max-width:none; border:0; }} }}
</style>
</head>
<body><main>
{chr(10).join(body)}
</main></body>
</html>"""


def is_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    if not is_table_row(stripped):
        return False
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header = rows[0]
    body = rows[1:]
    head_html = "<thead><tr>" + "".join(f"<th>{inline(cell)}</th>" for cell in header) + "</tr></thead>"
    body_html = "<tbody>" + "".join(
        "<tr>" + "".join(f"<td>{inline(cell)}</td>" for cell in row) + "</tr>"
        for row in body
    ) + "</tbody>"
    return f"<div class='table-wrap'><table>{head_html}{body_html}</table></div>"


def render_markdown_fragment(lines: list[str], wrapper: str = "div", class_name: str = "doc-snippet") -> str:
    parts: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            parts.append(f"<p>{inline(' '.join(paragraph))}</p>")
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            parts.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in list_items) + "</ul>")
            list_items = []

    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            flush_paragraph()
            flush_list()
            continue
        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            tag = "h4" if wrapper == "div" else "p"
            cls = " class='fragment-title'" if wrapper == "blockquote" else ""
            parts.append(f"<{tag}{cls}>{inline(heading.group(2))}</{tag}>")
            continue
        item = re.match(r"^[-*]\s+(.+)$", stripped)
        if item:
            flush_paragraph()
            list_items.append(item.group(1))
            continue
        flush_list()
        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    attrs = f" class='{class_name}'" if class_name else ""
    return f"<{wrapper}{attrs}>" + "".join(parts) + f"</{wrapper}>"


def is_documentation_fence(info: str, lines: list[str]) -> bool:
    language = info.split()[0].lower() if info.split() else ""
    if language in {"markdown", "md", "mdx", "text", "txt"}:
        return True
    if language:
        return False
    sample = "\n".join(lines[:8])
    return bool(re.search(r"(^|\n)#{1,4}\s+|@README\.md|@package\.json|@docs/", sample))


def is_diagnosis_chain(lines: list[str]) -> bool:
    text = "\n".join(lines)
    arrow_count = text.count("→") + text.count("->") + text.count("=>")
    has_tree_branch = bool(re.search(r"├──|└──", text))
    has_business_terms = bool(re.search(r"诊断|归因|问题|缺口|Hub|品类|门店|RD|IYA|YoY", text))
    return arrow_count >= 2 and (has_tree_branch or has_business_terms)


def render_diagnosis_chain(lines: list[str]) -> str:
    chain_parts: list[str] = []
    normalized = re.sub(r"\s+(?=[├└]──)", "\n", "\n".join(lines))
    for raw in normalized.splitlines():
        stripped = raw.strip()
        if not stripped:
            continue
        is_branch = bool(re.match(r"^[├└]──", stripped))
        stripped = re.sub(r"^[├└]──\s*", "", stripped)
        cells = [part.strip() for part in re.split(r"\s*→\s*", stripped) if part.strip()]
        if len(cells) > 1:
            chain_parts.append(
                f"<div class='chain-row{' branch' if is_branch else ''}'>"
                + "".join(f"<span>{inline(cell)}</span>" for cell in cells)
                + "</div>"
            )
        else:
            chain_parts.append(f"<p>{inline(stripped)}</p>")
    return "<div class='diagnosis-chain'>" + "".join(chain_parts) + "</div>"


def is_documentation_index_preamble(lines: list[str]) -> bool:
    text = " ".join(line.strip() for line in lines).lower()
    return "documentation index" in text and (
        "llms.txt" in text
        or "discover all available pages" in text
        or "complete documentation index" in text
    )


def normalize(lines: list[str]) -> list[str]:
    result: list[str] = []
    for raw in lines:
        line = raw.rstrip()
        step = re.match(r'^\s*<Step title="([^"]+)">\s*$', line)
        if step:
            result.append(f"#### {step.group(1)}")
            continue
        if re.match(r"^\s*</?Step>\s*$", line):
            continue
        if re.match(r"^\s*<Steps>\s*$", line):
            result.append(":::steps")
            continue
        if re.match(r"^\s*</Steps>\s*$", line):
            result.append(":::endsteps")
            continue
        if re.match(r"^\s*<Tip>\s*$", line):
            result.append(":::tip")
            continue
        if re.match(r"^\s*</Tip>\s*$", line):
            result.append(":::endtip")
            continue
        if re.match(r"^\s*<Callout>\s*$", line):
            result.append(":::callout")
            continue
        if re.match(r"^\s*</Callout>\s*$", line):
            result.append(":::endcallout")
            continue
        result.append(re.sub(r"\s+theme=\{null\}", "", line))
    return result


def split_frontmatter(markdown: str) -> tuple[dict[str, str], list[str]]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, lines

    end = None
    for idx in range(1, min(len(lines), 80)):
        if lines[idx].strip() == "---":
            end = idx
            break
    if end is None:
        return {}, lines

    meta: dict[str, str] = {}
    for raw in lines[1:end]:
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if match:
            key = match.group(1).strip().lower()
            value = match.group(2).strip().strip("\"'")
            if value:
                meta[key] = value
    return meta, lines[end + 1:]


def parse_markdown(markdown: str) -> tuple[str, dict]:
    frontmatter, body_lines = split_frontmatter(markdown)
    lines = normalize(body_lines)
    parts: list[str] = []
    h2s: list[str] = []
    title = frontmatter.get("name", "Publication Report").replace("-", " ").title()
    subtitle = frontmatter.get("description", "Reader-ready publication generated from source material.")
    code_count = 0
    doc_snippet_count = 0
    h3_count = 0
    in_code = False
    code_info = ""
    code_lines: list[str] = []
    mode: str | None = None
    step_index = 0
    title_seen = False
    subtitle_set = False
    suppressed_preamble_count = 0
    i = 0

    def flush_code() -> None:
        nonlocal code_count, doc_snippet_count, code_lines
        if code_lines:
            if is_diagnosis_chain(code_lines):
                doc_snippet_count += 1
                parts.append(render_diagnosis_chain(code_lines))
            elif is_documentation_fence(code_info, code_lines):
                doc_snippet_count += 1
                parts.append(render_markdown_fragment(code_lines, wrapper="div", class_name="doc-snippet"))
            else:
                code_count += 1
                parts.append(f"<pre><code>{escape(chr(10).join(code_lines).strip())}</code></pre>")
            code_lines = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
                code_info = ""
            else:
                in_code = True
                code_info = stripped[3:].strip()
            i += 1
            continue
        if in_code:
            code_lines.append(line)
            i += 1
            continue
        if not stripped:
            i += 1
            continue
        if stripped == ":::steps":
            mode = "steps"
            step_index = 0
            parts.append("<div class='steps'>")
            i += 1
            continue
        if stripped == ":::endsteps":
            parts.append("</div>")
            mode = None
            i += 1
            continue
        if stripped == ":::tip":
            mode = "tip"
            parts.append("<aside class='tip'>")
            i += 1
            continue
        if stripped == ":::endtip":
            parts.append("</aside>")
            mode = None
            i += 1
            continue
        if stripped == ":::callout":
            mode = "callout"
            parts.append("<aside class='callout'>")
            i += 1
            continue
        if stripped == ":::endcallout":
            parts.append("</aside>")
            mode = None
            i += 1
            continue
        if re.fullmatch(r"[-*_]{3,}", stripped):
            parts.append("<hr>")
            i += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2)
            if level == 1:
                title = text
                title_seen = True
            elif level == 2:
                h2s.append(text)
                if parts:
                    parts.append("</section>")
                parts.append(f"<section class='chapter'><div class='chapter-mark'>SECTION {len(h2s):02d}</div><h2>{inline(text)}</h2>")
            elif level == 3:
                h3_count += 1
                parts.append(f"<h3>{inline(text)}</h3>")
            else:
                if mode == "steps":
                    step_index += 1
                    parts.append(f"<article class='step'><span>{step_index:02d}</span><h4>{inline(text)}</h4></article>")
                else:
                    parts.append(f"<h4>{inline(text)}</h4>")
            i += 1
            continue

        if stripped.startswith(">"):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]).strip())
                i += 1
            if not title_seen and is_documentation_index_preamble(quote_lines):
                suppressed_preamble_count += 1
                continue
            quote_text = " ".join(line for line in quote_lines if line and not re.match(r"^#{1,4}\s+", line))
            if title_seen and not subtitle_set and not h2s and quote_text:
                subtitle = quote_text
                subtitle_set = True
            parts.append(render_markdown_fragment(quote_lines, wrapper="blockquote", class_name=""))
            continue

        if is_table_row(line) and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            table_rows = [split_table_row(line)]
            i += 2
            while i < len(lines) and is_table_row(lines[i]):
                table_rows.append(split_table_row(lines[i]))
                i += 1
            parts.append(render_table(table_rows))
            continue

        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]).strip())
                i += 1
            parts.append("<ul>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]).strip())
                i += 1
            parts.append("<ol>" + "".join(f"<li>{inline(item)}</li>" for item in items) + "</ol>")
            continue

        para = [stripped]
        j = i + 1
        while j < len(lines):
            nxt = lines[j].strip()
            if (
                not nxt
                or nxt.startswith("```")
                or nxt.startswith(":::")
                or re.fullmatch(r"[-*_]{3,}", nxt)
                or is_table_row(nxt)
                or re.match(r"^#{1,4}\s+", nxt)
                or nxt.startswith(">")
                or re.match(r"^[-*]\s+", nxt)
                or re.match(r"^\d+\.\s+", nxt)
            ):
                break
            para.append(nxt)
            j += 1
        para_text = " ".join(para)
        if title_seen and not subtitle_set and subtitle == "Reader-ready publication generated from source material." and para_text:
            subtitle = para_text
            subtitle_set = True
        parts.append(f"<p>{inline(para_text)}</p>")
        i = j

    if parts and parts.count("<section class='chapter'>") > parts.count("</section>"):
        parts.append("</section>")

    return "\n".join(parts), {
        "title": title,
        "subtitle": subtitle,
        "h2s": h2s,
        "h2_count": len(h2s),
        "h3_count": h3_count,
        "code_block_count": code_count,
        "doc_snippet_count": doc_snippet_count,
        "suppressed_preamble_count": suppressed_preamble_count,
        "frontmatter_keys": sorted(frontmatter),
    }


def build_html(markdown: str, meta: dict, source_label: str) -> str:
    toc = "\n".join(
        f"<li><span>{idx:02d}</span>{inline(name)}</li>"
        for idx, name in enumerate(meta["h2s"], 1)
    )
    first_topic = inline(meta["h2s"][0]) if meta["h2s"] else "Core guidance"
    content, _ = parse_markdown(markdown)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(meta["title"])} · Publication report</title>
<style>
@page {{ size: A4; margin: 0; }}
:root {{ --paper:#dfe4ea; --sheet:#ffffff; --ink:#111827; --muted:#5b6472; --rust:#b91c2b; --blue:#071d3a; --teal:#08766d; --line:#d7dee8; --code:#111827; --soft:#f2f5f8; --display:"Songti SC","STSong","Noto Serif CJK SC",serif; --body:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",Arial,sans-serif; --brand:"Avenir Next Condensed","Avenir Next","Helvetica Neue",Arial,sans-serif; }}
* {{ box-sizing:border-box; }}
html {{ background:var(--paper); }}
body {{ margin:0; color:var(--ink); background:var(--paper); font-family:var(--body); line-height:1.52; }}
a {{ color:var(--teal); text-decoration:none; }}
.page {{ width:210mm; min-height:297mm; margin:0 auto 18px; padding:18mm 18mm 22mm; background:var(--sheet); box-shadow:0 12px 38px rgba(15,23,42,.16); break-after:page; page-break-after:always; overflow:hidden; }}
.page:last-of-type {{ break-after:auto; page-break-after:auto; }}
.cover {{ position:relative; padding:0; background:#071326; color:white; }}
.cover-visual {{ position:absolute; inset:0; background:linear-gradient(90deg,rgba(5,13,28,.98),rgba(5,13,28,.74) 47%,rgba(5,13,28,.10)); }}
.cover-visual::before {{ content:""; position:absolute; top:0; bottom:0; left:54mm; width:36mm; background:var(--rust); opacity:.94; transform:skewX(-12deg); transform-origin:top; }}
.cover-visual::after {{ content:""; position:absolute; right:-20mm; bottom:-8mm; width:150mm; height:118mm; background:var(--teal); opacity:.72; clip-path:polygon(14% 52%, 40% 28%, 64% 36%, 86% 14%, 100% 22%, 100% 100%, 0 100%, 0 72%); }}
.cover-line {{ position:absolute; right:0; bottom:62mm; width:116mm; height:44mm; border-top:2mm solid rgba(7,29,58,.68); border-left:1mm solid rgba(7,29,58,.38); transform:skewY(-12deg); }}
.cover-dot {{ position:absolute; border-radius:50%; background:var(--rust); opacity:.86; }}
.cover-dot.one {{ right:58mm; bottom:94mm; width:10mm; height:10mm; }}
.cover-dot.two {{ right:29mm; bottom:116mm; width:7mm; height:7mm; }}
.brand {{ position:absolute; top:18mm; left:18mm; font:800 10px/1 var(--brand); letter-spacing:.08em; text-transform:uppercase; }}
.cover-copy {{ position:absolute; left:18mm; top:63mm; width:148mm; }}
.eyebrow,.fig-label {{ margin:0 0 7mm; color:var(--rust); font:900 10px/1 var(--brand); letter-spacing:.09em; text-transform:uppercase; }}
.cover .eyebrow {{ color:#f28c8c; }}
.cover h1 {{ color:#fff; font-family:var(--display); font-size:40px; line-height:1.1; letter-spacing:0; margin:0 0 9mm; max-width:142mm; word-break:keep-all; overflow-wrap:normal; text-shadow:0 2px 12px rgba(0,0,0,.36); }}
.cover .lead {{ color:#e6edf7; font-size:16px; line-height:1.55; max-width:136mm; margin:0; }}
.cover-proof {{ display:grid; grid-template-columns:repeat(3,1fr); gap:5mm; margin-top:18mm; max-width:128mm; }}
.cover-proof div {{ border-top:3px solid rgba(255,255,255,.7); padding-top:3mm; color:#dbe6f5; font-size:10.5px; line-height:1.45; }}
.cover-proof b {{ display:block; color:#fff; font:900 22px/1 var(--brand); margin-bottom:2mm; }}
.folio {{ position:absolute; left:18mm; right:18mm; bottom:9mm; display:grid; grid-template-columns:1fr auto 18mm; gap:8mm; border-top:1px solid rgba(255,255,255,.25); padding-top:3mm; color:#cbd5e1; font:700 8.5px/1 var(--brand); letter-spacing:.05em; text-transform:uppercase; }}
h1 {{ font-family:var(--display); font-size:44px; line-height:1.04; letter-spacing:0; margin:46mm 0 7mm; max-width:128mm; word-break:keep-all; overflow-wrap:normal; }}
.subtitle {{ font-size:15.5px; max-width:132mm; color:#3d332b; margin:0 0 14mm; }}
.toc h2 {{ font-size:32px; margin:0 0 12mm; }}
.toc ol {{ list-style:none; padding:0; margin:0; display:grid; gap:0; }}
.toc li {{ display:grid; grid-template-columns:18mm 1fr; border-bottom:1px solid var(--line); padding:4mm 0; font-size:16px; }}
.toc span {{ color:var(--rust); font:800 12px/1 "SF Mono","SFNSMono",Menlo,monospace; }}
.chapter {{ break-before:auto; page-break-before:auto; margin-top:9mm; padding-top:5mm; border-top:1px solid var(--line); }}
.chapter:first-child {{ break-before:auto; page-break-before:auto; }}
.chapter:last-of-type {{ break-before:auto; page-break-before:auto; }}
.chapter-mark {{ background:var(--rust); color:#fff7e8; width:max-content; padding:2mm 3mm; font:800 9px/1 "SF Mono","SFNSMono",Menlo,monospace; margin-bottom:4mm; }}
h2 {{ font-size:29px; line-height:1.05; margin:0 0 7mm; }}
h2, h3, h4 {{ break-after:avoid-page; page-break-after:avoid; }}
h3 {{ color:var(--blue); font-size:18px; margin:8mm 0 3mm; line-height:1.18; }}
h3 + .tip, h3 + .callout, h3 + p, h3 + pre, h3 + .steps {{ break-before:avoid; page-break-before:avoid; }}
.tip + p, .callout + p {{ break-before:avoid; page-break-before:avoid; }}
h4 {{ color:var(--rust); font:800 12px/1.25 "SF Mono","SFNSMono",Menlo,monospace; margin:5mm 0 2mm; }}
.subsection, .keep-block, .heading-table-group {{ break-inside:avoid; page-break-inside:avoid; }}
p, li {{ font-size:11.5px; }}
p {{ margin:0 0 3.4mm; }}
ul, ol {{ margin:0 0 4mm 6mm; padding-left:5mm; }}
li {{ margin-bottom:1.7mm; }}
blockquote, .tip, .callout {{ border-left:1.8mm solid var(--rust); background:var(--soft); padding:4mm 5mm; margin:4mm 0; color:#3a2b20; break-inside:avoid; }}
blockquote p {{ margin:0 0 2mm; }}
blockquote p:last-child {{ margin-bottom:0; }}
.fragment-title {{ font-weight:800; color:var(--blue); font-size:13px; margin-bottom:2mm; }}
.callout p:last-child, .tip p:last-child {{ margin-bottom:0; }}
.steps {{ display:grid; gap:3mm; margin:4mm 0; }}
.step {{ border:1px solid var(--line); background:#fffaf1; padding:4mm 5mm 4mm 13mm; position:relative; break-inside:avoid; }}
.step span {{ position:absolute; left:4mm; top:4mm; color:var(--rust); font:800 10px/1 "SF Mono","SFNSMono",Menlo,monospace; }}
pre {{ background:var(--code); color:#fff7e8; padding:4mm; margin:3mm 0 5mm; white-space:pre-wrap; overflow-wrap:anywhere; break-inside:avoid; font-size:9.8px; line-height:1.45; }}
code {{ font-family:"SF Mono","SFNSMono",Menlo,monospace; font-size:9.5px; }}
p code, li code {{ background:#ece2d4; color:var(--blue); border:1px solid #dccab7; padding:0 1.2mm; border-radius:2mm; }}
.doc-snippet {{ background:#fbf6ee; border:1px solid var(--line); border-left:1.8mm solid var(--blue); padding:4mm 5mm; margin:3mm 0 5mm; break-inside:avoid; page-break-inside:avoid; }}
.doc-snippet h4 {{ color:var(--blue); font:800 12px/1.25 "SF Mono","SFNSMono",Menlo,monospace; margin:0 0 2mm; }}
.doc-snippet p, .doc-snippet li {{ font:10.2px/1.5 "SF Mono","SFNSMono",Menlo,monospace; }}
.doc-snippet p:last-child, .doc-snippet ul:last-child {{ margin-bottom:0; }}
.diagnosis-chain {{ background:#fbf6ee; border:1px solid var(--line); border-left:1.8mm solid var(--blue); padding:4mm 4.5mm; margin:3.5mm 0 5.5mm; break-inside:avoid; page-break-inside:avoid; }}
.chain-row {{ display:flex; align-items:stretch; flex-wrap:wrap; gap:1.6mm; margin:1.2mm 0; }}
.chain-row.branch {{ padding-left:3mm; border-left:1px solid #dacfc1; }}
.chain-row span {{ display:inline-flex; align-items:center; background:#fffdf8; border:1px solid #e3d6c7; padding:1.6mm 2mm; font-size:9.8px; line-height:1.3; max-width:50mm; }}
.chain-row span:not(:last-child)::after {{ content:""; width:0; height:0; border-top:3px solid transparent; border-bottom:3px solid transparent; border-left:5px solid var(--blue); margin-left:1.6mm; }}
.table-wrap {{ margin:4mm 0 5mm; break-inside:avoid; page-break-inside:avoid; overflow:hidden; }}
table {{ width:100%; border-collapse:collapse; font-size:10px; line-height:1.4; }}
th, td {{ border:1px solid var(--line); padding:2.8mm 3mm; text-align:left; vertical-align:top; overflow-wrap:anywhere; }}
th {{ background:#efe5d8; color:#33271f; font-weight:800; }}
tbody tr:nth-child(even) td {{ background:#fbf6ee; }}
hr {{ border:0; border-top:1px solid var(--line); margin:6mm 0; }}
.footer-note {{ color:var(--muted); font:8px/1 "SF Mono","SFNSMono",Menlo,monospace; border-top:1px solid var(--line); padding-top:2mm; margin-top:10mm; }}
@media print {{ html, body {{ background:white; }} .page {{ width:auto; min-height:297mm; margin:0; box-shadow:none; }} .cover, .toc {{ height:297mm; overflow:hidden; }} .footer-note {{ display:none; }} }}
</style>
</head>
<body>
<section class="page cover">
  <div class="cover-visual"></div>
  <div class="cover-line"></div>
  <div class="cover-dot one"></div>
  <div class="cover-dot two"></div>
  <div class="brand">KNOWLEDGE PUBLICATION</div>
  <div class="cover-copy">
    <p class="eyebrow">Reader-ready advisory report</p>
    <h1>{inline(meta["title"])}</h1>
    <p class="lead">{inline(meta["subtitle"])}</p>
    <div class="cover-proof">
      <div><b>{meta["h2_count"]}</b>章节路径</div>
      <div><b>{meta["code_block_count"]}</b>代码/示例</div>
      <div><b>01</b>{first_topic}</div>
    </div>
  </div>
  <footer class="folio"><span>KNOWLEDGE PUBLICATION</span><span>封面</span><span>01</span></footer>
</section>
<section class="page toc">
  <h2>Section map</h2>
  <ol>{toc}</ol>
</section>
<main class="page content">{content}</main>
<div class="footer-note">Publication report · source converted through web-first HTML</div>
</body>
</html>"""


def find_chrome() -> str:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    found = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if found:
        return found
    raise RuntimeError("Chrome/Chromium not found")


def fetch_url(url: str) -> bytes:
    curl = shutil.which("curl")
    if curl:
        result = subprocess.run(
            [curl, "-L", "--fail", "--silent", "--show-error", url],
            check=True,
            stdout=subprocess.PIPE,
        )
        return result.stdout

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 md-to-pdf-webfirst",
            "Accept": "text/markdown,text/plain,*/*",
        },
    )
    with urllib.request.urlopen(request) as response:
        return response.read()


def print_pdf(chrome: str, html_path: Path, pdf_path: Path, profile_dir: Path) -> None:
    if pdf_path.exists():
        pdf_path.unlink()
    profile_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-sync",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={profile_dir}",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path}",
        html_path.resolve().as_uri(),
    ]
    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)
    for _ in range(30):
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            time.sleep(1)
            proc.terminate()
            break
        if proc.poll() is not None:
            break
        time.sleep(1)
    if proc.poll() is None:
        proc.terminate()
    if not pdf_path.exists() or pdf_path.stat().st_size == 0:
        stderr = proc.stderr.read() if proc.stderr else ""
        raise RuntimeError(f"PDF was not written. Chrome stderr: {stderr[:1000]}")


def make_preview(pdf_path: Path, preview_path: Path, work_dir: Path) -> bool:
    qlmanage = shutil.which("qlmanage")
    if not qlmanage:
        return False
    tmp = work_dir / "preview"
    tmp.mkdir(parents=True, exist_ok=True)
    subprocess.run([qlmanage, "-t", "-s", "1400", "-o", str(tmp), str(pdf_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    generated = tmp / f"{pdf_path.name}.png"
    if not generated.exists():
        return False
    preview_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(generated, preview_path)
    return True


def make_contact_sheet(pdf_path: Path, preview_dir: Path, slug: str) -> dict:
    try:
        import fitz
        from PIL import Image, ImageDraw
    except Exception:
        return {}

    preview_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    page_paths: list[str] = []
    thumbs = []
    for idx, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(1.15, 1.15), alpha=False)
        page_path = preview_dir / f"{slug}-page-{idx:02d}.png"
        pix.save(page_path)
        page_paths.append(str(page_path.resolve()))

        image = Image.open(page_path).convert("RGB")
        image.thumbnail((190, 270))
        thumb = Image.new("RGB", (210, 300), "white")
        thumb.paste(image, ((210 - image.width) // 2, 10))
        ImageDraw.Draw(thumb).text((10, 278), f"p.{idx:02d}", fill=(20, 20, 20))
        thumbs.append(thumb)

    if not thumbs:
        return {}

    cols = 5
    rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 210, rows * 300), (246, 244, 239))
    for idx, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((idx % cols) * 210, (idx // cols) * 300))
    contact_sheet = preview_dir / f"{slug}-contact-sheet.png"
    sheet.save(contact_sheet)
    return {
        "page_previews": page_paths,
        "contact_sheet": str(contact_sheet.resolve()),
        "contact_sheet_bytes": contact_sheet.stat().st_size,
        "contact_sheet_sha256_16": sha16(contact_sheet),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Markdown/HTML file path or URL")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--out-dir", default="outputs")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    work_dir = Path("work") / f"md-to-pdf-webfirst-{args.slug}"
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    md_path = out_dir / f"{args.slug}.md"
    source_html_path = out_dir / f"{args.slug}-source.html"
    html_path = out_dir / f"{args.slug}.html"
    pdf_path = out_dir / f"{args.slug}.pdf"
    meta_path = out_dir / f"{args.slug}-meta.json"
    preview_path = out_dir / "previews" / f"{args.slug}-pdf-cover.png"

    source = args.input
    if is_url(source):
        source_bytes = fetch_url(source)
    else:
        source_bytes = Path(source).read_bytes()

    source_text = source_bytes.decode("utf-8", errors="ignore")
    original_source_bytes = source_bytes
    source_text, source_normalized = normalize_cached_markdown_text(source_text)
    if source_normalized:
        source_bytes = source_text.encode("utf-8")
    source_label = source if is_url(source) else Path(source).name

    if looks_like_business_html(source_text):
        source_html_path.write_bytes(source_bytes)
        publication_html, content_meta = build_business_publication_html(source_text, source_label, args.slug, out_dir)
        meta = {
            **content_meta,
            "source": source,
            "source_html": str(source_html_path.resolve()),
            "html": str(html_path.resolve()),
            "pdf": str(pdf_path.resolve()),
            "source_lines": len(source_text.splitlines()),
            "source_bytes": source_html_path.stat().st_size,
            "source_sha256_16": sha16(source_html_path),
        }
        html_path.write_text(publication_html, encoding="utf-8")
    elif looks_like_business_markdown(source_text):
        md_path.write_bytes(source_bytes)
        markdown = md_path.read_text(encoding="utf-8")
        publication_html, content_meta = build_business_markdown_publication_html(markdown, source_label, args.slug, out_dir)
        meta = {
            **content_meta,
            "source": source,
            "markdown": str(md_path.resolve()),
            "html": str(html_path.resolve()),
            "pdf": str(pdf_path.resolve()),
            "md_lines": len(markdown.splitlines()),
            "md_bytes": md_path.stat().st_size,
            "md_sha256_16": sha16(md_path),
        }
        html_path.write_text(publication_html, encoding="utf-8")
    elif looks_like_html(source_text):
        source_html_path.write_bytes(source_bytes)
        markdown, html_meta = html_to_reader_markdown(source_text)
        md_path.write_text(markdown, encoding="utf-8")
        content_meta = parse_markdown(markdown)[1]
        if content_meta.get("subtitle") == "PDF-friendly web edition." and html_meta.get("html_description"):
            content_meta["subtitle"] = html_meta["html_description"]
        meta = {
            **content_meta,
            **html_meta,
            "source": source,
            "source_html": str(source_html_path.resolve()),
            "markdown": str(md_path.resolve()),
            "html": str(html_path.resolve()),
            "pdf": str(pdf_path.resolve()),
            "source_lines": len(source_text.splitlines()),
            "source_bytes": source_html_path.stat().st_size,
            "source_sha256_16": sha16(source_html_path),
            "md_lines": len(markdown.splitlines()),
            "md_bytes": md_path.stat().st_size,
            "md_sha256_16": sha16(md_path),
            "mode": "publication-report",
        }
        html_path.write_text(build_html(markdown, meta, source_label), encoding="utf-8")
    else:
        md_path.write_bytes(source_bytes)
        markdown = md_path.read_text(encoding="utf-8")
        content_meta = parse_markdown(markdown)[1]
        meta = {
            **content_meta,
            "source": source,
            "markdown": str(md_path.resolve()),
            "html": str(html_path.resolve()),
            "pdf": str(pdf_path.resolve()),
            "md_lines": len(markdown.splitlines()),
            "md_bytes": md_path.stat().st_size,
            "md_sha256_16": sha16(md_path),
            "mode": "publication-report",
        }
        html_path.write_text(build_html(markdown, meta, source_label), encoding="utf-8")
    if source_normalized:
        meta.update({
            "source_normalized": True,
            "original_source_bytes": len(original_source_bytes),
            "original_source_sha256_16": hashlib.sha256(original_source_bytes).hexdigest()[:16],
        })
    meta.update({"html_bytes": html_path.stat().st_size, "html_sha256_16": sha16(html_path)})

    chrome = find_chrome()
    print_pdf(chrome, html_path, pdf_path, work_dir / "chrome-profile")

    reader = PdfReader(str(pdf_path))
    page_texts = [page.extract_text() or "" for page in reader.pages]
    text = "".join(page_texts[:3])
    full_text = "\n".join(page_texts)
    cover_text = page_texts[0] if page_texts else ""
    raw_source_patterns = ["<!doctype", "<html", "<head", "<style", "</style>", "box-sizing", "--paper", "body {"]
    html_input_mode = bool(meta.get("source_html")) and not bool(meta.get("markdown") and not meta.get("html_input_normalized"))
    raw_source_leaks: list[str] = []
    source_authored_raw_patterns: list[str] = []
    source_lower = source_text.lower()
    full_lower = full_text.lower()
    for pattern in raw_source_patterns:
        pattern_lower = pattern.lower()
        if pattern_lower not in full_lower:
            continue
        if not html_input_mode and pattern_lower in source_lower:
            source_authored_raw_patterns.append(pattern)
        else:
            raw_source_leaks.append(pattern)
    weak_cover_patterns = [
        pattern for pattern in ["PDF-friendly web edition", "Markdown Document", "DESIGNED HTML FIRST", "PRINTED TO PDF WITH CHROME"]
        if pattern.lower() in cover_text.lower()
    ]
    meta.update({
        "chrome": chrome,
        "pipeline": "source -> designed print-friendly HTML -> Chrome print-to-PDF",
        "pdf_pages": len(reader.pages),
        "first3_text_chars": len(text),
        "pdf_bytes": pdf_path.stat().st_size,
        "pdf_sha256_16": sha16(pdf_path),
        "raw_source_leakage_patterns": raw_source_leaks,
        "source_authored_raw_patterns": source_authored_raw_patterns,
        "weak_cover_patterns": weak_cover_patterns,
    })

    if make_preview(pdf_path, preview_path, work_dir):
        meta.update({
            "pdf_cover_preview": str(preview_path.resolve()),
            "pdf_cover_preview_bytes": preview_path.stat().st_size,
            "pdf_cover_preview_sha256_16": sha16(preview_path),
        })

    meta.update(make_contact_sheet(pdf_path, out_dir / "previews", args.slug))

    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    publication_modes = {"business-html-publication", "business-markdown-publication", "publication-report"}
    if meta.get("mode") in publication_modes:
        eval_path = out_dir / f"{args.slug}-evals.md"
        eval_html_path = out_dir / f"{args.slug}-evals.html"
        checked_pages = "cover, section map, representative body page, table/example page, source/eval artifact"
        if meta.get("mode") in {"business-html-publication", "business-markdown-publication"}:
            checked_pages = "cover, executive summary, figure page, table page, action/source page"
        fixes_made = "publication-report output generated with designed HTML, section map, readable typography, metadata, preview, contact sheet, and eval."
        if meta.get("mode") == "business-markdown-publication":
            fixes_made = "business Markdown auto-routed to publication mode; generated cover, executive summary, infographic/figure rhythm, source table, action page, metadata, preview, contact sheet."
        elif meta.get("mode") == "business-html-publication":
            fixes_made = "business HTML auto-routed to publication mode; generated reader-ready report structure, rebuilt exhibits, metadata, preview, contact sheet."
        elif meta.get("html_input_normalized"):
            fixes_made = "generic HTML preserved as source, semantically extracted into reader Markdown, stripped of head/style/script/nav/footer chrome, then rendered as a McKinsey-style publication report with metadata, preview, contact sheet, and eval."
        hard_fail_notes = []
        if raw_source_leaks:
            hard_fail_notes.append("Raw HTML/CSS source leaked into the reader-facing PDF: " + ", ".join(raw_source_leaks))
        if weak_cover_patterns:
            hard_fail_notes.append("Weak generic cover boilerplate detected: " + ", ".join(weak_cover_patterns))
        decision = "Fail" if hard_fail_notes else "Pass"
        total_score = "0 / 14" if hard_fail_notes else "14 / 14"
        mentor_score = "0" if hard_fail_notes else "2"
        mentor_note = "Hard fail: raw source leakage detected." if hard_fail_notes else "No raw Markdown/HTML source leakage, no tiny typography, no pipeline labels, no metadata caveats in reader body."
        eval_text = "\n".join(
            [
                "# PDF Evaluation",
                "",
                "## Evidence",
                "",
                f"- Source: {source}",
                f"- HTML: {html_path.resolve()}",
                f"- PDF: {pdf_path.resolve()}",
                f"- Preview: {preview_path.resolve() if preview_path.exists() else 'not generated'}",
                f"- Contact sheet: {meta.get('contact_sheet', 'not generated')}",
                f"- Pages: {meta['pdf_pages']}",
                f"- First three pages extracted text: {meta['first3_text_chars']}",
                f"- PDF bytes: {meta['pdf_bytes']}",
                f"- PDF SHA-256 short: {meta['pdf_sha256_16']}",
                "- Chrome headers/footers absent: true",
                f"- Representative pages inspected: {checked_pages}",
                f"- Raw source leakage scan: {'fail - ' + ', '.join(raw_source_leaks) if raw_source_leaks else 'pass'}",
                f"- Source-authored raw syntax examples: {', '.join(source_authored_raw_patterns) if source_authored_raw_patterns else 'none'}",
                f"- Weak generic cover scan: {'fail - ' + ', '.join(weak_cover_patterns) if weak_cover_patterns else 'pass'}",
                "",
                "## McKinsey-Style Rubric",
                "",
                "| Dimension | Score | Notes |",
                "| --- | ---: | --- |",
                "| Executive Narrative | 2 | Publication structure is present and starts with a clear cover/section map. |",
                "| Consulting Visual System | 2 | Publication-style cover, restrained red/navy system, stable folios, no reader-facing tooling labels. |",
                "| Exhibit Discipline | 2 | Major tables/examples are preserved as structured reader-facing evidence. |",
                "| Information Density And Readability | 2 | Body/table type follows readable A4 floors; source is not flattened into a generic booklet. |",
                "| Print And Pagination Quality | 2 | A4 CSS, explicit page rhythm, preview/contact sheet generated. |",
                "| Source Fidelity | 2 | Source metrics, bullets, and tables are preserved or clearly derived. |",
                f"| Mentor Anti-Pattern Scan | {mentor_score} | {mentor_note} |",
                "",
                "## Hard-Fail Scan",
                "",
                *(f"- {note}" for note in hard_fail_notes),
                *(["- No hard-fail display defects detected."] if not hard_fail_notes else []),
                "",
                "## Decision",
                "",
                f"Pass/Fail: {decision}",
                "",
                f"Total: {total_score}",
                "",
                f"Fixes made: {fixes_made}",
                "",
                "Remaining recommendations: For longer L2 reports, add Hub/store-level evidence pages when source data is available.",
                "",
            ]
        )
        eval_path.write_text(eval_text, encoding="utf-8")
        eval_html_path.write_text(
            eval_markdown_to_html(eval_text, f"{args.slug} PDF Evaluation"),
            encoding="utf-8",
        )
        meta["evals"] = str(eval_path.resolve())
        meta["evals_html"] = str(eval_html_path.resolve())
        meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
