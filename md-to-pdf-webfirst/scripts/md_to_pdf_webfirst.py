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
from pathlib import Path

from pypdf import PdfReader


CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def sha16(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def escape(text: str) -> str:
    return html.escape(text, quote=True)


def inline(text: str) -> str:
    text = escape(text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<a>\1</a>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


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
        result.append(re.sub(r"\s+theme=\{null\}", "", line))
    return result


def parse_markdown(markdown: str) -> tuple[str, dict]:
    lines = normalize(markdown.splitlines())
    parts: list[str] = []
    h2s: list[str] = []
    title = "Markdown Document"
    subtitle = "PDF-friendly web edition."
    code_count = 0
    h3_count = 0
    in_code = False
    code_lines: list[str] = []
    mode: str | None = None
    step_index = 0
    i = 0

    def flush_code() -> None:
        nonlocal code_count, code_lines
        if code_lines:
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
            else:
                in_code = True
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

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            level = len(heading.group(1))
            text = heading.group(2)
            if level == 1:
                title = text
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
            quote = stripped.lstrip("> ").strip()
            if quote and not subtitle.startswith("Step-by-step"):
                subtitle = quote
            parts.append(f"<blockquote>{inline(quote)}</blockquote>")
            i += 1
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
                or re.match(r"^#{1,4}\s+", nxt)
                or nxt.startswith(">")
                or re.match(r"^[-*]\s+", nxt)
                or re.match(r"^\d+\.\s+", nxt)
            ):
                break
            para.append(nxt)
            j += 1
        parts.append(f"<p>{inline(' '.join(para))}</p>")
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
    }


def build_html(markdown: str, meta: dict, source_label: str) -> str:
    toc = "\n".join(
        f"<li><span>{idx:02d}</span>{inline(name)}</li>"
        for idx, name in enumerate(meta["h2s"], 1)
    )
    content, _ = parse_markdown(markdown)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(meta["title"])} · PDF-friendly web edition</title>
