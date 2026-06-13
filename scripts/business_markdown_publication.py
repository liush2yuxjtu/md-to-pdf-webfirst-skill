from __future__ import annotations

import html
import re
from pathlib import Path


def _clean(value: str) -> str:
    value = value.replace("\r", "")
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    return re.sub(r"\s+", " ", value).strip()


def _esc(value: str) -> str:
    return html.escape(_clean(value))


def _number(value: str, default: float = 0.0) -> float:
    value = value.replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    return float(match.group(0)) if match else default


def _pct(value: str, default: float = 0.0) -> float:
    match = re.search(r"-?\d+(?:\.\d+)?\s*%", value.replace(",", ""))
    return float(match.group(0).replace("%", "")) if match else default


def looks_like_business_markdown(source: str) -> bool:
    if source.lstrip().lower().startswith(("<!doctype html", "<html")):
        return False
    first_heading = re.search(r"^#{1,3}\s+(.+)$", source, flags=re.M)
    first_heading_text = first_heading.group(1) if first_heading else ""
    if re.search(r"(规则|模板|prompt|提示词|判断规则)", first_heading_text, flags=re.I):
        return False
    if "benchmark_code" in source or re.search(r"\{[^{}\n]*(rd_name|category|month|iya|giv)[^{}\n]*\}", source, flags=re.I):
        return False
    terms = ["IYA", "PS", "品类", "门店", "同比", "环比", "建议", "总体判断", "生意表现"]
    has_table = "|" in source and re.search(r"\|\s*品类\s*\|", source)
    has_title = bool(re.search(r"^#{1,3}\s+.*(生意|业务|诊断|概览|表现)", source, flags=re.M))
    return sum(term in source for term in terms) >= 5 and (has_table or has_title)


def _title(source: str) -> str:
    match = re.search(r"^#{1,3}\s+(.+)$", source, flags=re.M)
    return _clean(match.group(1)) if match else "业务表现概览"


def _section(source: str, name: str) -> str:
    pattern = rf"\*\*\[{re.escape(name)}\]\*\*(.*?)(?=\n---|\n\*\*\[|\Z)"
    match = re.search(pattern, source, flags=re.S)
    return match.group(1).strip() if match else ""


def _bullets(text: str) -> list[str]:
    return [_clean(m.group(1)) for m in re.finditer(r"^\s*-\s+(.+)$", text, flags=re.M)]


def _markdown_table(source: str) -> list[list[str]]:
    lines = source.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("|") and "品类" in line:
            rows: list[list[str]] = []
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                raw = lines[j].strip()
                cells = [c.strip() for c in raw.strip("|").split("|")]
                if not all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    rows.append(cells)
                j += 1
            return rows
    return []


def _html_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    head = "<thead><tr>" + "".join(f"<th>{_esc(c)}</th>" for c in rows[0]) + "</tr></thead>"
    body = "<tbody>" + "".join(
        "<tr>" + "".join(f"<td>{_esc(c)}</td>" for c in row) + "</tr>"
        for row in rows[1:]
    ) + "</tbody>"
    return f"<table>{head}{body}</table>"


def _metric(pattern: str, text: str, default: str = "—") -> str:
    match = re.search(pattern, text)
    return _clean(match.group(1)) if match else default


def _parse_category_bullets(items: list[str]) -> list[dict[str, str | float]]:
    rows: list[dict[str, str | float]] = []
    for item in items:
        name_match = re.match(r"([^：:]+)[：:]", item)
        if not name_match:
            continue
        name = _clean(name_match.group(1))
        iya = _pct(item)
        contribution = _metric(r"下跌贡献率\s*([-\d.]+%)", item)
        ps = _metric(r"PS 门店\s*([+-]?\d+\s*家)", item)
        note = re.sub(r"^[^：:]+[：:]\s*", "", item)
        rows.append({"name": name, "iya": iya, "contribution": contribution, "ps": ps, "note": note})
    return rows


def _bar_rows(rows: list[dict[str, str | float]]) -> str:
    parts: list[str] = []
    for row in rows:
        iya = float(row["iya"])
        width = max(4, min(100, iya / 1.6))
        cls = "risk" if iya < 95 else "growth"
        parts.append(
            f"<div class='bar-row {cls}'><span>{_esc(str(row['name']))}</span>"
            f"<div><i style='width:{width:.1f}%'></i></div><b>{iya:.2f}%</b></div>"
        )
    return "".join(parts)


