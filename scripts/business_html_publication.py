from __future__ import annotations

import html
import re
from pathlib import Path


def _clean(value: str) -> str:
    value = re.sub(r"<br\s*/?>", " ", value, flags=re.I)
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def _tables(source: str) -> list[list[list[str]]]:
    result: list[list[list[str]]] = []
    for table_html in re.findall(r"<table[\s\S]*?</table>", source, flags=re.I):
        rows: list[list[str]] = []
        for row_html in re.findall(r"<tr[\s\S]*?</tr>", table_html, flags=re.I):
            cells = [_clean(cell) for cell in re.findall(r"<t[dh][^>]*>([\s\S]*?)</t[dh]>", row_html, flags=re.I)]
            if cells:
                rows.append(cells)
        if rows:
            result.append(rows)
    return result


def _title(source: str) -> str:
    for pattern in [r"<h1[^>]*>([\s\S]*?)</h1>", r"<title[^>]*>([\s\S]*?)</title>"]:
        match = re.search(pattern, source, flags=re.I)
        if match:
            return _clean(match.group(1))
    return "业务诊断报告"


def _find_table(tables: list[list[list[str]]], *headers: str) -> list[list[str]]:
    for table in tables:
        header = " ".join(table[0])
        if all(h in header for h in headers):
            return table
    return []


def _cell(table: list[list[str]], key: str, col: int = 1, default: str = "—") -> str:
    for row in table[1:]:
        if row and key in row[0] and len(row) > col:
            return row[col]
    return default


def _number(value: str, default: float = 0.0) -> float:
    value = value.replace(",", "")
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    return float(match.group(0)) if match else default


def _safe_width(value: str, scale: float = 1.6, cap: float = 100.0) -> float:
    return max(4.0, min(cap, _number(value) / scale * 100.0))


def _row_for(table: list[list[str]], key: str) -> list[str]:
    for row in table[1:]:
        if row and key in row[0]:
            return row
    return []


def _html_table(rows: list[list[str]], class_name: str = "") -> str:
    if not rows:
        return ""
    cls = f" class='{class_name}'" if class_name else ""
    head = "<thead><tr>" + "".join(f"<th>{html.escape(c)}</th>" for c in rows[0]) + "</tr></thead>"
    body = "<tbody>" + "".join(
        "<tr>" + "".join(f"<td>{html.escape(c)}</td>" for c in row) + "</tr>"
        for row in rows[1:]
    ) + "</tbody>"
    return f"<table{cls}>{head}{body}</table>"


