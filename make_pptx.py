from __future__ import annotations

import html
import os
import zipfile
from pathlib import Path


OUT = Path("SYL_pitch_deck_10_slides.pptx")
HERO = Path("assets/syl-hero.png")
EMU = 914400
SLIDE_W = 13.333333 * EMU
SLIDE_H = 7.5 * EMU


def emu(inches: float) -> int:
    return int(inches * EMU)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def color(hex_color: str) -> str:
    return hex_color.replace("#", "").upper()


def text_box(x, y, w, h, text, size=24, bold=False, color_hex="#EEFDF8", align="l"):
    weight = "<a:b/>" if bold else ""
    paragraphs = ""
    for line in text.split("\n"):
        paragraphs += f"""
        <a:p>
          <a:pPr algn="{align}"/>
          <a:r><a:rPr lang="vi-VN" sz="{int(size*100)}" dirty="0">{weight}<a:solidFill><a:srgbClr val="{color(color_hex)}"/></a:solidFill><a:latin typeface="Aptos Display"/><a:cs typeface="Arial"/></a:rPr><a:t>{esc(line)}</a:t></a:r>
        </a:p>"""
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{text_box.next_id()}" name="Text"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
      <p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
      <p:txBody><a:bodyPr wrap="square" anchor="t"/><a:lstStyle/>{paragraphs}</p:txBody>
    </p:sp>"""


def reset_ids():
    text_box._id = 10


def next_id():
    text_box._id += 1
    return text_box._id


text_box._id = 10
text_box.next_id = next_id


def rect(x, y, w, h, fill="#1F3022", line="#B8D8A4", alpha=85000, radius="roundRect"):
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{text_box.next_id()}" name="Panel"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
        <a:prstGeom prst="{radius}"><a:avLst/></a:prstGeom>
        <a:solidFill><a:srgbClr val="{color(fill)}"><a:alpha val="{alpha}"/></a:srgbClr></a:solidFill>
        <a:ln w="12700"><a:solidFill><a:srgbClr val="{color(line)}"><a:alpha val="52000"/></a:srgbClr></a:solidFill></a:ln>
      </p:spPr>
    </p:sp>"""


def bg(fill="#102018"):
    return f"""<p:bg><p:bgPr><a:solidFill><a:srgbClr val="{color(fill)}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>"""


def hero_pic():
    return f"""
    <p:pic>
      <p:nvPicPr><p:cNvPr id="{text_box.next_id()}" name="syl-hero.png"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
      <p:blipFill><a:blip r:embed="rId2"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
      <p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{int(SLIDE_W)}" cy="{int(SLIDE_H)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
    </p:pic>
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{text_box.next_id()}" name="Overlay"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{int(SLIDE_W)}" cy="{int(SLIDE_H)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="102018"><a:alpha val="30000"/></a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>
    </p:sp>"""


