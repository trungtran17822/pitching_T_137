from __future__ import annotations

import html
import zipfile
from pathlib import Path


OUT = Path("SYL_pitch_deck_18_slides.pptx")
HERO = Path("assets/syl-hero.png")
DIAGRAM = Path("assets/overview-diagram.png")
LOGO = Path("assets/logo.jpg")
DEMO_VIDEO = Path("demo.mp4")
SURVEY_IMAGES = {
    "missed_alert": Path("assets/survey/missed-alert.png"),
    "support_solution": Path("assets/survey/support-solution.png"),
    "early_access": Path("assets/survey/early-access.png"),
    "false_alarm": Path("assets/survey/false-alarm.png"),
}
TECH_IMAGES = {
    "val_epoch": Path("assets/tech/val-epoch.jpg"),
    "threshold": Path("assets/tech/threshold.jpg"),
    "test_clf": Path("assets/tech/test-clf.jpg"),
    "test_distribution": Path("assets/tech/test-distribution.jpg"),
    "validation_metrics": Path("assets/tech/validation-metrics.jpg"),
    "confusion_matrix": Path("assets/tech/confusion-matrix.jpg"),
    "fall_probability": Path("assets/tech/fall-probability.jpg"),
    "eval_retrain": Path("assets/tech/eval-retrain.jpg"),
}
EMU = 914400
SLIDE_W = 13.333333 * EMU
SLIDE_H = 7.5 * EMU


def emu(inches: float) -> int:
    return int(inches * EMU)


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def color(value: str) -> str:
    return value.replace("#", "").upper()


def reset_ids() -> None:
    shape._id = 10


def next_id() -> int:
    shape._id += 1
    return shape._id


def shape_id() -> int:
    return next_id()


def shape(xml: str) -> str:
    return xml


shape._id = 10


def bg(fill: str = "#102018") -> str:
    return f"""<p:bg><p:bgPr><a:solidFill><a:srgbClr val="{color(fill)}"/></a:solidFill><a:effectLst/></p:bgPr></p:bg>"""