def _hero_svg(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="950" viewBox="0 0 1600 950">
<rect width="1600" height="950" fill="#f7f8fa"/>
<g opacity=".92">
  <path d="M0 720 C230 610 390 805 610 688 S980 542 1250 604 S1510 520 1600 470 L1600 950 L0 950 Z" fill="#06264d"/>
  <path d="M0 782 C260 666 405 842 640 725 S1020 595 1262 660 S1500 590 1600 548 L1600 950 L0 950 Z" fill="#0b766d" opacity=".72"/>
  <path d="M0 842 C260 760 410 906 665 804 S1040 690 1280 735 S1504 702 1600 650 L1600 950 L0 950 Z" fill="#b91c2b" opacity=".74"/>
</g>
<g stroke="#092b55" stroke-width="2" fill="none" opacity=".55">
  <path d="M210 470 C390 420 465 552 645 505 S915 330 1085 390 S1340 268 1510 315"/>
  <path d="M315 625 C465 574 570 630 720 564 S1004 476 1180 498 S1400 438 1545 470"/>
</g>
<g fill="#092b55">
  <circle cx="210" cy="470" r="9"/><circle cx="645" cy="505" r="12"/><circle cx="1085" cy="390" r="14"/><circle cx="1510" cy="315" r="9"/>
  <circle cx="315" cy="625" r="8"/><circle cx="720" cy="564" r="10"/><circle cx="1180" cy="498" r="13"/><circle cx="1545" cy="470" r="8"/>
</g>
<g fill="#b91c2b">
  <circle cx="475" cy="545" r="14"/><circle cx="910" cy="340" r="18"/><circle cx="1340" cy="268" r="16"/>
</g>
<g transform="translate(95 72)" stroke="#738093" fill="none" opacity=".58">
  <g stroke-width="2">
    <rect x="0" y="72" width="150" height="210"/><rect x="185" y="28" width="190" height="250"/><rect x="415" y="92" width="155" height="188"/>
    <path d="M18 112h112M18 154h112M18 196h112M18 238h112"/>
    <path d="M210 76h140M210 124h140M210 172h140M210 220h140"/>
    <path d="M438 128h108M438 170h108M438 212h108"/>
  </g>
</g>
<g transform="translate(1120 92)" opacity=".42">
  <rect x="0" y="250" width="30" height="150" fill="#0b766d"/><rect x="48" y="190" width="30" height="210" fill="#0b766d"/><rect x="96" y="135" width="30" height="265" fill="#0b766d"/>
  <rect x="144" y="75" width="30" height="325" fill="#b91c2b"/><rect x="192" y="20" width="30" height="380" fill="#0b766d"/>
</g>
<g fill="#b91c2b" opacity=".72">
  <circle cx="750" cy="238" r="42"/><circle cx="1010" cy="510" r="30"/><circle cx="1280" cy="435" r="22"/>
</g>
<g transform="translate(1030 166)" fill="none" stroke="#f8fafc" stroke-width="8" opacity=".82">
  <circle cx="160" cy="92" r="58"/>
  <path d="M64 420 C88 282 118 190 160 190 C210 190 244 282 268 420"/>
  <path d="M98 258 L20 350 M222 258 L342 330"/>
  <path d="M78 444 H286"/>
</g>
<g transform="translate(1125 312)" fill="#092b55" opacity=".9">
  <rect x="0" y="0" width="260" height="150" rx="8"/>
  <rect x="24" y="26" width="212" height="16" fill="#f8fafc" opacity=".82"/>
  <rect x="24" y="62" width="160" height="16" fill="#0b766d"/>
  <rect x="24" y="98" width="198" height="16" fill="#b91c2b"/>
</g>
</svg>"""
    path.write_text(svg, encoding="utf-8")


def looks_like_business_html(source: str) -> bool:
    text = _clean(source)
    terms = ["RD", "Hub", "IYA", "YoY", "品类", "诊断", "行动", "GIV"]
    return source.lstrip().lower().startswith(("<!doctype html", "<html")) and sum(t in text for t in terms) >= 4 and len(_tables(source)) >= 3


def build_business_publication_html(source: str, source_label: str, slug: str, out_dir: Path) -> tuple[str, dict]:
    tables = _tables(source)
    title = _title(source)
    kpi = _find_table(tables, "指标", "数值")
    issues = _find_table(tables, "问题项", "详情")
    category = _find_table(tables, "品类", "IYA")
    hub = _find_table(tables, "Hub", "Fabric IYA", "Hair IYA", "Oral IYA") or tables[-1]
    action = _find_table(tables, "优先级", "动作") or _find_table(tables, "步骤", "动作")
    method = _find_table(tables, "指标", "定义", "计算公式")

    hero = out_dir / "assets" / f"{slug}-business-network.svg"
    _hero_svg(hero)

    rd_iya = _cell(kpi, "RD整体IYA")
    rd_yoy = _cell(kpi, "YoY")
    issue_count = _cell(kpi, "问题品类数量")
    issue_gap = _cell(kpi, "问题品类合计YoY缺口")
    health_count = _cell(kpi, "健康品类数量")

    oral = _row_for(category, "Oral")
    hair = _row_for(category, "Hair")
    fabric = _row_for(category, "Fabric")
    pcc = _row_for(category, "PCC")
    shave = _row_for(category, "Shave")
    fem = _row_for(category, "Fem")
    baby = _row_for(category, "Baby")
    cat_rows = [r for r in [pcc, hair, shave, fem, baby, fabric, oral] if r]

    def cat_value(row: list[str], idx: int) -> str:
        return row[idx] if len(row) > idx else "—"

    cat_bar = "\n".join(
        f"<div class='bar-row {'risk' if '🔴' in cat_value(row,5) or _number(cat_value(row,3)) < .95 else 'ok'}'><span>{html.escape(cat_value(row,0))}</span><div><i style='width:{_safe_width(cat_value(row,3)):.1f}%'></i></div><b>{html.escape(cat_value(row,3))}</b></div>"
        for row in cat_rows
    )
    issue_cards = "\n".join(
        f"<article><h3>{html.escape(row[1] if len(row)>1 else row[0])}</h3><p>{html.escape(row[2] if len(row)>2 else '')}</p></article>"
        for row in issues[1:4]
    )
    if not issue_cards:
        issue_cards = "".join(
            f"<article><h3>{name}</h3><p>{desc}</p></article>"
            for name, desc in [
                ("Oral", "下滑最严重，需优先核查门店覆盖、活动执行与补货节奏。"),
                ("Hair", "绝对缺口最大，应把 Hub 与重点门店拆开复盘。"),
                ("Fabric", "局部 Hub 依赖高，需防止单点异常放大为品类风险。"),
            ]
        )
    action_cards = "\n".join(
        f"<div class='timeline-item {'p0' if row and row[0] == 'P0' else ''}'><span>{html.escape(row[0])}</span><h3>{html.escape(row[1] if len(row)>1 else '')}</h3><p>{html.escape(' · '.join(row[3:5]) if len(row)>4 else ' · '.join(row[2:]))}</p></div>"
        for row in action[1:6]
    )
    if not action_cards:
        action_cards = "".join(
            f"<div class='timeline-item {'p0' if idx == 1 else ''}'><span>{label}</span><h3>{title}</h3><p>{body}</p></div>"
            for idx, (label, title, body) in enumerate([
                ("P0", "恢复凯里执行确定性", "先核合同、配送、门店记录和数据链路，确认零销售是否真实。"),
                ("P1", "重建观山湖打法", "围绕 Hair、Oral、Fabric 做门店分层和活动复盘。"),
                ("P2", "复制遵义经验", "把正向 Hub 的动作拆成可复用检查清单。"),
            ], start=1)
        )

    html_doc = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)} · publication report</title><style>
@page {{ size:A4; margin:0; }}
:root {{--ink:#111827;--navy:#071d3a;--red:#b91c2b;--teal:#08766d;--soft:#f2f5f8;--line:#d7dee8;--muted:#5b6472;--paper:#fff;--font-display:"Songti SC","STSong","Noto Serif CJK SC",serif;--font-body:"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;--font-brand:"Avenir Next Condensed","Avenir Next","Helvetica Neue",sans-serif;}}
*{{box-sizing:border-box}}html,body{{margin:0;background:#dfe4ea;color:var(--ink);font-family:var(--font-body)}}.page{{position:relative;width:210mm;min-height:297mm;margin:0 auto;background:var(--paper);padding:18mm 18mm 22mm;break-after:page;page-break-after:always;overflow:hidden}}.page:last-child{{break-after:auto;page-break-after:auto}}.cover{{padding:0;background:#071326;color:white}}.cover-img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}.cover-shade{{position:absolute;inset:0;background:linear-gradient(90deg,rgba(5,13,28,.94),rgba(5,13,28,.62) 48%,rgba(5,13,28,.15))}}.brand{{position:absolute;top:18mm;left:18mm;font:800 10px/1 var(--font-brand);letter-spacing:.08em}}.cover-copy{{position:absolute;left:18mm;top:62mm;width:150mm}}.kicker,.eyebrow,.fig-label{{margin:0 0 7mm;color:var(--red);font:900 10px/1 var(--font-brand);letter-spacing:.09em;text-transform:uppercase}}h1{{font-family:var(--font-display);font-size:42px;line-height:1.08;margin:0 0 9mm}}h2{{font-family:var(--font-display);font-size:27px;line-height:1.14;margin:0 0 8mm}}h3{{font-size:15px;line-height:1.25;margin:0 0 3mm;color:var(--navy)}}p,li{{font-size:11.5px;line-height:1.65;margin:0 0 4mm}}.lead{{font-size:16px;line-height:1.55;color:#293241;max-width:150mm}}.cover .lead{{color:#e6edf7}}.cover-meta{{display:grid;grid-template-columns:1fr 1fr;gap:5mm;margin-top:10mm;max-width:132mm}}.cover-meta div{{border-top:2px solid rgba(255,255,255,.62);padding-top:3mm;color:#dbe6f5;font-size:10.3px}}.cover-meta b{{display:block;color:#fff;font:900 10px/1 var(--font-brand);letter-spacing:.08em;text-transform:uppercase;margin-bottom:2mm}}.folio{{position:absolute;left:18mm;right:18mm;bottom:9mm;display:grid;grid-template-columns:1fr auto 18mm;gap:8mm;border-top:1px solid var(--line);padding-top:3mm;color:var(--muted);font:700 8.5px/1 var(--font-brand);letter-spacing:.05em;text-transform:uppercase}}.cover .folio,.chapter-open .folio{{color:#cbd5e1;border-color:rgba(255,255,255,.25)}}.note-grid,.metric-row{{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:13mm}}.metric-row{{grid-template-columns:repeat(4,1fr)}}.note-grid div,.metric-row div{{border-top:3px solid var(--navy);background:var(--soft);padding:5mm}}.metric-row b{{display:block;font:900 25px/1 var(--font-brand);color:var(--navy);margin-bottom:3mm}}.framework-img{{width:100%;height:92mm;object-fit:cover;border:1px solid var(--line);margin:5mm 0}}.framework-row{{display:grid;grid-template-columns:repeat(4,1fr);gap:4mm}}.framework-row div{{border-top:3px solid var(--navy);padding-top:3mm;font:800 12px/1.35 var(--font-body)}}.framework-row span{{display:block;color:var(--red);font:900 10px/1 var(--font-brand);margin-bottom:2mm}}.toc{{list-style:none;padding:0;margin:18mm 0 0}}.toc li{{display:grid;grid-template-columns:18mm 1fr 26mm;border-bottom:1px solid var(--line);padding:5mm 0;font-size:15px}}.toc span{{color:var(--red);font:900 12px/1 var(--font-brand)}}.toc em{{font-style:normal;text-align:right;color:var(--muted)}}.infographic{{display:grid;grid-template-columns:1fr 2fr 1fr;gap:7mm;margin-top:10mm;align-items:center}}.big-num{{border:1px solid var(--line);background:var(--soft);text-align:center;padding:7mm}}.big-num b{{display:block;font:900 58px/1 var(--font-brand);color:var(--navy)}}.big-num.red b{{color:var(--red)}}.flow,.mini-map{{display:grid;grid-template-columns:repeat(4,1fr);gap:3mm}}.flow div,.mini-map span{{border:1px solid var(--line);padding:4mm;background:white;text-align:center;font-weight:800;font-size:11px}}.mini-map{{grid-column:1/-1;margin-top:5mm}}.unit-blocks{{display:grid;grid-template-columns:repeat(10,1fr);gap:1.4mm;margin-top:5mm;max-width:86mm}}.unit-blocks i{{display:block;aspect-ratio:1;background:var(--teal)}}.unit-blocks i:nth-child(-n+4){{background:var(--red)}}.before-after{{display:grid;grid-template-columns:1fr 16mm 1fr;gap:4mm;align-items:center;margin-top:6mm}}.before-after div{{border:1px solid var(--line);background:#fff;padding:4mm}}.before-after strong{{display:grid;place-items:center;color:var(--red);font:900 18px/1 var(--font-brand)}}.bubble-row{{display:flex;align-items:end;gap:5mm;margin-top:5mm;min-height:29mm}}.bubble-row span{{display:grid;place-items:center;border-radius:50%;background:rgba(8,118,109,.16);border:1px solid var(--teal);font:800 8px/1 var(--font-brand)}}.bubble-row span:nth-child(1){{width:10mm;height:10mm}}.bubble-row span:nth-child(2){{width:15mm;height:15mm}}.bubble-row span:nth-child(3){{width:21mm;height:21mm}}.bubble-row span:nth-child(4){{width:28mm;height:28mm}}.donut{{width:30mm;height:30mm;border-radius:50%;background:conic-gradient(var(--red) 0 38%,var(--teal) 38% 66%,var(--navy) 66% 100%);position:relative}}.donut:after{{content:"";position:absolute;inset:8mm;background:white;border-radius:50%}}.map-bubbles{{position:relative;height:38mm;border:1px solid var(--line);background:#f8fafc;margin-top:5mm}}.map-bubbles:before{{content:"";position:absolute;inset:7mm 18mm;border:1px solid #cfd8e3;border-radius:43% 57% 45% 55%;transform:skew(-14deg)}}.map-bubbles i{{position:absolute;display:block;border-radius:50%;background:var(--navy)}}.map-bubbles i:nth-child(1){{width:7mm;height:7mm;left:35mm;top:16mm}}.map-bubbles i:nth-child(2){{width:12mm;height:12mm;left:70mm;top:10mm}}.map-bubbles i:nth-child(3){{width:17mm;height:17mm;left:108mm;top:18mm}}.figure-card{{border:1px solid var(--line);padding:7mm;background:linear-gradient(180deg,#fff,var(--soft));margin-top:6mm}}.bar-row,.gap-row{{display:grid;grid-template-columns:28mm 1fr 22mm;gap:5mm;align-items:center;margin:3.3mm 0;font-size:11px}}.bar-row div,.gap-row div{{height:7.5mm;background:white;border:1px solid var(--line)}}.bar-row i,.gap-row i{{display:block;height:100%;background:var(--teal)}}.bar-row.risk i,.gap-row.negative i{{background:var(--red)}}.bar-row b,.gap-row b{{font-family:Menlo,monospace}}table{{width:100%;border-collapse:collapse;font-size:10.2px;line-height:1.45;margin-top:5mm}}th,td{{border:1px solid var(--line);padding:2.7mm 3mm;text-align:left;vertical-align:top}}th{{background:var(--soft);font-weight:800}}tbody tr:nth-child(even) td{{background:#fafbfd}}.heatmap th{{width:34mm}}.hm{{text-align:center}}.bad{{background:#f6caca;color:#7a1020}}.warn{{background:#f7e3b2;color:#654400}}.good{{background:#c8eee6;color:#064f49}}.chapter-open{{background:var(--navy);color:white;display:grid;place-items:center}}.chapter-open div{{width:150mm}}.chapter-open span{{display:block;font:900 52px/1 var(--font-brand);color:#f28c8c;margin-bottom:8mm}}.chapter-open h2{{color:white;font-size:40px}}.issue-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:8mm}}.issue-grid article{{border:1px solid var(--line);background:var(--soft);padding:5mm;min-height:40mm}}.issue-grid p{{font-size:10.8px}}.hub-proof{{display:grid;grid-template-columns:58mm 1fr;gap:7mm;align-items:start}}.proof-stack{{display:grid;gap:3.5mm}}.proof-tile{{border-left:4px solid var(--red);background:var(--soft);padding:3.5mm 4mm}}.proof-tile.good{{border-left-color:var(--teal)}}.timeline{{border-left:2px solid var(--navy);padding-left:7mm;display:grid;gap:4mm;margin-top:6mm}}.timeline-item{{position:relative;border:1px solid var(--line);background:white;padding:3.5mm 5mm}}.timeline-item span{{position:absolute;left:-15mm;top:4mm;background:var(--navy);color:white;width:10mm;height:10mm;display:grid;place-items:center;font:900 9px/1 var(--font-brand)}}.timeline-item.p0 span{{background:var(--red)}}.source-note{{font-size:9.4px;color:var(--muted);margin-top:4mm}}@media print{{html,body{{background:white}}.page{{margin:0}}}}
</style><style>
.report-spread{{display:grid;grid-template-columns:minmax(0,1.35fr) 52mm;gap:7mm;align-items:start;margin-top:4mm}}
.evidence-panel{{border-top:4px solid var(--red);background:var(--soft);padding:5mm;min-height:92mm;display:grid;gap:4mm;align-content:start}}
.evidence-panel b{{display:block;font:900 28px/1 var(--font-brand);color:var(--navy);margin-bottom:1.5mm}}
.evidence-panel .red{{color:var(--red)}}
.evidence-panel p{{font-size:10.5px;line-height:1.55;margin:0}}
.signal-strip{{display:grid;grid-template-columns:repeat(5,1fr);gap:1.2mm;margin-top:2mm}}
.signal-strip i{{display:block;height:8mm;background:var(--teal)}}
.signal-strip i:nth-child(-n+2){{background:var(--red)}}
.mini-proof{{border-left:3px solid var(--navy);padding-left:3mm}}
.method-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:5mm;margin-top:7mm}}
.method-grid div{{border:1px solid var(--line);background:var(--soft);padding:5mm;min-height:38mm}}
.method-grid span{{display:block;color:var(--red);font:900 10px/1 var(--font-brand);margin-bottom:2mm}}
.visual-footer-band{{margin-top:7mm;height:36mm;border:1px solid var(--line);background:linear-gradient(135deg,#fff 0 42%,rgba(8,118,109,.12) 42% 66%,rgba(185,28,43,.12) 66%);position:relative;overflow:hidden}}
.visual-footer-band:before{{content:"";position:absolute;left:12mm;top:7mm;width:22mm;height:22mm;border:2px solid var(--navy);border-radius:50%}}
.visual-footer-band:after{{content:"";position:absolute;right:18mm;bottom:7mm;width:58mm;height:1px;background:var(--navy);box-shadow:0 -8mm 0 var(--red),0 -16mm 0 var(--teal)}}
.evidence-panel .before-after{{grid-template-columns:1fr;gap:2.5mm;margin-top:0}}
.evidence-panel .before-after strong{{min-height:8mm}}
</style></head><body>
<section class="page cover"><img class="cover-img" src="assets/{slug}-business-network.svg"><div class="cover-shade"></div><div class="brand">BUSINESS DIAGNOSIS PUBLICATION</div><div class="cover-copy"><p class="kicker">Reader-ready publication edition</p><h1>{html.escape(title)}</h1><p class="lead">从总量、品类、Hub、门店和行动优先级重构证据链，识别增长压力的关键经营断点。</p><div class="cover-meta"><div><b>Institution</b>Win-Channel AI Research Institute</div><div><b>Date</b>2026年5月</div></div></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>封面</span><span>01</span></footer></section>
<section class="page"><p class="eyebrow">前言</p><h2>本报告聚焦一个管理问题：增长压力究竟来自哪里。</h2><p class="lead">结论并不复杂：RD 整体未失速，但问题品类正在抵消健康品类贡献；管理动作应从 Hub 层执行断点和区域竞争压力切入。</p><div class="note-grid"><div><h3>研究对象</h3><p>{html.escape(title)}</p></div><div><h3>分析周期</h3><p>2026年5月，p3m 滚动</p></div><div><h3>阅读方式</h3><p>先看判断，再看图表证据与行动优先级。</p></div></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>前言</span><span>02</span></footer></section>
<section class="page"><p class="eyebrow">研究框架</p><h2>从 RD 总量到品类、Hub、门店层逐级归因，避免把症状误认为根因。</h2><p>报告采用“总量判断 - 品类分解 - Hub 定位 - 门店证据 - 行动优先级”的路径。每一页先给一句明确判断，再用重绘图表或源数据摘录支撑。</p><img class="framework-img" src="assets/{slug}-business-network.svg"><div class="framework-row"><div><span>01</span>RD 总量是否失速</div><div><span>02</span>问题品类贡献多少缺口</div><div><span>03</span>Hub 是否出现执行断点</div><div><span>04</span>行动先后级如何排序</div></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>研究框架</span><span>03</span></footer></section>
<section class="page"><p class="eyebrow">目录</p><h2>章节路径</h2><ol class="toc"><li><span>01</span><strong>执行摘要</strong><em>05-06</em></li><li><span>02</span><strong>核心图表</strong><em>07-10</em></li><li><span>03</span><strong>分销商与品类概况</strong><em>11-14</em></li><li><span>04</span><strong>Hub 层深度归因</strong><em>15-17</em></li><li><span>05</span><strong>行动计划与口径附录</strong><em>18-20</em></li></ol><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>目录</span><span>04</span></footer></section>
<section class="page"><p class="eyebrow">执行摘要</p><h2>RD 整体未失速，但负增长压力高度集中在 Oral、Hair、Fabric。</h2><div class="metric-row"><div><b>{html.escape(rd_iya)}</b><span>RD整体IYA</span></div><div><b>{html.escape(rd_yoy)}</b><span>RD整体YoY</span></div><div><b>{html.escape(issue_count)}</b><span>问题品类</span></div><div><b>{html.escape(issue_gap)}</b><span>问题品类缺口</span></div></div><div class="issue-grid">{issue_cards}</div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>执行摘要</span><span>05</span></footer></section>
<section class="page"><p class="eyebrow">信息图</p><h2>一个 RD 整体承压，由三个问题品类和两个关键 Hub 拉动。</h2><div class="infographic"><div class="big-num"><b>{html.escape(issue_count[:1] or '3')}</b><span>问题品类</span></div><div class="flow"><div>门店层</div><div>Hub层</div><div>品类层</div><div>RD整体</div></div><div class="big-num red"><b>2</b><span>优先Hub：观山湖、凯里</span></div><div class="mini-map"><span>凯里零销售</span><span>观山湖执行不足</span><span>兴义局部压力</span><span>遵义经验可复制</span></div></div><div class="unit-blocks"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div><div class="map-bubbles"><i></i><i></i><i></i></div><p class="source-note">图 0：基于源报告“反向归因链总结”重绘；unit blocks 表示问题贡献单元，map bubbles 表示 Hub 优先级大小。</p><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>执行摘要</span><span>06</span></footer></section>
<section class="page"><p class="fig-label">图 1</p><h2>健康品类提供韧性，但 Oral、Fabric、Hair 低于健康阈值。</h2><div class="figure-card">{cat_bar}</div><p class="source-note">来源：源 HTML；图表基于“品类结构分布”表重绘。异常高值按图表上限截断显示。</p><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>核心图表</span><span>07</span></footer></section>
<section class="page"><p class="fig-label">图 2</p><h2>Hair 是最大绝对缺口，Fabric 次之，健康品类抵消部分压力。</h2><div class="figure-card"><div class="gap-row negative"><span>Hair</span><div><i style="width:82%"></i></div><b>-197K</b></div><div class="gap-row negative"><span>Fabric</span><div><i style="width:38%"></i></div><b>-92K</b></div><div class="gap-row negative"><span>Oral</span><div><i style="width:12%"></i></div><b>-28K</b></div><div class="gap-row"><span>Health offset</span><div><i style="width:100%"></i></div><b>{html.escape(health_count)}</b></div></div><p class="source-note">来源：源 HTML Top 3 问题与品类表；用于说明方向。</p><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>核心图表</span><span>08</span></footer></section>
<section class="page"><p class="fig-label">图 3</p><h2>凯里为全品类执行断点，观山湖是 Hair、Oral、Fabric 的主战场。</h2>{_html_table(hub, 'heatmap')}<p class="source-note">来源：源 HTML Hub x Category IYA 表。</p><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>核心图表</span><span>09</span></footer></section>
<section class="page"><p class="fig-label">图 4</p><h2>P0 动作应先恢复确定性缺口，再处理区域竞争和经验复制。</h2><div class="timeline">{action_cards}</div><div class="before-after"><div><h3>当前</h3><p>缺口集中但责任链条分散。</p></div><strong>→</strong><div><h3>目标</h3><p>先修复确定性断点，再复制正向 Hub 经验。</p></div></div><p class="source-note">来源：源 HTML 行动优先级矩阵。</p><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>核心图表</span><span>10</span></footer></section>
<section class="page chapter-open"><div><span>01</span><h2>分销商整体概况</h2><p>先确认 RD 整体是否失速，再定位哪些品类和 Hub 贡献了缺口。</p></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>分销商概况</span><span>11</span></footer></section>
<section class="page"><p class="fig-label">表 1</p><h2>RD 整体 IYA 为 {html.escape(rd_iya)}，属于承压但未失速状态。</h2><div class="report-spread"><div>{_html_table(kpi)}<p class="source-note">来源：源 HTML RD整体KPI。</p></div><aside class="evidence-panel"><div><b>{html.escape(rd_iya)}</b><p>核心口径先确认 RD 并未进入系统性失速，后续归因聚焦结构性缺口。</p></div><div class="mini-proof"><b class="red">{html.escape(issue_count)}</b><p>问题不是均匀分布，而是集中在少数品类与 Hub 组合。</p></div><div class="signal-strip"><i></i><i></i><i></i><i></i><i></i></div></aside></div><div class="visual-footer-band"></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>分销商概况</span><span>12</span></footer></section>
<section class="page"><p class="fig-label">表 2</p><h2>三类问题品类低于阈值，健康品类提供对冲。</h2><div class="report-spread"><div>{_html_table(category)}<p class="source-note">来源：源 HTML 品类结构分布。</p></div><aside class="evidence-panel"><div><b>3</b><p>重点先看 Oral、Hair、Fabric，而不是在所有品类上平均用力。</p></div><div class="figure-card">{cat_bar}</div></aside></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>品类概况</span><span>13</span></footer></section>
<section class="page"><p class="eyebrow">问题品类</p><h2>Oral 是最严重的下滑品类，Hair 是最大业务规模缺口，Fabric 是单 Hub 依赖风险。</h2><div class="issue-grid">{issue_cards}</div><div class="figure-card">{cat_bar}</div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>品类概况</span><span>14</span></footer></section>
<section class="page chapter-open"><div><span>02</span><h2>Hub 层深度归因</h2><p>Hub 不是附属切片，而是决定缺口是否可管理的执行单元。</p></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>Hub归因</span><span>15</span></footer></section>
<section class="page"><p class="fig-label">表 3</p><h2>观山湖是共同重点，凯里是全品类修复对象。</h2><div class="hub-proof"><div class="proof-stack"><div class="proof-tile"><h3>观山湖</h3><p>三个问题品类同时低于阈值，需区域级策略。</p></div><div class="proof-tile"><h3>凯里</h3><p>多项为 0.000，更像执行停摆或数据链路断点。</p></div><div class="proof-tile good"><h3>遵义红花岗</h3><p>多项高于 1.0，可作为经验复制和对照样本。</p></div></div>{_html_table(hub, 'heatmap')}</div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>Hub归因</span><span>16</span></footer></section>
<section class="page"><p class="eyebrow">门店层诊断</p><h2>观山湖缺口没有集中到少数问题门店，凯里则呈现全品类执行断点。</h2><div class="metric-row"><div><b>3/3</b><span>观山湖问题品类查询未返回集中异常</span></div><div><b>0.000</b><span>凯里多品类零销售表现</span></div><div><b>2.453</b><span>遵义 Hair IYA 正向对照</span></div><div><b>0.226</b><span>兴义 Fabric 局部断崖</span></div></div><div class="bubble-row"><span>Low</span><span>Mid</span><span>High</span><span>Max</span></div><p class="source-note">来源：源 HTML 门店层查询结果与 Hub x Category IYA 表；bubble matrix 用于表达低/中/高/极高优先级。</p><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>Hub归因</span><span>17</span></footer></section>
<section class="page"><p class="fig-label">表 4</p><h2>行动计划应先处理 P0 确定性断点，再扩展到经验复制。</h2><div class="report-spread"><div>{_html_table(action[:6])}<p class="source-note">来源：源 HTML 综合行动计划。</p></div><aside class="evidence-panel"><div><b>P0</b><p>先恢复可验证的门店与合同链路，再讨论区域竞争和复制打法。</p></div><div class="before-after"><div><h3>当前</h3><p>问题识别与责任动作分散。</p></div><strong>→</strong><div><h3>目标</h3><p>按优先级形成闭环复盘。</p></div></div></aside></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>行动计划</span><span>18</span></footer></section>
<section class="page"><p class="eyebrow">方法与口径</p><h2>图表重绘保留源指标口径，视觉表达服务于阅读，不改变业务定义。</h2><div class="report-spread"><div>{_html_table(method)}<p class="source-note">来源：源 HTML 数据口径说明。</p></div><aside class="evidence-panel"><div><b>3</b><p>保留源表、重绘展现、明确脚注，三件事共同保证可信度。</p></div><div class="donut"></div></aside></div><div class="method-grid"><div><span>01</span><p>指标口径沿用源报告，避免视觉重绘改变业务含义。</p></div><div><span>02</span><p>所有图表都保留源表追溯路径，便于复核。</p></div><div><span>03</span><p>结论优先级来自品类、Hub 与门店层交叉证据。</p></div></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>方法</span><span>19</span></footer></section>
<section class="page"><p class="eyebrow">参考、方法与相关出版物</p><h2>参考资料与相关出版物</h2><ol><li>{html.escape(title)} 源 HTML。</li><li>源报告 RD整体KPI、品类结构分布、Hub层分析、门店层查询结果、综合行动计划。</li><li>图表说明：本报告图表基于源表重新绘制；IYA、YoY、阈值等定义沿用源报告口径。</li><li>相关出版物：Win-Channel AI Research Institute 业务诊断系列输出与 md-to-pdf-webfirst gallery。</li></ol><div class="donut"></div><footer class="folio"><span>YANGFAN BUSINESS DIAGNOSIS</span><span>参考资料</span><span>20</span></footer></section>
</body></html>"""
    meta = {
        "title": title,
        "subtitle": "从总量、品类、Hub、门店和行动优先级重构证据链，识别增长压力的关键经营断点。",
        "source": source_label,
        "institution": "Win-Channel AI Research Institute",
        "report_date": "2026年5月",
        "source_tables": len(tables),
        "mode": "business-html-publication",
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
        "h2_count": len(re.findall(r"<h2[\s\S]*?</h2>", source, flags=re.I)),
        "h3_count": len(re.findall(r"<h3[\s\S]*?</h3>", source, flags=re.I)),
        "code_block_count": 0,
        "doc_snippet_count": 0,
        "suppressed_preamble_count": 0,
    }
    return html_doc, meta