slides = [
    {
        "kicker": "AI Safety Camera · 2026",
        "title": "SYL",
        "lead": "Camera cảnh báo té ngã ở người già và phát hiện người lạ.",
        "chips": ["Fall detection", "Stranger alert", "Privacy by role", "B2B2C"],
        "hero": True,
    },
    {
        "kicker": "Problem",
        "title": "Người già ngã tại nhà, gia đình biết quá muộn.",
        "lead": "Camera chuyển động gây nhiễu; sản phẩm fall detection nhập khẩu lại đắt và chưa phổ biến tại Việt Nam.",
        "cards": [
            ("Phát hiện trễ", "Người đi làm hoặc sống xa không có tín hiệu đủ nhanh khi cha mẹ gặp sự cố."),
            ("Bỏ lỡ cảnh báo", "Motion alert quá nhiều khiến chủ nhà tắt thông báo và bỏ qua sự kiện thật."),
            ("Rủi ro riêng tư", "Camera gia đình có nguy cơ bị truy cập trái phép, lộ ảnh hoặc video nhạy cảm."),
        ],
    },
    {
        "kicker": "Market Signal",
        "title": "Thị trường chăm sóc người cao tuổi đã đủ lớn để bắt đầu.",
        "metrics": [
            ("16,1 triệu", "người cao tuổi tại Việt Nam theo dữ liệu dân cư quốc gia, cập nhật năm 2025."),
            (">16%", "dân số Việt Nam là người cao tuổi; dân số trung bình năm 2025 khoảng 102,3 triệu."),
            ("1,5–1,9 triệu", "người cao tuổi té ngã mỗi năm, tạo nhu cầu cảnh báo sớm tại nhà."),
        ],
        "quote": "Dân số già hóa nhanh + con cái đi làm xa + camera gia đình đã phổ biến tạo thời điểm phù hợp cho một lớp AI an toàn giá hợp lý.",
    },
    {
        "kicker": "Solution",
        "title": "SYL biến camera thành hệ thống chăm sóc chủ động.",
        "lead": "Gateway AI kết nối camera, phát hiện té ngã và người lạ, rồi gửi cảnh báo đúng người đúng quyền.",
        "cards": [
            ("Té ngã", "Ưu tiên recall cao để giảm nguy cơ bỏ sót ca ngã thật."),
            ("Người lạ", "Nhận diện người nhà và cảnh báo khi phát hiện đối tượng lạ."),
            ("Quyền 5 phút", "Bác sĩ được cấp quyền tạm thời khi có sự cố, sau đó tự thu hồi."),
        ],
    },
    {
        "kicker": "How It Works",
        "title": "Từ tín hiệu camera đến hành động khẩn cấp.",
        "steps": [
            ("01", "Camera", "Ghi nhận khu vực đã cấu hình."),
            ("02", "AI pose", "Phân tích tư thế, chuyển động, đối tượng."),
            ("03", "Cảnh báo", "Tạo alert theo mức ưu tiên."),
            ("04", "Liên hệ", "Gọi admin, gia đình hoặc bác sĩ."),
            ("05", "Thu hồi", "Quyền xem khẩn cấp hết hạn sau 5 phút."),
        ],
    },
    {
        "kicker": "Technical Edge",
        "title": "Ưu tiên không bỏ sót sự cố thật.",
        "metrics": [
            ("≥85%", "recall mục tiêu cho phát hiện té ngã."),
            ("83.05%", "F1 cho phát hiện người lạ trong thử nghiệm nội bộ."),
            ("85.96%", "recall cho stranger detection."),
        ],
        "quote": "Báo động giả có thể xử lý ở tầng xác nhận; bỏ sót ca ngã thật là rủi ro lớn hơn.",
    },
    {
        "kicker": "Users & Roles",
        "title": "Thiết kế cho gia đình, chủ nhà và người chăm sóc.",
        "cards": [
            ("Admin", "Thêm camera, phân quyền, kiểm tra lỗi trên dashboard."),
            ("Gia đình", "Chỉ xem camera được cấp phép và nhận cảnh báo liên quan."),
            ("Bác sĩ", "Xem tạm thời camera phòng người lớn tuổi khi có sự cố."),
            ("Người cao tuổi", "Không cần thao tác, không cần nhớ đeo thiết bị."),
        ],
    },
    {
        "kicker": "Business Model",
        "title": "Gateway AI + hợp tác phân phối B2B2C.",
        "prices": [
            ("Standard", "5.2tr", "Raspberry Pi 5 4GB + hệ thống SYL."),
            ("Plus", "8.5tr", "Raspberry Pi 5 8GB + hệ thống SYL."),
            ("Pro", "10tr", "8GB + nâng cấp bản mới nhất, miễn phí 6 tháng đầu."),
        ],
        "lead": "Giai đoạn đầu bán sỉ qua đối tác camera; dài hạn chuyển sang hoa hồng/doanh thu.",
    },
    {
        "kicker": "Competition",
        "title": "Nằm giữa camera phổ thông và hệ thống chuyên dụng đắt tiền.",
        "cards": [
            ("Camera phổ thông", "EZVIZ/IMOU mạnh về giá, nhưng chủ yếu motion/human detection."),
            ("Camera chuyên dụng", "Hanwha, i-PRO, Hikvision có fall detection nhưng chi phí cao hoặc khó mua tại VN."),
            ("SYL", "Tập trung fall detection + stranger alert, gateway phổ biến, dễ tích hợp."),
        ],
    },
    {
        "kicker": "Roadmap & Ask",
        "title": "Cần phần cứng thật, dữ liệu thật, đối tác thật.",
        "cards": [
            ("0–3 tháng", "Hoàn thiện MVP, dashboard admin, phân quyền, cảnh báo khẩn."),
            ("3–6 tháng", "Benchmark trên camera/gateway phổ biến, dữ liệu đồng ý/ẩn danh."),
            ("6–12 tháng", "Pilot với đối tác camera, chủ nhà hoặc cơ sở chăm sóc."),
            ("Kêu gọi", "Tìm 1–2 đối tác thử nghiệm, bộ camera/gateway và cố vấn AI biên."),
        ],
    },
]