def rect(x: float, y: float, w: float, h: float, fill: str = "#1F3022", line: str = "#B8D8A4", alpha: int = 85000) -> str:
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{shape_id()}" name="Panel"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
      <p:spPr>
        <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
        <a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>
        <a:solidFill><a:srgbClr val="{color(fill)}"><a:alpha val="{alpha}"/></a:srgbClr></a:solidFill>
        <a:ln w="12700"><a:solidFill><a:srgbClr val="{color(line)}"><a:alpha val="52000"/></a:srgbClr></a:solidFill></a:ln>
      </p:spPr>
    </p:sp>"""


def text_box(x: float, y: float, w: float, h: float, text: str, size: float = 24, bold: bool = False, color_hex: str = "#EEFDF8", align: str = "l") -> str:
    bold_xml = "<a:b/>" if bold else ""
    paragraphs = ""
    for line in text.split("\n"):
        paragraphs += f"""
        <a:p>
          <a:pPr algn="{align}"/>
          <a:r><a:rPr lang="vi-VN" sz="{int(size * 100)}" dirty="0">{bold_xml}<a:solidFill><a:srgbClr val="{color(color_hex)}"/></a:solidFill><a:latin typeface="Aptos Display"/><a:cs typeface="Arial"/></a:rPr><a:t>{esc(line)}</a:t></a:r>
        </a:p>"""
    return f"""
    <p:sp>
      <p:nvSpPr><p:cNvPr id="{shape_id()}" name="Text"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
      <p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/><a:ln><a:noFill/></a:ln></p:spPr>
      <p:txBody><a:bodyPr wrap="square" anchor="t"/><a:lstStyle/>{paragraphs}</p:txBody>
    </p:sp>"""


def image(rel_id: str, x: float, y: float, w: float, h: float, name: str) -> str:
    return f"""
    <p:pic>
      <p:nvPicPr><p:cNvPr id="{shape_id()}" name="{esc(name)}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/></p:nvPicPr>
      <p:blipFill><a:blip r:embed="{rel_id}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
      <p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
    </p:pic>"""


def video_object(video_rel_id: str, media_rel_id: str, poster_rel_id: str, x: float, y: float, w: float, h: float, title: str) -> str:
    return f"""
    <p:pic>
      <p:nvPicPr>
        <p:cNvPr id="{shape_id()}" name="{esc(title)}"><a:hlinkClick action="ppaction://media"/></p:cNvPr>
        <p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>
        <p:nvPr>
          <a:videoFile r:link="{video_rel_id}"/>
          <p:extLst><p:ext uri="{{DAA4B4D4-6D71-4841-9C94-3DE7FCFBF8DC}}"><p14:media r:embed="{media_rel_id}"/></p:ext></p:extLst>
        </p:nvPr>
      </p:nvPicPr>
      <p:blipFill><a:blip r:embed="{poster_rel_id}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>
      <p:spPr><a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
    </p:pic>"""


def footer(index: int, total: int) -> str:
    return text_box(11.72, 6.86, 0.95, 0.16, f"{index:02d} / {total}", 8.5, True, "#A8C4C0", "r")


slides = [
    {
        "type": "hero",
        "kicker": "Fall detection · Stranger alert · Privacy by role",
        "title": "SYL",
        "lead": "Lớp AI an toàn cho gia đình có người cao tuổi: phát hiện té ngã, cảnh báo người lạ và kích hoạt hỗ trợ khẩn cấp đúng lúc.",
        "chips": ["YOLO Pose", "Real-time alerts", "WebRTC/HLS streaming", "B2B2C"],
    },
    {
        "kicker": "Problem",
        "title": "Khoảnh khắc nguy hiểm nhất thường xảy ra khi không ai đang nhìn.",
        "lead": "Gia đình cần một hệ thống biết phân biệt sự cố thật với chuyển động bình thường, thay vì chỉ gửi thêm nhiều thông báo nhiễu.",
        "cards": [
            ("Phát hiện trễ", "Người đi làm hoặc sống xa không thể luôn theo dõi camera để biết cha mẹ gặp sự cố."),
            ("Alert fatigue", "Motion alert quá nhiều khiến người dùng dễ tắt thông báo và bỏ lỡ cảnh báo quan trọng."),
            ("Rủi ro riêng tư", "Camera gia đình phải kiểm soát ai được xem, xem trong bao lâu và xem vì lý do gì."),
        ],
    },
    {
        "type": "survey_market",
        "kicker": "Market Signal",
        "title": "Survey xác nhận nỗi lo thật và mức sẵn sàng thử nghiệm.",
        "metrics": [
            ("52", "câu trả lời khảo sát về nhu cầu chăm sóc người thân lớn tuổi tại nhà."),
            ("85%", "có người lớn tuổi trong gia đình và lo lắng khi họ ở nhà một mình."),
            ("66,7%", "tin dùng thiết bị điện tử để hỗ trợ theo dõi người thân lớn tuổi."),
        ],
        "bars": [
            ("Có NCT & lo lắng", 85),
            ("Tin thiết bị điện tử", 66.7),
            ("Quan tâm sản phẩm", 59),
            ("Có sự cố không báo kịp", 46.2),
            ("Chắc chắn demo", 38.5),
            ("Báo động giả", 34.6),
        ],
        "quote": "Nền thị trường: khoảng 16,1 triệu người cao tuổi tại Việt Nam và 1,5–1,9 triệu ca té ngã mỗi năm tạo nhu cầu rõ cho cảnh báo sớm tại nhà.",
    },
    {
        "kicker": "Solution",
        "title": "SYL biến camera hiện có thành hệ thống chăm sóc chủ động.",
        "lead": "Gateway AI kết nối camera IP, phân tích hình ảnh thời gian thực và gửi cảnh báo có bằng chứng đến đúng người xử lý.",
        "cards": [
            ("Phát hiện té ngã", "Nhận biết tư thế/ngữ cảnh nguy hiểm để kích hoạt cảnh báo khẩn."),
            ("Phát hiện người lạ", "Đối chiếu người nhà với người lạ để giảm rủi ro an ninh trong nhà."),
            ("Bằng chứng tức thì", "Email/app gửi snapshot hoặc video evidence để gia đình xác minh nhanh."),
        ],
    },
    {
        "kicker": "Product Flow",
        "title": "Từ camera đến hành động khẩn cấp trong vài bước.",
        "steps": [
            ("01", "Stream", "Camera IP gửi RTSP qua mạng LAN hoặc tunnel bảo mật."),
            ("02", "Infer", "Model pose/face chạy inference và bám theo người trong khung hình."),
            ("03", "Classify", "Temporal classifier xác định té ngã, bất động hoặc người lạ."),
            ("04", "Alert", "Hệ thống gửi cảnh báo real-time kèm bằng chứng."),
            ("05", "Respond", "Gia đình/admin/bác sĩ phối hợp xử lý trên app."),
        ],
    },
    {
        "type": "architecture",
        "kicker": "System Architecture",
        "title": "Kiến trúc triển khai thật: camera LAN, AI services, streaming và web app.",
        "cards": [
            ("Ingestion", "IMOU/IP Camera qua RTSP, SSH reverse tunnel, MediaMTX và FFmpeg."),
            ("AI pipeline", "YOLO Pose ONNX, ONNX Runtime, OpenCV, ByteTrack, Temporal Fall Classifier, YuNet & SFace."),
            ("Backend", "FastAPI, WebSocket, Pydantic, LangChain/LangGraph điều phối alert và quyền truy cập."),
            ("Data layer", "PostgreSQL metadata, Redis cache, MinIO cho snapshot/video evidence."),
        ],
    },
    {
        "kicker": "Tech Stack",
        "title": "Nền tảng đủ sâu để chạy real-time, đủ gọn để triển khai thực tế.",
        "cards": [
            ("Computer Vision", "YOLO Pose, ONNX Runtime, OpenCV, ByteTrack, Temporal Fall Classifier, YuNet & SFace."),
            ("Streaming", "MediaMTX, WebRTC/HLS, FFmpeg và SSH Reverse Tunnel cho camera LAN."),
            ("Frontend", "React, TypeScript, Vite, hls.js, Canvas overlay; prototype React Native."),
            ("Backend", "FastAPI, WebSocket, Pydantic, LangChain/LangGraph cho workflow cảnh báo."),
            ("Storage", "PostgreSQL, Redis và MinIO để lưu metadata, cache và object evidence."),
            ("DevOps", "Docker Compose, Caddy HTTPS, uv, pnpm, Pytest, Ruff và MyPy."),
        ],
    },
    {
        "kicker": "Traction",
        "title": "Không chỉ là ý tưởng: hệ thống đã chạy được end-to-end.",
        "metrics": [
            ("240/240", "automated tests passed; Ruff và TypeScript type-check đạt 100%."),
            ("8–15 FPS", "runtime YOLO26n-pose, phụ thuộc cấu hình máy và điều kiện mạng."),
            ("83.05%", "F1 cho bài toán phát hiện người lạ trong thử nghiệm nội bộ."),
        ],
        "quote": "Web, API và Media Gateway đã triển khai trên VPS; kết nối thành công camera IP LAN qua SSH Tunnel và gửi email kèm snapshot/video evidence.",
    },
    {
        "type": "demo_video",
        "kicker": "Demo",
        "title": "Product demo: SYL phát hiện, ghi nhận và cảnh báo theo thời gian thực.",
        "video": "demo.mp4",
    },
    {
        "type": "business_competition",
        "kicker": "Business Model · Competitive Position",
        "title": "SYL có mức giá dễ tiếp cận hơn camera chuyên dụng, nhưng thông minh hơn camera phổ thông.",
        "prices": [
            ("Standard", "5.2tr", "Raspberry Pi 5 4GB + hệ thống SYL cho nhu cầu cơ bản."),
            ("Plus", "8.5tr", "Raspberry Pi 5 8GB + hệ thống SYL cho cấu hình mạnh hơn."),
            ("Pro", "10tr", "8GB + nâng cấp bản mới nhất, miễn phí 6 tháng đăng ký đầu."),
        ],
        "cards": [
            ("EZVIZ/IMOU", "Mạnh về giá và phân phối, nhưng chủ yếu là motion detection hoặc human detection."),
            ("Hanwha/i-PRO/Hikvision", "Có hướng fall detection chuyên dụng nhưng chi phí cao hoặc chưa dễ tiếp cận tại Việt Nam."),
            ("SYL", "Định vị là lớp AI chăm sóc: fall detection, stranger alert, evidence và phân quyền."),
        ],
    },
    {
        "kicker": "Privacy & Roles",
        "title": "Cảnh báo khẩn cấp phải đi cùng quyền riêng tư có kiểm soát.",
        "cards": [
            ("Admin", "Thêm camera, phân quyền, xem dashboard và kiểm tra lỗi hệ thống."),
            ("Gia đình", "Chỉ xem camera được cấp phép và nhận cảnh báo liên quan đến người thân."),
            ("Bác sĩ", "Được cấp quyền tạm thời khi có sự cố, phục vụ tư vấn hoặc đánh giá nhanh."),
            ("5 phút", "Quyền xem tình huống khẩn cấp tự thu hồi để giảm rủi ro lạm dụng dữ liệu."),
        ],
    },
    {
        "type": "roadmap",
        "kicker": "Next Step",
        "title": "Từ ý tưởng đến sản phẩm thị trường trong 19 tuần.",
        "cards": [
            ("Phase 1 · 0–4 tuần", "Hoàn thiện MVP: access control, emergency alerts và demo run ổn định."),
            ("Phase 2 · 3 tuần", "Benchmark trên các gateway/camera phổ biến để đo FPS, độ trễ và độ ổn định."),
            ("Đối tác nhận được gì", "Đang tìm 2 đối tác cung cấp camera và 1 đối tác cung cấp địa điểm thử nghiệm. Đổi lại: đối tác camera nhận đội kỹ thuật hỗ trợ riêng + ưu đãi giá; đối tác địa điểm nhận sản phẩm dùng thử miễn phí 3 tháng."),
            ("Mục tiêu pilot · 4–12 tuần", "Xác nhận hệ thống đạt Recall ≥85% và Precision với độ trễ cảnh báo chấp nhận được trên phần cứng/mạng thực tế của đối tác, không chỉ trong môi trường test nội bộ."),
        ],
        "quote": "Kết luận: SYL có thể triển khai và launch ra thị trường trong 19 tuần, tính từ lúc hình thành ý tưởng đến sản phẩm hoàn chỉnh.",
    },
    {
        "type": "closing",
        "kicker": "Thank you",
        "title": "SYL",
        "lead": "melphins",
    },
    {
        "type": "chart_focus",
        "kicker": "Model Training",
        "title": "Validation theo epoch cho thấy metric duy trì ổn định trên ngưỡng mục tiêu.",
        "image": "val_epoch",
        "media": "tech-val-epoch.jpg",
    },
    {
        "type": "chart_focus",
        "kicker": "Threshold Tuning",
        "title": "Ngưỡng validation được theo dõi qua từng epoch để chọn điểm cắt phù hợp.",
        "image": "threshold",
        "media": "tech-threshold.jpg",
    },
    {
        "type": "chart_focus",
        "kicker": "Test Classification",
        "title": "Biểu đồ lỗi phân loại giúp định hướng dữ liệu cần bổ sung cho re-train.",
        "image": "test_clf",
        "media": "tech-test-clf.jpg",
    },
    {
        "type": "eval_retrain",
        "kicker": "Highlighted Evaluation",
        "title": "Eval re-train xác nhận hiệu năng trên locked test và điều kiện chạy gần real-time.",
        "comparison": [
            ("Average latency", "332,467 ms", "155,544 ms"),
            ("p95 latency", "511,749 ms", "194,355 ms"),
            ("FPS", "3,22–5,55 FPS\nphụ thuộc đường truyền", "6,43–8,45 FPS"),
        ],
        "images": ["eval_retrain"],
    },
    {
        "type": "test_distribution",
        "kicker": "Model Evidence",
        "title": "Phân phối xác suất dự đoán trên tập test cho thấy hai nhóm fall/non-fall tách biệt rõ.",
        "points": [
        ],
        "images": ["test_distribution"],
    },
]


def topbar(label: str = "SYL") -> str:
    return image("rId2", 0.72, 0.28, 1.12, 0.55, "logo.jpg")


def card_group(items: list[tuple[str, str]], y: float = 4.08, cols: int = 3) -> str:
    out = ""
    gap = 0.18
    total_w = 11.5
    w = (total_w - gap * (cols - 1)) / cols
    h = 1.08
    x0 = 0.92
    for i, (head, body) in enumerate(items):
        row = i // cols
        col = i % cols
        x = x0 + col * (w + gap)
        yy = y + row * 1.32
        out += rect(x, yy, w, h)
        out += text_box(x + 0.16, yy + 0.13, w - 0.32, 0.28, head, 15.6, True, "#EEFDF8")
        out += text_box(x + 0.16, yy + 0.45, w - 0.32, 0.46, body, 9.4, False, "#A8C4C0")
    return out


def metric_group(items: list[tuple[str, str]]) -> str:
    out = ""
    for i, (num, body) in enumerate(items):
        x = 0.92 + i * 3.93
        out += rect(x, 4.05, 3.65, 1.32, fill="#1A2B20", line="#B8D8A4")
        out += text_box(x + 0.18, 4.24, 3.25, 0.45, num, 26.5, True, "#70F0A8")
        out += text_box(x + 0.18, 4.83, 3.25, 0.35, body, 9.6, False, "#A8C4C0")
    return out


def steps_group(items: list[tuple[str, str, str]]) -> str:
    out = ""
    gap = 0.13
    w = (11.5 - gap * 4) / 5
    for i, (num, head, body) in enumerate(items):
        x = 0.92 + i * (w + gap)
        out += rect(x, 3.85, w, 1.65, fill="#1A2B20", line="#B8D8A4")
        out += text_box(x + 0.13, 4.04, w - 0.26, 0.26, num, 13, True, "#70F0A8")
        out += text_box(x + 0.13, 4.52, w - 0.26, 0.28, head, 14.2, True, "#EEFDF8")
        out += text_box(x + 0.13, 4.91, w - 0.26, 0.42, body, 8.7, False, "#A8C4C0")
    return out


def survey_chart_group(items: list[tuple[str, float]]) -> str:
    out = rect(0.72, 4.22, 4.9, 1.72, fill="#1A2B20", line="#B8D8A4", alpha=85000)
    out += text_box(0.92, 4.36, 4.45, 0.2, "Tín hiệu nhu cầu từ report & survey", 12.0, True, "#EEFDF8")
    for i, (label, value) in enumerate(items):
        y = 4.67 + i * 0.2
        out += text_box(0.92, y, 1.52, 0.12, label, 6.15, False, "#A8C4C0")
        out += rect(2.48, y + 0.01, 2.18, 0.08, fill="#2B3A24", line="#2B3A24", alpha=90000)
        out += rect(2.48, y + 0.01, 2.18 * value / 100, 0.08, fill="#59E0D0", line="#59E0D0", alpha=100000)
        out += text_box(4.78, y, 0.55, 0.12, f"{str(value).replace('.', ',')}%", 6.15, True, "#70F0A8", "r")
    return out


def mini_bars(x: float, y: float, values: list[float], title: str, scale: float = 1.0) -> str:
    height = 0.72 * scale
    out = rect(x, y, 2.25, height, fill="#1A2B20", line="#B8D8A4", alpha=83000)
    out += text_box(x + 0.14, y + 0.1, 1.9, 0.12, title, 7.8, True, "#EEFDF8")
    bar_w = 0.32
    gap = 0.11
    base = y + 0.58 * scale
    for i, value in enumerate(values):
        h = 0.34 * value * scale
        bx = x + 0.18 + i * (bar_w + gap)
        out += rect(bx, base - h, bar_w, h, fill="#59E0D0", line="#59E0D0", alpha=100000)
    return out


def mini_ring(x: float, y: float, label: str, title: str, scale: float = 1.0) -> str:
    out = rect(x, y, 2.25, 0.72 * scale, fill="#1A2B20", line="#B8D8A4", alpha=83000)
    out += text_box(x + 0.14, y + 0.1, 1.2, 0.12, title, 7.8, True, "#EEFDF8")
    out += text_box(x + 1.22, y + 0.24 * scale, 0.82, 0.18, label, 13.5 * scale, True, "#70F0A8", "ctr")
    return out


def visual_row(kind: str, y: float = 5.82, scale: float = 1.0) -> str:
    presets = {
        "problem": [("ring", "Mẫu khảo sát", "52"), ("ring", "Báo động giả", "34,6%"), ("ring", "Không báo kịp", "46,2%")],
        "solution": [("ring", "Fall recall", "≥85%"), ("ring", "Stranger F1", "83%"), ("bars", "Evidence flow", [0.3, 0.58, 0.86])],
        "product": [("bars", "Camera", [0.5, 0.7]), ("bars", "AI pipeline", [0.35, 0.65, 0.9]), ("bars", "Response", [0.45, 0.8])],
        "architecture": [("bars", "Streaming", [0.45, 0.78, 0.58]), ("ring", "AI services", "83%"), ("bars", "Storage", [0.8, 0.48, 0.64])],
        "tech": [("bars", "Runtime", [0.53, 0.73, 1.0]), ("ring", "Coverage", "100%"), ("bars", "Pipeline", [0.4, 0.62, 0.76, 0.92])],
        "traction": [("ring", "Test pass", "100%"), ("bars", "FPS range", [0.53, 0.73, 1.0]), ("ring", "F1 score", "83%")],
        "business": [("bars", "Price ladder", [0.52, 0.85, 1.0]), ("bars", "Positioning", [0.45, 0.75, 0.55]), ("bars", "Go-to-market", [0.48, 0.78, 0.96])],
        "roles": [("bars", "Access scope", [1.0, 0.64, 0.36]), ("ring", "Doctor window", "5p"), ("bars", "Data risk", [0.9, 0.52, 0.24])],
        "roadmap": [("bars", "MVP", [0.33]), ("bars", "Benchmark", [0.25]), ("bars", "Trial", [1.0])],
    }
    items = presets[kind]
    out = ""
    for i, item in enumerate(items):
        x = 0.92 + i * 2.45
        if item[0] == "bars":
            out += mini_bars(x, y, item[2], item[1], scale)
        else:
            out += mini_ring(x, y, item[2], item[1], scale)
    return out


def build_slide(slide: dict, index: int, total: int) -> str:
    reset_ids()
    shapes = bg()

    if slide.get("type") == "demo_video":
        shapes += topbar()
        shapes += text_box(0.92, 1.02, 4.8, 0.28, slide["kicker"], 11.5, True, "#59E0D0")
        shapes += text_box(0.88, 1.47, 11.5, 0.85, slide["title"], 27, True)
        shapes += rect(1.05, 2.55, 11.25, 3.78, fill="#050807", line="#B8D8A4", alpha=96000)
        shapes += video_object("rId3", "rId4", "rId2", 1.28, 2.75, 10.78, 3.38, "demo.mp4")
        shapes += text_box(0.92, 6.42, 11.5, 0.2, "Demo video: demo.mp4", 10.5, True, "#A8C4C0", "ctr")
    elif slide.get("type") == "hero":
        shapes += image("rId3", 0, 0, 13.333333, 7.5, "syl-hero.png")
        shapes += f"""
        <p:sp>
          <p:nvSpPr><p:cNvPr id="{shape_id()}" name="Overlay"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
          <p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{int(SLIDE_W)}" cy="{int(SLIDE_H)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val="102018"><a:alpha val="28000"/></a:srgbClr></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>
        </p:sp>"""
        shapes += topbar()
        shapes += text_box(0.92, 1.35, 6.8, 0.34, slide["kicker"], 12, True, "#59E0D0")
        shapes += text_box(0.88, 1.82, 4.1, 1.05, slide["title"], 72, True)
        shapes += text_box(0.96, 3.0, 6.5, 0.68, slide["lead"], 18, False, "#D8F4EF")
        x = 0.96
        for chip in slide["chips"]:
            shapes += rect(x, 3.95, 1.68, 0.36, fill="#E7D8B5", line="#B8D8A4", alpha=17000)
            shapes += text_box(x + 0.08, 4.04, 1.5, 0.13, chip, 8.4, True, "#D8F4EF", "ctr")
            x += 1.86
    elif slide.get("type") == "closing":
        shapes += rect(1.48, 0.7, 10.38, 5.0, fill="#FFFFFF", line="#B8D8A4", alpha=98000)
        shapes += image("rId2", 1.95, 1.2, 9.45, 4.05, "logo.jpg")
        shapes += text_box(0.92, 6.0, 11.5, 0.45, slide["lead"], 25, True, "#EEFDF8", "ctr")
    elif slide.get("type") == "chart_focus":
        shapes += topbar()
        shapes += text_box(0.92, 1.02, 4.8, 0.28, slide["kicker"], 11.5, True, "#59E0D0")
        shapes += text_box(0.88, 1.44, 11.4, 0.92, slide["title"], 27.0, True)
        shapes += rect(0.86, 2.66, 11.6, 3.82, fill="#FFFFFF", line="#B8D8A4", alpha=98000)
        shapes += image("rId3", 1.02, 2.82, 11.28, 3.5, slide["media"])
    elif slide.get("type") == "eval_retrain":
        shapes += topbar()
        shapes += text_box(0.92, 0.94, 4.8, 0.28, slide["kicker"], 11.5, True, "#59E0D0")
        shapes += text_box(0.88, 1.28, 11.45, 0.82, slide["title"], 25.5, True)
        shapes += rect(0.82, 2.74, 7.18, 3.66, fill="#FFFFFF", line="#B8D8A4", alpha=98000)
        shapes += image("rId3", 0.96, 2.9, 6.9, 3.34, "eval-retrain.jpg")
        table_x, table_y = 8.24, 2.74
        widths = [1.22, 1.42, 1.42]
        shapes += rect(table_x, table_y, 4.12, 3.02, fill="#1A2B20", line="#B8D8A4")
        shapes += rect(table_x, table_y, 4.12, 0.52, fill="#24402F", line="#B8D8A4")
        headers = ["Metric", "On VPS", "On local"]
        cx = table_x
        for i, head in enumerate(headers):
            shapes += text_box(cx + 0.08, table_y + 0.16, widths[i] - 0.12, 0.18, head, 9.2, True, "#70F0A8")
            cx += widths[i]
        for r, (metric, vps, local) in enumerate(slide["comparison"]):
            yy = table_y + 0.52 + r * 0.78
            shapes += rect(table_x, yy, 4.12, 0.78, fill="#1A2B20", line="#B8D8A4", alpha=78000)
            shapes += text_box(table_x + 0.08, yy + 0.19, widths[0] - 0.12, 0.2, metric, 7.8, False, "#A8C4C0")
            shapes += text_box(table_x + widths[0] + 0.08, yy + 0.15, widths[1] - 0.12, 0.36, vps, 8.2, True, "#EEFDF8")
            shapes += text_box(table_x + widths[0] + widths[1] + 0.08, yy + 0.15, widths[2] - 0.12, 0.36, local, 8.2, True, "#EEFDF8")
    elif slide.get("type") == "test_distribution":
        shapes += topbar()
        shapes += text_box(0.92, 1.02, 4.8, 0.28, slide["kicker"], 11.5, True, "#59E0D0")
        shapes += text_box(0.88, 1.45, 11.4, 1.0, slide["title"], 27.0, True)
        shapes += rect(1.08, 2.78, 11.18, 3.64, fill="#FFFFFF", line="#B8D8A4", alpha=98000)
        shapes += image("rId3", 1.22, 2.92, 10.9, 3.36, "test-distribution.jpg")
    else:
        shapes += topbar()
        shapes += text_box(0.92, 1.02, 4.8, 0.28, slide["kicker"], 11.5, True, "#59E0D0")
        shapes += text_box(0.88, 1.47, 11.5, 1.15, slide["title"], 29, True)
        if "lead" in slide:
            shapes += text_box(0.94, 2.78, 9.4, 0.55, slide["lead"], 13.2, False, "#CFE7E3")
        if slide.get("type") == "survey_market":
            for i, (num, body) in enumerate(slide["metrics"]):
                x = 0.72 + i * 1.65
                out_w = 1.48
                shapes += rect(x, 2.9, out_w, 1.08, fill="#1A2B20", line="#B8D8A4")
                shapes += text_box(x + 0.1, 3.06, out_w - 0.2, 0.32, num, 18.2, True, "#70F0A8")
                shapes += text_box(x + 0.1, 3.47, out_w - 0.2, 0.31, body, 6.25, False, "#A8C4C0")
            shapes += survey_chart_group(slide["bars"])
            shapes += rect(5.88, 2.78, 3.12, 1.48, fill="#FFFFFF", line="#B8D8A4", alpha=98000)
            shapes += image("rId3", 5.98, 2.88, 2.92, 1.28, "missed-alert.png")
            shapes += rect(9.18, 2.78, 3.12, 1.48, fill="#FFFFFF", line="#B8D8A4", alpha=98000)
            shapes += image("rId4", 9.28, 2.88, 2.92, 1.28, "support-solution.png")
            shapes += rect(5.88, 4.48, 3.12, 1.48, fill="#FFFFFF", line="#B8D8A4", alpha=98000)
            shapes += image("rId5", 5.98, 4.58, 2.92, 1.28, "early-access.png")
            shapes += rect(9.18, 4.48, 3.12, 1.48, fill="#FFFFFF", line="#B8D8A4", alpha=98000)
            shapes += image("rId6", 9.28, 4.58, 2.92, 1.28, "false-alarm.png")
        elif "metrics" in slide:
            shapes += metric_group(slide["metrics"])
        if "steps" in slide:
            shapes += steps_group(slide["steps"])
        if slide.get("type") == "roadmap":
            for i, (head, body) in enumerate(slide["cards"]):
                x = 0.92 + (i % 2) * 5.86
                yy = 3.1 + (i // 2) * 1.42
                shapes += rect(x, yy, 5.55, 1.16, fill="#1A2B20", line="#B8D8A4")
                shapes += text_box(x + 0.17, yy + 0.12, 5.18, 0.24, head, 13.8, True, "#EEFDF8")
                shapes += text_box(x + 0.17, yy + 0.43, 5.15, 0.55, body, 7.8, False, "#A8C4C0")
        if slide.get("type") == "business_competition":
            for i, (name, price, body) in enumerate(slide["prices"]):
                yy = 3.0 + i * 1.05
                shapes += rect(0.92, yy, 5.45, 0.82, fill="#1A2B20", line="#B8D8A4")
                shapes += text_box(1.1, yy + 0.12, 2.1, 0.2, name, 13.2, True, "#EEFDF8")
                shapes += text_box(3.25, yy + 0.12, 1.25, 0.2, price, 13.2, True, "#FFD166")
                shapes += text_box(1.1, yy + 0.42, 4.95, 0.18, body, 7.9, False, "#A8C4C0")
            for i, (head, body) in enumerate(slide["cards"]):
                yy = 3.0 + i * 1.05
                shapes += rect(6.65, yy, 5.55, 0.82, fill="#1A2B20", line="#B8D8A4")
                shapes += text_box(6.83, yy + 0.12, 5.15, 0.2, head, 13.2, True, "#EEFDF8")
                shapes += text_box(6.83, yy + 0.42, 5.05, 0.18, body, 7.9, False, "#A8C4C0")
        if "cards" in slide and slide.get("type") not in ("architecture", "roadmap", "business_competition"):
            cols = 4 if len(slide["cards"]) == 4 else 3
            y = 3.75 if len(slide["cards"]) > 4 else (4.1 if "lead" in slide else 3.9)
            shapes += card_group(slide["cards"], y=y, cols=cols)
        if "prices" in slide and slide.get("type") != "business_competition":
            shapes += card_group([(f"{name} · {price}", body) for name, price, body in slide["prices"]], y=4.0, cols=3)
        if slide.get("type") == "architecture":
            shapes += rect(0.65, 2.62, 8.25, 3.98, fill="#FFFFFF", line="#B8D8A4", alpha=98000)
            shapes += image("rId3", 0.8, 2.77, 7.95, 3.68, "overview-diagram.png")
            for i, (head, body) in enumerate(slide["cards"]):
                yy = 2.62 + i * 0.84
                shapes += rect(9.12, yy, 3.33, 0.68, fill="#1A2B20", line="#B8D8A4")
                shapes += text_box(9.27, yy + 0.09, 3.0, 0.18, head, 10.8, True, "#EEFDF8")
                shapes += text_box(9.27, yy + 0.31, 2.96, 0.21, body, 6.8, False, "#A8C4C0")
        if "quote" in slide:
            qy = 6.2 if slide.get("type") == "roadmap" or slide.get("kicker") == "Traction" else 5.78
            shapes += rect(0.92, qy, 10.8, 0.55, fill="#2B3A24", line="#7FB069", alpha=76000)
            shapes += text_box(1.12, qy + 0.14, 10.2, 0.22, slide["quote"], 9.4 if slide.get("type") == "roadmap" or slide.get("kicker") == "Traction" else 11.5, False, "#D8F4EF")
        viz_map = {
            "Problem": "problem",
            "Solution": "solution",
            "Product Flow": "product",
            "Tech Stack": "tech",
            "Traction": "traction",
            "Privacy & Roles": "roles",
        }
        if slide.get("type") == "business_competition":
            shapes += visual_row("business")
        elif slide.get("type") == "roadmap":
            shapes += visual_row("roadmap", y=5.62, scale=0.55)
        elif slide.get("kicker") == "Traction":
            shapes += visual_row("traction", y=5.48, scale=0.7)
        elif slide.get("kicker") in viz_map:
            shapes += visual_row(viz_map[slide["kicker"]])

    shapes += footer(index, total)
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:p14="http://schemas.microsoft.com/office/powerpoint/2010/main">
  <p:cSld>{shapes}</p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>"""


def slide_rels(slide: dict) -> str:
    rels = [
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>',
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/logo.jpg"/>',
    ]
    if slide.get("type") == "hero":
        rels.append('<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/syl-hero.png"/>')
    if slide.get("type") == "architecture":
        rels.append('<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/overview-diagram.png"/>')
    if slide.get("type") == "survey_market":
        rels.append('<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/survey-missed-alert.png"/>')
        rels.append('<Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/survey-support-solution.png"/>')
        rels.append('<Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/survey-early-access.png"/>')
        rels.append('<Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/survey-false-alarm.png"/>')
    if slide.get("type") == "demo_video":
        rels.append('<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/video" Target="../media/demo.mp4"/>')
        rels.append('<Relationship Id="rId4" Type="http://schemas.microsoft.com/office/2007/relationships/media" Target="../media/demo.mp4"/>')
    if slide.get("type") == "chart_focus":
        rels.append(f'<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{slide["media"]}"/>')
    if slide.get("type") == "eval_retrain":
        rels.append('<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/tech-eval-retrain.jpg"/>')
    if slide.get("type") == "test_distribution":
        rels.append('<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/tech-test-distribution.jpg"/>')
    return f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rels)}</Relationships>"""


def build_pptx() -> None:
    for asset in (HERO, DIAGRAM, LOGO, DEMO_VIDEO, *SURVEY_IMAGES.values(), *TECH_IMAGES.values()):
        if not asset.exists():
            raise FileNotFoundError(asset)
    if OUT.exists():
        OUT.unlink()

    total = len(slides)
    theme_rid = f"rId{total + 2}"
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="jpg" ContentType="image/jpeg"/>
  <Default Extension="jpeg" ContentType="image/jpeg"/>
  <Default Extension="mp4" ContentType="video/mp4"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
""" + "".join(
        f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n'
        for i in range(1, total + 1)
    ) + "</Types>"

    presentation_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