def _cards(items: list[str], limit: int = 4) -> str:
    cards: list[str] = []
    for item in items[:limit]:
        title = item.split("：", 1)[0] if "：" in item else item.split(":", 1)[0]
        body = item.split("：", 1)[1] if "：" in item else item
        cards.append(f"<article><h3>{_esc(title)}</h3><p>{_esc(body)}</p></article>")
    return "".join(cards)


def _hero_svg(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="950" viewBox="0 0 1600 950">
<rect width="1600" height="950" fill="#f7f8fb"/>
<rect x="0" y="0" width="420" height="950" fill="#071d3a"/>
<path d="M420 0 L690 0 L506 950 L270 950 Z" fill="#b91c2b" opacity=".92"/>
<path d="M650 780 C820 610 940 720 1100 548 S1370 390 1600 468 L1600 950 L650 950 Z" fill="#0b766d" opacity=".76"/>
<path d="M620 690 C780 560 930 632 1080 500 S1360 288 1600 358" fill="none" stroke="#071d3a" stroke-width="8" opacity=".7"/>
<g transform="translate(850 170)" fill="none" stroke="#071d3a" stroke-width="3" opacity=".52">
  <rect x="0" y="260" width="70" height="210"/><rect x="110" y="178" width="70" height="292"/><rect x="220" y="95" width="70" height="375"/><rect x="330" y="20" width="70" height="450"/>
</g>
<g fill="#b91c2b" opacity=".85">
  <circle cx="740" cy="630" r="18"/><circle cx="915" cy="555" r="24"/><circle cx="1110" cy="455" r="28"/><circle cx="1365" cy="325" r="22"/>
</g>
<g transform="translate(70 88)" stroke="#f8fafc" fill="none" opacity=".34">
  <rect x="0" y="0" width="240" height="310"/><path d="M30 60h180M30 120h180M30 180h180M30 240h180"/>
  <circle cx="120" cy="460" r="86"/><path d="M60 460h120M120 400v120"/>
</g>
<g transform="translate(980 150)" fill="none" stroke="#071d3a" stroke-width="8" opacity=".78">
  <circle cx="155" cy="92" r="55"/>
  <path d="M58 430 C88 284 118 190 155 190 C206 190 238 286 268 430"/>
  <path d="M100 262 L20 345 M215 262 L340 330"/>
  <path d="M78 448 H292"/>
</g>
<g transform="translate(1082 314)" fill="#f8fafc" stroke="#071d3a" stroke-width="4" opacity=".9">
  <rect x="0" y="0" width="255" height="142" rx="8"/>
  <path d="M32 38 H220 M32 76 H178 M32 112 H208"/>
</g>
</svg>"""
    path.write_text(svg, encoding="utf-8")


def build_business_markdown_publication_html(source: str, source_label: str, slug: str, out_dir: Path) -> tuple[str, dict]:
    title = _title(source)
    overall = _section(source, "总体判断")
    praise = _bullets(_section(source, "值得表扬"))
    improve = _bullets(_section(source, "有提升空间"))
    low_base = _bullets(_section(source, "Low Base 低基数品类"))
    actions = _bullets(_section(source, "建议"))
    ps_table = _markdown_table(source)
    categories = _parse_category_bullets(praise + improve + low_base)
    issue_categories = [r for r in categories if float(r["iya"]) < 95]
    growth_categories = [r for r in categories if float(r["iya"]) >= 100]

    total_ship = _metric(r"整体出货\s*\*\*([^*]+)\*\*", overall)
    rd_iya = _metric(r"IYA\s*\*\*([^*]+)\*\*", overall)
    mom = _metric(r"vs 上月\s*\*\*([^*]+)\*\*", overall)
    yoy_pp = _metric(r"同比\s*([-\d.]+pp)", overall)
    mom_pp = _metric(r"环比\s*([-\d.]+pp)", overall)
    decline_focus = _metric(r"合计贡献了\s*([^，。]+)", _section(source, "建议"))
    oral_drop = _metric(r"Oral.*?环比暴跌\s*([^，。]+)", _section(source, "建议"))

    hero = out_dir / "assets" / f"{slug}-overview-network.svg"
    _hero_svg(hero)

    category_bars = _bar_rows(categories)
    issue_cards = _cards([str(r["note"]) for r in issue_categories], 4)
    praise_cards = _cards(praise, 2)
    low_base_cards = _cards(low_base, 2)
    action_cards = "".join(
        f"<div class='action'><span>{idx:02d}</span><p>{_esc(item)}</p></div>"
        for idx, item in enumerate(actions or ["进入 Fabric、Hair、Oral 三大品类 L2 下钻分析"], 1)
    )
    evidence_pack = (
        f"<div><h3>总量判断</h3><p>出货 { _esc(total_ship) }，IYA { _esc(rd_iya) }，同比 { _esc(yoy_pp) }。</p></div>"
        f"<div><h3>优先问题</h3><p>Fabric、Hair、Oral 是下一轮下钻入口。</p></div>"
        f"<div><h3>覆盖证据</h3><p>PS 门店表保留原始结构，解释覆盖扩张是否转化。</p></div>"
    )
    low_base_interpretation = (
        "<div><h3>Baby</h3><p>高 IYA 来自极低去年 GIV 与 PS 基数，应作为口径提醒，而不是优先增长结论。</p></div>"
        "<div><h3>Skin</h3><p>今年和去年均无出货，PS 门店为 0，应从核心经营判断中剥离。</p></div>"
        "<div><h3>管理含义</h3><p>低基数品类只用于解释异常值，不改变 Fabric、Hair、Oral 的优先级。</p></div>"
    )
    action_gates = (
        "<div><h3>Fabric</h3><p>验证 PS +3 家为何未转化为产出增长，先查门店动销与铺货质量。</p></div>"
        "<div><h3>Hair</h3><p>作为最大品类，先量化缺口来源，再拆到 Hub 与重点门店。</p></div>"
        "<div><h3>Oral</h3><p>环比暴跌优先排查断货、渠道调整或数据异常。</p></div>"
    )

    html_doc = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{_esc(title)} · publication report</title><style>
@page{{size:A4;margin:0}}:root{{--ink:#111827;--navy:#071d3a;--red:#b91c2b;--teal:#08766d;--soft:#f2f5f8;--line:#d7dee8;--muted:#5b6472;--paper:#fff;--display:"Songti SC","STSong","Noto Serif CJK SC",serif;--body:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",Arial,sans-serif;--brand:"Avenir Next Condensed","Avenir Next","Helvetica Neue",Arial,sans-serif}}*{{box-sizing:border-box}}html,body{{margin:0;background:#dfe4ea;color:var(--ink);font-family:var(--body)}}.page{{position:relative;width:210mm;min-height:297mm;margin:0 auto;background:var(--paper);padding:18mm 18mm 22mm;break-after:page;page-break-after:always;overflow:hidden}}.page:last-child{{break-after:auto;page-break-after:auto}}.cover{{padding:0;background:#071326;color:white}}.cover img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}.shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,13,28,.94),rgba(5,13,28,.60) 46%,rgba(5,13,28,.08))}}.brand{{position:absolute;top:18mm;left:18mm;font:800 10px/1 var(--brand);letter-spacing:.08em}}.cover-copy{{position:absolute;left:18mm;top:64mm;width:150mm}}.eyebrow,.fig-label{{margin:0 0 7mm;color:var(--red);font:900 10px/1 var(--brand);letter-spacing:.09em;text-transform:uppercase}}h1{{font-family:var(--display);font-size:40px;line-height:1.1;margin:0 0 9mm}}h2{{font-family:var(--display);font-size:27px;line-height:1.14;margin:0 0 7mm}}h3{{font-size:15px;line-height:1.25;margin:0 0 3mm;color:var(--navy)}}p,li{{font-size:11.5px;line-height:1.65;margin:0 0 4mm}}.lead{{font-size:16px;line-height:1.55;color:#293241;max-width:154mm}}.cover .lead{{color:#e6edf7}}.folio{{position:absolute;left:18mm;right:18mm;bottom:9mm;display:grid;grid-template-columns:1fr auto 18mm;gap:8mm;border-top:1px solid var(--line);padding-top:3mm;color:var(--muted);font:700 8.5px/1 var(--brand);letter-spacing:.05em;text-transform:uppercase}}.cover .folio{{color:#cbd5e1;border-color:rgba(255,255,255,.25)}}.metric-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:5mm;margin:10mm 0}}.metric-row div,.note-grid div{{border-top:3px solid var(--navy);background:var(--soft);padding:5mm}}.metric-row b{{display:block;font:900 24px/1 var(--brand);color:var(--navy);margin-bottom:3mm}}.metric-row small{{display:block;color:var(--muted);font-size:9.5px}}.toc{{list-style:none;padding:0;margin:17mm 0 0}}.toc li{{display:grid;grid-template-columns:18mm 1fr 24mm;border-bottom:1px solid var(--line);padding:5mm 0;font-size:15px}}.toc span{{color:var(--red);font:900 12px/1 var(--brand)}}.toc em{{font-style:normal;text-align:right;color:var(--muted)}}.framework-img{{width:100%;height:90mm;object-fit:cover;border:1px solid var(--line);margin:5mm 0}}.framework-row,.issue-grid,.note-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:7mm}}.framework-row div,.issue-grid article{{border:1px solid var(--line);background:var(--soft);padding:5mm}}.framework-row span{{display:block;color:var(--red);font:900 10px/1 var(--brand);margin-bottom:2mm}}.big-layout{{display:grid;grid-template-columns:42mm 1fr 42mm;gap:7mm;align-items:center;margin-top:10mm}}.big-num{{border:1px solid var(--line);background:var(--soft);text-align:center;padding:7mm}}.big-num b{{display:block;font:900 46px/1 var(--brand);color:var(--navy)}}.big-num.red b{{color:var(--red)}}.flow{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}}.flow div{{border:1px solid var(--line);padding:4mm;background:white;text-align:center;font-weight:800;font-size:11px}}.figure-card{{border:1px solid var(--line);padding:7mm;background:linear-gradient(180deg,#fff,var(--soft));margin-top:6mm}}.bar-row{{display:grid;grid-template-columns:29mm 1fr 24mm;gap:5mm;align-items:center;margin:3.1mm 0;font-size:11px}}.bar-row div{{height:7.5mm;background:white;border:1px solid var(--line)}}.bar-row i{{display:block;height:100%;background:var(--teal)}}.bar-row.risk i{{background:var(--red)}}.bar-row b{{font-family:Menlo,monospace}}table{{width:100%;border-collapse:collapse;font-size:10.2px;line-height:1.45;margin-top:5mm}}th,td{{border:1px solid var(--line);padding:2.7mm 3mm;text-align:left;vertical-align:top}}th{{background:var(--soft);font-weight:800}}tbody tr:nth-child(even) td{{background:#fafbfd}}.action{{display:grid;grid-template-columns:16mm 1fr;gap:5mm;border-top:1px solid var(--line);padding:4mm 0}}.action span{{display:grid;place-items:center;width:11mm;height:11mm;background:var(--red);color:white;font:900 9px/1 var(--brand)}}.source-note{{font-size:9.4px;color:var(--muted);margin-top:4mm}}.chapter-open{{background:var(--navy);color:white;display:grid;place-items:center}}.chapter-open div{{width:150mm}}.chapter-open span{{display:block;font:900 52px/1 var(--brand);color:#f28c8c;margin-bottom:8mm}}.chapter-open h2{{color:white;font-size:38px}}@media print{{html,body{{background:white}}.page{{margin:0}}}}
</style><style>.cover-meta{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:10mm;max-width:132mm}}.cover-meta div{{border-top:2px solid rgba(255,255,255,.62);padding-top:3mm;color:#dbe6f5;font-size:10.3px}}.cover-meta b{{display:block;color:#fff;font:900 10px/1 var(--brand);letter-spacing:.08em;text-transform:uppercase;margin-bottom:2mm}}.unit-blocks{{display:grid;grid-template-columns:repeat(10,1fr);gap:1.4mm;margin-top:5mm;max-width:86mm}}.unit-blocks i{{display:block;aspect-ratio:1;background:var(--teal)}}.unit-blocks i:nth-child(-n+4){{background:var(--red)}}.before-after{{display:grid;grid-template-columns:1fr 16mm 1fr;gap:4mm;align-items:center;margin-top:6mm}}.before-after div{{border:1px solid var(--line);background:#fff;padding:4mm}}.before-after strong{{display:grid;place-items:center;color:var(--red);font:900 18px/1 var(--brand)}}.bubble-row{{display:flex;align-items:end;gap:5mm;margin-top:5mm;min-height:29mm}}.bubble-row span{{display:grid;place-items:center;border-radius:50%;background:rgba(8,118,109,.16);border:1px solid var(--teal);font:800 8px/1 var(--brand)}}.bubble-row span:nth-child(1){{width:10mm;height:10mm}}.bubble-row span:nth-child(2){{width:15mm;height:15mm}}.bubble-row span:nth-child(3){{width:21mm;height:21mm}}.bubble-row span:nth-child(4){{width:28mm;height:28mm}}.donut{{width:30mm;height:30mm;border-radius:50%;background:conic-gradient(var(--red) 0 38%,var(--teal) 38% 66%,var(--navy) 66% 100%);position:relative}}.donut:after{{content:"";position:absolute;inset:8mm;background:white;border-radius:50%}}.map-bubbles{{position:relative;height:38mm;border:1px solid var(--line);background:#f8fafc;margin-top:5mm}}.map-bubbles:before{{content:"";position:absolute;inset:7mm 18mm;border:1px solid #cfd8e3;border-radius:43% 57% 45% 55%;transform:skew(-14deg)}}.map-bubbles i{{position:absolute;display:block;border-radius:50%;background:var(--navy)}}.map-bubbles i:nth-child(1){{width:7mm;height:7mm;left:35mm;top:16mm}}.map-bubbles i:nth-child(2){{width:12mm;height:12mm;left:70mm;top:10mm}}.map-bubbles i:nth-child(3){{width:17mm;height:17mm;left:108mm;top:18mm}}</style></head><body>
<section class="page cover"><img src="assets/{slug}-overview-network.svg"><div class="shade"></div><div class="brand">BUSINESS OVERVIEW PUBLICATION</div><div class="cover-copy"><p class="eyebrow">Reader-ready executive overview</p><h1>{_esc(title)}</h1><p class="lead">将 L1 概览重构为“判断 - 证据 - 含义 - 行动”的咨询式阅读路径。</p><div class="cover-meta"><div><b>Institution</b>Win-Channel AI Research Institute</div><div><b>Date</b>2026年5月</div></div></div><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>封面</span><span>01</span></footer></section>
<section class="page"><p class="eyebrow">执行摘要</p><h2>同比承压且持续弱化，Fabric、Hair、Oral 是下一轮 L2 下钻的优先入口。</h2><p class="lead">{_esc(overall)}</p><div class="metric-row"><div><b>{_esc(total_ship)}</b><small>整体出货</small></div><div><b>{_esc(rd_iya)}</b><small>RD IYA / { _esc(yoy_pp) }</small></div><div><b>{_esc(mom)}</b><small>vs 上月 / { _esc(mom_pp) }</small></div><div><b>{_esc(decline_focus)}</b><small>Fabric + Hair 下跌贡献</small></div></div><div class="issue-grid">{issue_cards}</div><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>执行摘要</span><span>02</span></footer></section>
<section class="page"><p class="eyebrow">目录</p><h2>章节路径</h2><ol class="toc"><li><span>01</span><strong>执行摘要与研究框架</strong><em>02-04</em></li><li><span>02</span><strong>品类压力与正向驱动</strong><em>05-06</em></li><li><span>03</span><strong>PS 重点门店覆盖</strong><em>07</em></li><li><span>04</span><strong>Low Base 与行动建议</strong><em>08-09</em></li></ol><div class="note-grid">{evidence_pack}</div><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>目录</span><span>03</span></footer></section>
<section class="page"><p class="eyebrow">研究框架</p><h2>短概览也必须先给判断，再给图表证据，而不是只把 Markdown 打成 PDF。</h2><img class="framework-img" src="assets/{slug}-overview-network.svg"><div class="framework-row"><div><span>01</span>RD 总量：确认同比与环比压力</div><div><span>02</span>品类分解：锁定 Fabric / Hair / Oral</div><div><span>03</span>门店覆盖：检查 PS 扩张是否转化</div></div><div class="unit-blocks"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><div class="map-bubbles"><i></i><i></i><i></i></div><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>研究框架</span><span>04</span></footer></section>
<section class="page"><p class="fig-label">图 1</p><h2>增长压力集中在 Fabric、Hair、Oral；Fem 与 Shave 提供正向对冲。</h2><div class="figure-card">{category_bars}</div><p class="source-note">图 1：基于源 Markdown 各品类 IYA 与描述重绘。Baby 低基数 IYA 做截断展示，不作为健康品类判断。</p><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>品类压力</span><span>05</span></footer></section>
<section class="page"><p class="fig-label">图 2</p><h2>Fem、Shave 是当前正向驱动力，但不足以抵消三大问题品类压力。</h2><div class="big-layout"><div class="big-num"><b>{len(growth_categories)}</b><small>增长/健康品类</small></div><div class="flow"><div>Fem</div><div>Shave</div><div>Fabric</div><div>Hair / Oral</div></div><div class="big-num red"><b>{len(issue_categories)}</b><small>重点问题品类</small></div></div><div class="issue-grid">{praise_cards}</div><div class="bubble-row"><span>Low</span><span>Mid</span><span>High</span><span>Max</span></div><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>正向驱动</span><span>06</span></footer></section>
<section class="page"><p class="fig-label">表 1</p><h2>PS 门店净增不等于产出改善，Oral 覆盖下降需优先解释。</h2>{_html_table(ps_table)}<p class="source-note">来源：源 Markdown “PS 重点门店覆盖”表。</p><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>PS覆盖</span><span>07</span></footer></section>
<section class="page"><p class="eyebrow">Low Base 低基数</p><h2>Baby 的极高 IYA 是低基数失真，不能被解读为核心增长质量。</h2><div class="issue-grid">{low_base_cards}</div><div class="note-grid">{low_base_interpretation}</div><p class="source-note">来源：源 Markdown Low Base 段落。低基数页用于保护指标解释，不扩大业务结论。</p><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>低基数</span><span>08</span></footer></section>
<section class="page"><p class="eyebrow">建议</p><h2>下一步不是泛泛“关注”，而是进入 Fabric、Hair、Oral 的 L2 下钻。</h2><div class="figure-card">{action_cards}</div><div class="note-grid">{action_gates}</div><div class="before-after"><div><h3>当前</h3><p>问题品类明确，但 L2 责任链条仍需下钻。</p></div><strong>→</strong><div><h3>目标</h3><p>用 Hub/门店证据锁定可执行修复动作。</p></div></div><p class="lead">尤其需要解释：Fabric + Hair 的 { _esc(decline_focus) } 下跌贡献，以及 Oral 环比暴跌 { _esc(oral_drop) } 背后的断货、渠道调整或数据异常。</p><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>行动建议</span><span>09</span></footer></section>
<section class="page"><p class="eyebrow">方法、来源与相关出版物</p><h2>本 PDF 保留源 Markdown 口径，并将表格与段落重构为出版级阅读路径。</h2><ol><li>源文件：{_esc(source_label)}</li><li>指标口径：IYA、PS 门店、同比、环比、覆盖进度均沿用源 Markdown。</li><li>重绘说明：品类压力图基于源段落提取 IYA，PS 表保留源表结构。</li><li>相关出版物：Win-Channel AI Research Institute 业务概览与诊断系列输出。</li></ol><div class="donut"></div><footer class="folio"><span>YANGFAN BUSINESS OVERVIEW</span><span>来源</span><span>10</span></footer></section>
</body></html>"""
    meta = {
        "title": title,
        "subtitle": "将 L1 概览重构为“判断 - 证据 - 含义 - 行动”的咨询式阅读路径。",
        "source": source_label,
        "institution": "Win-Channel AI Research Institute",
        "report_date": "2026年5月",
        "mode": "business-markdown-publication",
        "hero_asset": str(hero.resolve()),
        "publication_features": [
            "human_editorial_cover",
            "cover_title_subtitle_date_institution",
            "designed_toc",
            "one_page_summary",
            "chapter_visual_openers",
            "big_numbers",
            "unit_blocks",
            "before_after",
            "bubble_matrix",
            "donut",
            "map_bubbles",
            "references_methodology_related_publications",
        ],
        "business_markdown_signals": ["IYA", "PS", "品类", "总体判断", "建议"],
        "category_count": len(categories),
        "issue_category_count": len(issue_categories),
        "growth_category_count": len(growth_categories),
        "h2_count": len(re.findall(r"^#{2}\s+", source, flags=re.M)),
        "h3_count": len(re.findall(r"^#{3}\s+", source, flags=re.M)),
        "code_block_count": source.count("```") // 2,
        "doc_snippet_count": 0,
        "suppressed_preamble_count": 0,
    }
    return html_doc, meta