def card_group(items, y=4.25, cols=3):
    out = ""
    gap = 0.18
    total_w = 11.5
    w = (total_w - gap * (cols - 1)) / cols
    x0 = 0.92
    for i, (head, body) in enumerate(items):
        row = i // cols
        col = i % cols
        x = x0 + col * (w + gap)
        yy = y + row * 1.35
        out += rect(x, yy, w, 1.08)
        out += text_box(x + 0.16, yy + 0.13, w - 0.32, 0.28, head, 18, True, "#EEFDF8")
        out += text_box(x + 0.16, yy + 0.45, w - 0.32, 0.46, body, 10.7, False, "#A8C4C0")
    return out


def metric_group(items):
    out = ""
    for i, (num, body) in enumerate(items):
        x = 0.92 + i * 3.93
        out += rect(x, 4.05, 3.65, 1.32, fill="#1A2B20", line="#B8D8A4")
        out += text_box(x + 0.18, 4.24, 3.25, 0.45, num, 31, True, "#70F0A8")
        out += text_box(x + 0.18, 4.83, 3.25, 0.35, body, 10.8, False, "#A8C4C0")
    return out


def build_slide(slide, index):
    reset_ids()
    shapes = bg()
    if slide.get("hero"):
        shapes += hero_pic()
        shapes += text_box(0.75, 0.45, 4.5, 0.3, "SYL", 15, True)
        shapes += text_box(0.92, 1.35, 6.8, 0.34, slide["kicker"], 12, True, "#59E0D0")
        shapes += text_box(0.88, 1.82, 4.1, 1.05, slide["title"], 72, True)
        shapes += text_box(0.96, 3.0, 6.5, 0.58, slide["lead"], 22, False, "#D8F4EF")
        x = 0.96
        for chip in slide["chips"]:
            shapes += rect(x, 3.85, 1.55, 0.36, fill="#E7D8B5", line="#B8D8A4", alpha=17000)
            shapes += text_box(x + 0.08, 3.94, 1.38, 0.13, chip, 8.5, True, "#D8F4EF", "ctr")
            x += 1.72
    else:
        shapes += text_box(0.75, 0.42, 4.2, 0.28, "SYL", 13, True, "#EEFDF8")
        shapes += text_box(0.92, 1.02, 4.8, 0.28, slide["kicker"], 11.5, True, "#59E0D0")
        shapes += text_box(0.88, 1.47, 11.5, 1.15, slide["title"], 34, True)
        if "lead" in slide:
            shapes += text_box(0.94, 2.78, 9.4, 0.55, slide["lead"], 15, False, "#CFE7E3")
        if "metrics" in slide:
            shapes += metric_group(slide["metrics"])
        if "cards" in slide:
            cols = 4 if len(slide["cards"]) == 4 else 3
            shapes += card_group(slide["cards"], y=4.1 if "lead" in slide else 3.9, cols=cols)
        if "prices" in slide:
            shapes += card_group([(f"{a} · {b}", c) for a, b, c in slide["prices"]], y=4.0, cols=3)
        if "steps" in slide:
            gap = 0.13
            w = (11.5 - gap * 4) / 5
            for i, (num, head, body) in enumerate(slide["steps"]):
                x = 0.92 + i * (w + gap)
                shapes += rect(x, 3.85, w, 1.65, fill="#1A2B20", line="#B8D8A4")
                shapes += text_box(x + 0.13, 4.04, w - 0.26, 0.26, num, 13, True, "#70F0A8")
                shapes += text_box(x + 0.13, 4.52, w - 0.26, 0.28, head, 16, True, "#EEFDF8")
                shapes += text_box(x + 0.13, 4.91, w - 0.26, 0.42, body, 9.7, False, "#A8C4C0")
        if "quote" in slide:
            shapes += rect(0.92, 5.78, 10.8, 0.55, fill="#2B3A24", line="#7FB069", alpha=76000)
            shapes += text_box(1.12, 5.93, 10.2, 0.22, slide["quote"], 13, False, "#D8F4EF")

    shapes += text_box(11.78, 6.86, 0.9, 0.16, f"{index:02d} / 10", 8.5, True, "#A8C4C0", "r")
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>{shapes}</p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def slide_rels(has_image=False):
    rels = [
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
    ]
    if has_image:
        rels.append('<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/syl-hero.png"/>')
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rels)}</Relationships>"""


def build_pptx():
    if not HERO.exists():
        raise FileNotFoundError(HERO)
    if OUT.exists():
        OUT.unlink()

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
""" + "".join(
        f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
        for i in range(1, len(slides) + 1)
    ) + "</Types>"

    presentation_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