""" + "".join(
        f'  <Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>\n'
        for i in range(1, total + 1)
    ) + f"""  <Relationship Id="{theme_rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>
</Relationships>"""

    presentation = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{''.join(f'<p:sldId id="{256+i}" r:id="rId{i+2}"/>' for i in range(total))}</p:sldIdLst>
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
        z.write(DIAGRAM, "ppt/media/overview-diagram.png")
        z.write(LOGO, "ppt/media/logo.jpg")
        z.write(DEMO_VIDEO, "ppt/media/demo.mp4")
        z.write(SURVEY_IMAGES["missed_alert"], "ppt/media/survey-missed-alert.png")
        z.write(SURVEY_IMAGES["support_solution"], "ppt/media/survey-support-solution.png")
        z.write(SURVEY_IMAGES["early_access"], "ppt/media/survey-early-access.png")
        z.write(SURVEY_IMAGES["false_alarm"], "ppt/media/survey-false-alarm.png")
        z.write(TECH_IMAGES["val_epoch"], "ppt/media/tech-val-epoch.jpg")
        z.write(TECH_IMAGES["threshold"], "ppt/media/tech-threshold.jpg")
        z.write(TECH_IMAGES["test_clf"], "ppt/media/tech-test-clf.jpg")
        z.write(TECH_IMAGES["test_distribution"], "ppt/media/tech-test-distribution.jpg")
        z.write(TECH_IMAGES["validation_metrics"], "ppt/media/tech-validation-metrics.jpg")
        z.write(TECH_IMAGES["confusion_matrix"], "ppt/media/tech-confusion-matrix.jpg")
        z.write(TECH_IMAGES["fall_probability"], "ppt/media/tech-fall-probability.jpg")
        z.write(TECH_IMAGES["eval_retrain"], "ppt/media/tech-eval-retrain.jpg")
        for i, slide in enumerate(slides, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", build_slide(slide, i, total))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels(slide))

    print(f"Wrote {OUT.resolve()} ({OUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    build_pptx()
