# -*- coding: utf-8 -*-
"""Sinh build_pptx_hust.py từ build_pptx.py: CHỈ đổi trình bày sang template HUST RED 2026.
Mọi chuỗi nội dung, ảnh, sơ đồ, speaker notes và thứ tự 18 slide giữ nguyên từ script gốc."""
from pathlib import Path

HERE = Path(__file__).parent
src = (HERE / 'build_pptx.py').read_text(encoding='utf-8')


def rep(old, new):
    global src
    assert src.count(old) >= 1, f'không tìm thấy: {old[:90]}'
    src = src.replace(old, new)


def rep_block(start, end, new):
    global src
    i = src.index(start); j = src.index(end, i)
    src = src[:i] + new + src[j:]


rep("OUT = ROOT / 'Slide_bao_cao_thiet_ke_giao_dien_Di_cho_tien_loi.pptx'",
    "OUT = ROOT / 'BaoCao_UI_Design_HUST.pptx'\nHA = ROOT / 'assets/hust'\nTEMPLATE = HA / 'HUST_RED_PPT_TEMPLATE_2026_16x9.pptx'")

# ---- bảng màu HUST (đỏ #C02034, chữ đỏ #C00000, vàng #E59C0A, xám) ----
for old, new in [
    ("ORANGE = RGBColor(0xFF, 0x93, 0x3E)", "ORANGE = RGBColor(0xC0, 0x20, 0x34)  # đỏ HUST"),
    ("ORANGE_D = RGBColor(0x9A, 0x3F, 0x00)", "ORANGE_D = RGBColor(0xC0, 0x00, 0x00)  # chữ đỏ của template"),
    ("ORANGE_S = RGBColor(0xFF, 0xE9, 0xD6)", "ORANGE_S = RGBColor(0xFB, 0xEA, 0xEC)"),
    ("BLUE = RGBColor(0x73, 0xA5, 0xCA)", "BLUE = RGBColor(0x59, 0x59, 0x59)"),
    ("BLUE_D = RGBColor(0x2F, 0x6F, 0x99)", "BLUE_D = RGBColor(0x40, 0x40, 0x40)"),
    ("BLUE_S = RGBColor(0xE7, 0xF1, 0xF8)", "BLUE_S = RGBColor(0xF2, 0xF2, 0xF2)"),
    ("CREAM = RGBColor(0xFF, 0xE9, 0xA9)", "CREAM = RGBColor(0xE5, 0x9C, 0x0A)  # vàng HUST"),
    ("BROWN = RGBColor(0x2A, 0x1A, 0x0F)", "BROWN = RGBColor(0x26, 0x26, 0x26)"),
    ("MUTED = RGBColor(0x7A, 0x66, 0x56)", "MUTED = RGBColor(0x59, 0x59, 0x59)"),
    ("BORDER = RGBColor(0xF0, 0xDF, 0xC8)", "BORDER = RGBColor(0xD9, 0xD9, 0xD9)"),
    ("FONT = 'Arial'", "FONT = 'Calibri'  # template dùng Lato (thiếu dấu tiếng Việt, chưa cài) → Calibri"),
]:
    rep(old, new)

# ---- dựng trên template HUST: xoá slide mẫu, dùng layout có sẵn ----
rep("""prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]""", """prs = Presentation(str(TEMPLATE))
_ids = prs.slides._sldIdLst
for _sid in list(_ids):
    prs.part.drop_rel(_sid.rId); _ids.remove(_sid)
LAY = {l.name: l for l in prs.slide_layouts}
DY = 0.0  # dịch nội dung lên để nằm giữa thanh tiêu đề đỏ và footer logo của template


def yy(y):
    return y + DY if y >= 1.3 else y""")

# mọi hàm vẽ dùng yy() cho toạ độ dọc
for fn in ("def tb(slide, x, y, w, h,", "def bullets(slide, x, y, w, h,", "def card(slide, x, y, w, h,", "def circle(slide, x, y, d,",
           "def chip(slide, x, y, text,", "def phone(slide, name, x, y, h,", "def picture_fit(slide, path, x, y, w, h):"):
    i = src.index(fn); j = src.index('\n', src.index('):', i)) + 1
    src = src[:j] + '    y = yy(y)\n' + src[j:]
# nhãn dưới điện thoại đã được dịch một lần trong phone(): tránh dịch lần hai
rep("        tb(slide, x - 0.25, y + h + 0.06, w + 0.5, 0.3, label, 12, False, label_color, PP_ALIGN.CENTER, italic=True)",
    "        tb(slide, x - 0.25, y + h + 0.06 - DY, w + 0.5, 0.3, label, 12, False, label_color, PP_ALIGN.CENTER, italic=True)")