""" + "".join(
        f'  <Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
        for i in range(1, len(slides) + 1)
    ) + """  <Relationship Id="rId12" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
</Relationships>"""

    presentation = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{''.join(f'<p:sldId id="{256+i}" r:id="rId{i+2}"/>' for i in range(len(slides)))}</p:sldIdLst>
  <p:sldSz cx="{int(SLIDE_W)}" cy="{int(SLIDE_H)}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle/>
</p:presentation>"""

    root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>"""

    master = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>"""

    master_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>"""

    layout = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>"""

    layout_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>"""

    theme = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="SYL Theme">
  <a:themeElements>
    <a:clrScheme name="SYL"><a:dk1><a:srgbClr val="102018"/></a:dk1><a:lt1><a:srgbClr val="EEFDF8"/></a:lt1><a:dk2><a:srgbClr val="1F3022"/></a:dk2><a:lt2><a:srgbClr val="A8C4C0"/></a:lt2><a:accent1><a:srgbClr val="59E0D0"/></a:accent1><a:accent2><a:srgbClr val="70F0A8"/></a:accent2><a:accent3><a:srgbClr val="FFD166"/></a:accent3><a:accent4><a:srgbClr val="FF8A9A"/></a:accent4><a:accent5><a:srgbClr val="6E8F55"/></a:accent5><a:accent6><a:srgbClr val="2B3A24"/></a:accent6><a:hlink><a:srgbClr val="59E0D0"/></a:hlink><a:folHlink><a:srgbClr val="70F0A8"/></a:folHlink></a:clrScheme>
    <a:fontScheme name="SYL"><a:majorFont><a:latin typeface="Aptos Display"/><a:ea typeface=""/><a:cs typeface="Arial"/></a:majorFont><a:minorFont><a:latin typeface="Aptos"/><a:ea typeface=""/><a:cs typeface="Arial"/></a:minorFont></a:fontScheme>
    <a:fmtScheme name="SYL"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
  </a:themeElements>
</a:theme>"""

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("ppt/presentation.xml", presentation)
        z.writestr("ppt/_rels/presentation.xml.rels", presentation_rels)
        z.writestr("ppt/slideMasters/slideMaster1.xml", master)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", master_rels)
        z.writestr("ppt/slideLayouts/slideLayout1.xml", layout)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", layout_rels)
        z.writestr("ppt/theme/theme1.xml", theme)
        z.write(HERO, "ppt/media/syl-hero.png")
        for i, slide in enumerate(slides, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", build_slide(slide, i))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels(has_image=bool(slide.get("hero"))))

    print(f"Wrote {OUT.resolve()} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build_pptx()