<style>
@page {{ size: A4; margin: 14mm 16mm 15mm; }}
:root {{ --paper:#f5f1e8; --sheet:#fffdf8; --ink:#17130f; --muted:#6d6258; --rust:#b45136; --blue:#263f73; --teal:#176b63; --line:#d9cbbb; --code:#17130f; --soft:#f8f2e8; }}
* {{ box-sizing:border-box; }}
html {{ background:var(--paper); }}
body {{ margin:0; color:var(--ink); background:var(--paper); font-family:"Iowan Old Style", "Songti SC", "STSong", "Noto Serif CJK SC", Georgia, serif; line-height:1.52; }}
a {{ color:var(--teal); text-decoration:none; }}
.page {{ width:210mm; min-height:297mm; margin:0 auto 18px; padding:18mm 18mm 16mm; background:var(--sheet); box-shadow:0 12px 38px rgba(45,33,20,.14); break-after:page; page-break-after:always; }}
.page:last-of-type {{ break-after:auto; page-break-after:auto; }}
.cover {{ position:relative; display:grid; align-content:center; overflow:hidden; background:linear-gradient(90deg, rgba(180,81,54,.11) 1px, transparent 1px) 0 0/10mm 10mm, linear-gradient(0deg, rgba(38,63,115,.08) 1px, transparent 1px) 0 0/10mm 10mm, var(--sheet); }}
.cover::after {{ content:""; position:absolute; inset:0 20mm 0 auto; width:8mm; background:var(--rust); box-shadow:10mm 0 0 var(--blue); }}
.kicker {{ font:800 10px/1.2 "SF Mono","SFNSMono",Menlo,monospace; color:var(--rust); text-transform:uppercase; letter-spacing:.08em; }}
h1 {{ font-size:44px; line-height:1.04; letter-spacing:0; margin:46mm 0 7mm; max-width:128mm; word-break:keep-all; overflow-wrap:normal; }}
.subtitle {{ font-size:15.5px; max-width:132mm; color:#3d332b; margin:0 0 14mm; }}
.blackbar {{ background:var(--code); color:#fff7e8; padding:5mm 6mm; font:11px/1 "SF Mono","SFNSMono",Menlo,monospace; width:165mm; letter-spacing:.03em; }}
.facts {{ display:grid; grid-template-columns:30mm 1fr; width:148mm; margin-top:11mm; font:10px/1.35 "SF Mono","SFNSMono",Menlo,monospace; }}
.facts div {{ border-bottom:1px solid rgba(91,72,53,.28); padding:3mm; }}
.facts div:nth-child(odd) {{ color:var(--rust); font-weight:700; text-transform:lowercase; }}
.toc h2 {{ font-size:32px; margin:0 0 12mm; }}
.toc ol {{ list-style:none; padding:0; margin:0; display:grid; gap:0; }}
.toc li {{ display:grid; grid-template-columns:18mm 1fr; border-bottom:1px solid var(--line); padding:4mm 0; font-size:16px; }}
.toc span {{ color:var(--rust); font:800 12px/1 "SF Mono","SFNSMono",Menlo,monospace; }}
.chapter {{ break-before:page; page-break-before:always; }}
.chapter:first-child {{ break-before:auto; page-break-before:auto; }}
.chapter:last-of-type {{ break-before:auto; page-break-before:auto; }}
.chapter-mark {{ background:var(--rust); color:#fff7e8; width:max-content; padding:2mm 3mm; font:800 9px/1 "SF Mono","SFNSMono",Menlo,monospace; margin-bottom:4mm; }}
h2 {{ font-size:29px; line-height:1.05; margin:0 0 7mm; }}
h3 {{ color:var(--blue); font-size:18px; margin:8mm 0 3mm; line-height:1.18; }}
h4 {{ color:var(--rust); font:800 12px/1.25 "SF Mono","SFNSMono",Menlo,monospace; margin:5mm 0 2mm; }}
p, li {{ font-size:11.2px; }}
p {{ margin:0 0 3.4mm; }}
ul, ol {{ margin:0 0 4mm 6mm; padding-left:5mm; }}
li {{ margin-bottom:1.7mm; }}
blockquote, .tip {{ border-left:1.8mm solid var(--rust); background:var(--soft); padding:4mm 5mm; margin:4mm 0; color:#3a2b20; }}
.steps {{ display:grid; gap:3mm; margin:4mm 0; }}
.step {{ border:1px solid var(--line); background:#fffaf1; padding:4mm 5mm 4mm 13mm; position:relative; break-inside:avoid; }}
.step span {{ position:absolute; left:4mm; top:4mm; color:var(--rust); font:800 10px/1 "SF Mono","SFNSMono",Menlo,monospace; }}
pre {{ background:var(--code); color:#fff7e8; padding:4mm; margin:3mm 0 5mm; white-space:pre-wrap; overflow-wrap:anywhere; break-inside:avoid; }}
code {{ font-family:"SF Mono","SFNSMono",Menlo,monospace; font-size:9.3px; }}
p code, li code {{ background:#ece2d4; color:var(--blue); border:1px solid #dccab7; padding:0 1.2mm; border-radius:2mm; }}
.footer-note {{ position:fixed; bottom:6mm; left:16mm; right:16mm; color:var(--muted); font:8px/1 "SF Mono","SFNSMono",Menlo,monospace; border-top:1px solid var(--line); padding-top:2mm; }}
@media print {{ html, body {{ background:white; }} .page {{ width:auto; min-height:267mm; margin:0; box-shadow:none; }} .cover, .toc {{ height:267mm; overflow:hidden; }} .footer-note {{ position:fixed; }} }}
</style>
</head>
<body>
<section class="page cover">
  <div class="kicker">Markdown / PDF-friendly web first</div>
  <h1>{inline(meta["title"])}</h1>
  <p class="subtitle">{inline(meta["subtitle"])}</p>
  <div class="blackbar">DESIGNED HTML FIRST · PRINTED TO PDF WITH CHROME</div>
  <div class="facts">
    <div>source</div><div>{escape(source_label)}</div>
    <div>lines</div><div>{meta["md_lines"]}</div>
    <div>sections</div><div>{meta["h2_count"]}</div>
    <div>code blocks</div><div>{meta["code_block_count"]}</div>
  </div>
</section>
<section class="page toc">
  <h2>Section map</h2>
  <ol>{toc}</ol>
</section>
<main class="page content">{content}</main>
<div class="footer-note">PDF-friendly web edition · source converted from markdown</div>
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Markdown file path or URL")
    parser.add_argument("--slug", required=True)
    parser.add_argument("--out-dir", default="outputs")
    args = parser.parse_args()

    out_dir = Path(args.out_dir)
    work_dir = Path("work") / f"md-to-pdf-webfirst-{args.slug}"
    out_dir.mkdir(parents=True, exist_ok=True)
    work_dir.mkdir(parents=True, exist_ok=True)

    md_path = out_dir / f"{args.slug}.md"
    html_path = out_dir / f"{args.slug}.html"
    pdf_path = out_dir / f"{args.slug}.pdf"
    meta_path = out_dir / f"{args.slug}-meta.json"
    preview_path = out_dir / "previews" / f"{args.slug}-pdf-cover.png"

    source = args.input
    if is_url(source):
        md_path.write_bytes(fetch_url(source))
    else:
        md_path.write_bytes(Path(source).read_bytes())

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
    }
    html_path.write_text(build_html(markdown, meta, source), encoding="utf-8")
    meta.update({"html_bytes": html_path.stat().st_size, "html_sha256_16": sha16(html_path)})

    chrome = find_chrome()
    print_pdf(chrome, html_path, pdf_path, work_dir / "chrome-profile")

    reader = PdfReader(str(pdf_path))
    text = "".join((page.extract_text() or "") for page in reader.pages[:3])
    meta.update({
        "chrome": chrome,
        "pipeline": "markdown -> designed print-friendly HTML -> Chrome print-to-PDF",
        "pdf_pages": len(reader.pages),
        "first3_text_chars": len(text),
        "pdf_bytes": pdf_path.stat().st_size,
        "pdf_sha256_16": sha16(pdf_path),
    })

    if make_preview(pdf_path, preview_path, work_dir):
        meta.update({
            "pdf_cover_preview": str(preview_path.resolve()),
            "pdf_cover_preview_bytes": preview_path.stat().st_size,
            "pdf_cover_preview_sha256_16": sha16(preview_path),
        })

    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