rep_block("def title(slide, text, kicker=None, dark=False):", "def screen_slide(",
'''def title(slide, text, kicker=None, dark=False):
    """Tiêu đề nằm trong thanh đỏ của layout HUST; nhãn mục ở góc phải thanh đỏ."""
    t = slide.shapes.title
    t.left, t.top, t.width, t.height = Inches(0.45), Inches(0.1), Inches(9.6), Inches(0.5)
    tf = t.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = text
    r.font.name = FONT; r.font.size = Pt(24); r.font.bold = True; r.font.color.rgb = WHITE
    if kicker:
        tb(slide, 10.1, 0.17, 2.85, 0.36, kicker.upper(), 11, True, RGBColor(0xFB, 0xEA, 0xEC), PP_ALIGN.RIGHT, MSO_ANCHOR.MIDDLE)


def footer(slide, n, dark=False):
    """Footer logo + đường kẻ có sẵn trong layout; chỉ thêm số trang theo vị trí của template."""
    tb(slide, 12.2, 7.12, 0.75, 0.26, str(n), 10, True, ORANGE_D, PP_ALIGN.RIGHT)


def new(notes, dark=False, layout='Section Header'):
    global DY
    s = prs.slides.add_slide(LAY[layout])
    for ph in list(s.placeholders):
        if layout != 'Section Header' or ph.placeholder_format.type != 1:  # chỉ giữ ô tiêu đề
            ph._element.getparent().remove(ph._element)
    DY = -0.4 if layout == 'Section Header' else 0.0
    s.notes_slide.notes_text_frame.text = notes
    return s


''')
# số thứ tự trên nền đỏ/xám: chữ trắng
rep("circle(s, 0.6, y, 0.42, ORANGE if i % 2 == 0 else BLUE, str(i + 1), BROWN, 14)",
    "circle(s, 0.6, y, 0.42, ORANGE if i % 2 == 0 else BLUE, str(i + 1), WHITE, 14)")
rep("circle(s, cx + 0.25, 1.85, 0.5, ORANGE, str(i + 1), BROWN, 16)",
    "circle(s, cx + 0.25, 1.85, 0.5, ORANGE, str(i + 1), WHITE, 16)")

# ---- slide 1: bìa HUST (layout nền trắng có vòng chấm + logo chính thức) ----
rep_block("tb(s, 0.7, 0.75, 7, 0.35, 'IT4788 · PHÁT TRIỂN ỨNG DỤNG ĐA NỀN TẢNG', 13, True, CREAM)", "# ============ 2. Tổng quan ============",
"""s.shapes.add_picture(str(HA / 'hust_logo_full.png'), Inches(0.55), Inches(0.4), height=Inches(0.95))
tb(s, 0.7, 1.75, 7, 0.35, 'IT4788 · PHÁT TRIỂN ỨNG DỤNG ĐA NỀN TẢNG', 13, True, MUTED)
tb(s, 0.7, 2.25, 6.6, 1.9, ['Thiết kế giao diện', [('Đi chợ tiện lợi', {'color': ORANGE_D})]], 44, True, BROWN, spacing=1.0)
tb(s, 0.7, 4.25, 6.0, 1.2, 'Báo cáo phân tích và thiết kế giao diện dựa trên mã nguồn và ảnh chụp sản phẩm thực tế (React Native + Expo + TypeScript)', 17, False, MUTED)
tb(s, 0.7, 5.75, 6, 0.3, 'Nhóm thực hiện: ……………………………', 14, False, BROWN)
tb(s, 0.7, 6.15, 6, 0.3, 'Hà Nội, 11/2026', 14, True, ORANGE_D)
phone(s, '01_login', 7.45, 1.25, 4.6)
phone(s, '10_home', 9.25, 0.75, 5.6)
phone(s, '30_fridge', 11.25, 1.6, 4.3)

""")
rep("rất mong nhận được góp ý.', dark=True)", "rất mong nhận được góp ý.', dark=True, layout='Title Slide')")
rep("bài trình bày gồm ba phần".capitalize() if False else "và đánh giá.', dark=True)", "và đánh giá.', dark=True, layout='Title and Content')")

# ---- slide 18: kết luận trên nền đỏ chấm tròn của template ----
rep_block("tb(s, 0.7, 0.75, 7, 0.35, 'KẾT LUẬN', 13, True, CREAM)", "prs.core_properties.title",
"""_pn = card(s, 0.4, 0.5, 7.9, 6.55, ORANGE, None, 0.04)
from pptx.oxml.ns import qn as _qn
from lxml import etree as _et
_clr = _pn.fill._xPr.find('.//' + _qn('a:srgbClr')); _al = _et.SubElement(_clr, _qn('a:alpha')); _al.set('val', '88000')
tb(s, 0.7, 0.75, 7, 0.35, 'KẾT LUẬN', 13, True, RGBColor(0xFB, 0xEA, 0xEC))
tb(s, 0.7, 1.35, 7.4, 1.6, 'Giao diện thực tế, nhất quán và sẵn sàng phát triển tiếp', 34, True, WHITE, spacing=1.05)
kp = [('17', 'màn hình nghiệp vụ quanh 5 tab'), ('14', 'component dùng chung trên bộ token'), ('51', 'ảnh chụp từ ứng dụng chạy thật'), ('5', 'hạn chế ưu tiên cần xử lý')]
for i, (v, l) in enumerate(kp):
    cx = 0.7 + (i % 2) * 3.7; cy = 3.4 + (i // 2) * 1.55
    tb(s, cx, cy, 1.4, 0.8, v, 40, True, WHITE)
    tb(s, cx + 1.35, cy + 0.12, 2.2, 0.9, l, 14, False, RGBColor(0xFB, 0xEA, 0xEC))
tb(s, 0.7, 6.45, 7, 0.4, 'Cảm ơn thầy cô và các bạn đã lắng nghe!', 18, True, WHITE)
phone(s, '40_meal', 8.55, 0.85, 5.7)
phone(s, '20_shopping', 10.75, 1.45, 4.9)

""")
rep("prs.core_properties.title = 'Thiết kế giao diện Đi chợ tiện lợi'",
    "prs.core_properties.title = 'Thiết kế giao diện Đi chợ tiện lợi'\nprs.core_properties.author = 'Nhóm Đi chợ tiện lợi'")

(HERE / 'build_pptx_hust.py').write_text(src, encoding='utf-8')
print('written build_pptx_hust.py')
