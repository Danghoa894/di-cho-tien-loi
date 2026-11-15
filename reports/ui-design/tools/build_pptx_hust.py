# -*- coding: utf-8 -*-
"""Slide_bao_cao_thiet_ke_giao_dien_Di_cho_tien_loi.pptx — python-pptx, 16:9, 18 slide, có speaker notes."""
from pathlib import Path
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu

ROOT = Path('D:/Project/di-cho-tien-loi/reports/ui-design')
MK = ROOT / 'assets/illustrations'
DG = ROOT / 'assets/diagrams'
OUT = ROOT / 'BaoCao_UI_Design_HUST.pptx'
HA = ROOT / 'assets/hust'
TEMPLATE = HA / 'HUST_RED_PPT_TEMPLATE_2026_16x9.pptx'

ORANGE = RGBColor(0xC0, 0x20, 0x34)  # đỏ HUST
ORANGE_D = RGBColor(0xC0, 0x00, 0x00)  # chữ đỏ của template
ORANGE_S = RGBColor(0xFB, 0xEA, 0xEC)
BLUE = RGBColor(0x59, 0x59, 0x59)
BLUE_D = RGBColor(0x40, 0x40, 0x40)
BLUE_S = RGBColor(0xF2, 0xF2, 0xF2)
CREAM = RGBColor(0xE5, 0x9C, 0x0A)  # vàng HUST
BROWN = RGBColor(0x26, 0x26, 0x26)
MUTED = RGBColor(0x59, 0x59, 0x59)
BORDER = RGBColor(0xD9, 0xD9, 0xD9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x2E, 0x7D, 0x32); GREEN_S = RGBColor(0xE8, 0xF5, 0xE9)
AMBER = RGBColor(0x8A, 0x5A, 0x00); AMBER_S = RGBColor(0xFF, 0xF3, 0xD1)
RED = RGBColor(0xC6, 0x28, 0x28); RED_S = RGBColor(0xFF, 0xEB, 0xEE)
FONT = 'Calibri'  # template dùng Lato (thiếu dấu tiếng Việt, chưa cài) → Calibri

prs = Presentation(str(TEMPLATE))
_ids = prs.slides._sldIdLst
for _sid in list(_ids):
    prs.part.drop_rel(_sid.rId); _ids.remove(_sid)
LAY = {l.name: l for l in prs.slide_layouts}
DY = 0.0  # dịch nội dung lên để nằm giữa thanh tiêu đề đỏ và footer logo của template


def yy(y):
    return y + DY if y >= 1.3 else y
SW, SH = 13.333, 7.5


def tb(slide, x, y, w, h, text, size=16, bold=False, color=BROWN, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, italic=False, margin=0.0, spacing=1.1):
    y = yy(y)
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(margin); tf.margin_top = tf.margin_bottom = Inches(0.02)
    tf.vertical_anchor = anchor
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = spacing
        runs = line if isinstance(line, list) else [(line, {})]
        for rt, ro in runs:
            r = p.add_run(); r.text = rt
            f = r.font; f.name = FONT; f.size = Pt(ro.get('size', size)); f.bold = ro.get('bold', bold)
            f.italic = ro.get('italic', italic); f.color.rgb = ro.get('color', color)
        if i < len(lines) - 1:
            p.space_after = Pt(6)
    return box


def bullets(slide, x, y, w, h, items, size=15, color=BROWN, gap=8):
    y = yy(y)
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0); tf.margin_top = Inches(0.02)
    for i, it in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap); p.line_spacing = 1.08
        pPr = p._p.get_or_add_pPr()
        pPr.set('marL', str(Emu(Inches(0.22)))); pPr.set('indent', str(-Emu(Inches(0.22))))
        from pptx.oxml.ns import qn
        from lxml import etree
        bu = etree.SubElement(pPr, qn('a:buFont')); bu.set('typeface', 'Arial')
        bc = etree.SubElement(pPr, qn('a:buChar')); bc.set('char', '•')
        parts = it if isinstance(it, list) else [(it, {})]
        for rt, ro in parts:
            r = p.add_run(); r.text = rt; f = r.font; f.name = FONT; f.size = Pt(ro.get('size', size))
            f.bold = ro.get('bold', False); f.color.rgb = ro.get('color', color)
    return box


def card(slide, x, y, w, h, fill=WHITE, line=BORDER, radius=0.08, shadow=False):
    y = yy(y)
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.adjustments[0] = radius
    s.fill.solid(); s.fill.fore_color.rgb = fill
    if line is None: s.line.fill.background()
    else: s.line.color.rgb = line; s.line.width = Pt(1)
    if not shadow:
        s.shadow.inherit = False
    s.text_frame.text = ''
    return s


def circle(slide, x, y, d, fill, text, color=WHITE, size=14):
    y = yy(y)
    s = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    s.fill.solid(); s.fill.fore_color.rgb = fill; s.line.fill.background(); s.shadow.inherit = False
    tf = s.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; r = p.add_run(); r.text = text
    r.font.name = FONT; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = color
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return s


def chip(slide, x, y, text, fill, color, size=11, w=None):
    y = yy(y)
    w = w or (0.16 + 0.085 * len(text))
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(0.3))
    s.adjustments[0] = 0.5; s.fill.solid(); s.fill.fore_color.rgb = fill; s.line.fill.background(); s.shadow.inherit = False
    tf = s.text_frame; tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; r = p.add_run(); r.text = text
    r.font.name = FONT; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = color
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return w


def phone(slide, name, x, y, h, label=None, label_color=MUTED):
    y = yy(y)
    path = MK / f'mockup_{name}.png'
    iw, ih = Image.open(path).size
    w = h * iw / ih
    slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    if label:
        tb(slide, x - 0.25, y + h + 0.06 - DY, w + 0.5, 0.3, label, 12, False, label_color, PP_ALIGN.CENTER, italic=True)
    return w


def picture_fit(slide, path, x, y, w, h):
    y = yy(y)
    iw, ih = Image.open(path).size
    r = min(w / iw, h / ih); pw, ph = iw * r, ih * r
    slide.shapes.add_picture(str(path), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2), Inches(pw), Inches(ph))
    return pw, ph


def title(slide, text, kicker=None, dark=False):
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


def screen_slide(n, kicker, ttl, phones, points, notes, ph_h=5.15):
    s = new(notes)
    title(s, ttl, kicker)
    # phones bên phải
    widths = []
    for nm, _ in phones:
        iw, ih = Image.open(MK / f'mockup_{nm}.png').size; widths.append(ph_h * iw / ih)
    gap = 0.35
    total = sum(widths) + gap * (len(phones) - 1)
    x = SW - 0.6 - total
    for (nm, lb), w in zip(phones, widths):
        phone(s, nm, x, 1.55, ph_h, lb); x += w + gap
    # điểm nhấn bên trái
    left_w = SW - 0.6 - total - 0.5 - 0.6
    y = 1.65
    for i, (head, body) in enumerate(points):
        circle(s, 0.6, y, 0.42, ORANGE if i % 2 == 0 else BLUE, str(i + 1), WHITE, 14)
        tb(s, 1.2, y - 0.03, left_w - 0.6, 0.35, head, 16, True)
        tb(s, 1.2, y + 0.33, left_w - 0.6, 0.95, body, 13.5, False, MUTED)
        y += 1.32
    footer(s, n)
    return s

# ============ 1. Bìa ============
s = new('Kính chào thầy cô và các bạn. Nhóm xin trình bày báo cáo phân tích và thiết kế giao diện của ứng dụng Đi chợ tiện lợi, bài tập lớn học phần IT4788. Điểm khác biệt của báo cáo là mọi nội dung đều được rút ra từ mã nguồn thực tế và mọi hình giao diện đều là ảnh chụp ứng dụng đang chạy, không phải bản vẽ mockup. Bài trình bày gồm ba phần: phân tích yêu cầu và cấu trúc, thiết kế từng nhóm màn hình, và đánh giá.', dark=True, layout='Title and Content')
s.shapes.add_picture(str(HA / 'hust_logo_full.png'), Inches(0.55), Inches(0.4), height=Inches(0.95))
tb(s, 0.7, 1.75, 7, 0.35, 'IT4788 · PHÁT TRIỂN ỨNG DỤNG ĐA NỀN TẢNG', 13, True, MUTED)
tb(s, 0.7, 2.25, 6.6, 1.9, ['Thiết kế giao diện', [('Đi chợ tiện lợi', {'color': ORANGE_D})]], 44, True, BROWN, spacing=1.0)
tb(s, 0.7, 4.25, 6.0, 1.2, 'Báo cáo phân tích và thiết kế giao diện dựa trên mã nguồn và ảnh chụp sản phẩm thực tế (React Native + Expo + TypeScript)', 17, False, MUTED)
tb(s, 0.7, 5.75, 6, 0.3, 'Nhóm thực hiện: ……………………………', 14, False, BROWN)
tb(s, 0.7, 6.15, 6, 0.3, 'Hà Nội, 11/2026', 14, True, ORANGE_D)
phone(s, '01_login', 7.45, 1.25, 4.6)
phone(s, '10_home', 9.25, 0.75, 5.6)
phone(s, '30_fridge', 11.25, 1.6, 4.3)

# ============ 2. Tổng quan ============
s = new('Đi chợ tiện lợi là ứng dụng di động giúp một gia đình dùng chung danh sách đi chợ, tủ lạnh, kế hoạch bữa ăn và công thức. Về kỹ thuật, ứng dụng viết bằng Expo SDK 58, React Native 0.88 và TypeScript, điều hướng bằng Expo Router, dữ liệu dùng TanStack Query và Zustand, kết nối backend Express với MongoDB. Qua khảo sát mã nguồn, nhóm thống kê được 17 màn hình nghiệp vụ, 5 tab chính và 14 component giao diện dùng chung. Trang quản trị web mới chỉ có API ở backend, chưa có giao diện.')
title(s, 'Tổng quan dự án', 'Giới thiệu')
tb(s, 0.6, 1.6, 5.9, 1.6, 'Ứng dụng di động đa nền tảng giúp gia đình cùng quản lý đi chợ, tủ lạnh, bữa ăn và công thức — dữ liệu chia sẻ trong một nhóm gia đình.', 17, False, BROWN, spacing=1.2)
techs = [('Expo SDK 58', ORANGE_S, ORANGE_D), ('React Native 0.88', ORANGE_S, ORANGE_D), ('TypeScript', ORANGE_S, ORANGE_D), ('Expo Router', BLUE_S, BLUE_D),
         ('TanStack Query', BLUE_S, BLUE_D), ('Zustand', BLUE_S, BLUE_D), ('Express + MongoDB', GREEN_S, GREEN), ('Expo Push', GREEN_S, GREEN)]
x, y = 0.6, 3.25
for t_, f_, c_ in techs:
    w = 0.3 + 0.1 * len(t_)
    if x + w > 6.5: x, y = 0.6, y + 0.45
    chip(s, x, y, t_, f_, c_, 12, w); x += w + 0.15
tb(s, 0.6, 4.55, 5.9, 1.9, ['Phạm vi khảo sát: 23 file route, 14 file component, 13 file API của mobile; routes, models, services của backend; tài liệu docs/.', 'Ảnh giao diện: 51 ảnh chụp tự động từ ứng dụng chạy thật với dữ liệu mẫu.'], 13.5, False, MUTED, spacing=1.15)
stats = [('17', 'màn hình nghiệp vụ', ORANGE_S, ORANGE_D), ('5', 'tab điều hướng chính', AMBER_S, AMBER), ('14', 'component UI dùng chung', BLUE_S, BLUE_D), ('0', 'màn hình Web Admin', RED_S, RED)]
for i, (v, l, f_, c_) in enumerate(stats):
    cx = 7.1 + (i % 2) * 2.95; cy = 1.6 + (i // 2) * 2.55
    card(s, cx, cy, 2.75, 2.3, f_, None, 0.1)
    tb(s, cx + 0.3, cy + 0.3, 2.2, 1.1, v, 60, True, c_)
    tb(s, cx + 0.3, cy + 1.45, 2.2, 0.7, l, 15, True, c_)
footer(s, 2)

# ============ 3. Bài toán & đối tượng ============
s = new('Bài toán xuất phát từ ba vấn đề quen thuộc trong gia đình: mua trùng hoặc thiếu vì không có danh sách chung, thực phẩm bị quên đến hết hạn, và mất công nghĩ món ăn mỗi ngày. Trong mã nguồn, người dùng được chia thành bốn trường hợp: người chưa có nhóm, thành viên, trưởng nhóm và quản trị viên hệ thống. Giao diện hiển thị nút theo quyền: ví dụ chỉ trưởng nhóm mới thấy nút tạo danh sách đi chợ hay thêm món vào bữa ăn, còn thành viên vẫn được đánh dấu đã mua.')
title(s, 'Bài toán và đối tượng sử dụng', 'Phân tích yêu cầu')
probs = [('Mua trùng, mua thiếu', 'Danh sách ghi giấy hoặc nhắn tin, không biết ai đi chợ, mua được tới đâu.', 'cart'),
         ('Thực phẩm hết hạn', 'Đồ trong tủ bị quên, phải bỏ đi — lãng phí tiền và thực phẩm.', 'fridge'),
         ('Nghĩ món mỗi ngày', 'Không nắm được nguyên liệu sẵn có để lên thực đơn.', 'meal')]
for i, (h_, b_, _) in enumerate(probs):
    cx = 0.6 + i * 4.1
    card(s, cx, 1.6, 3.85, 1.9, ORANGE_S if i == 1 else WHITE, BORDER, 0.08)
    circle(s, cx + 0.25, 1.85, 0.5, ORANGE, str(i + 1), WHITE, 16)
    tb(s, cx + 0.9, 1.9, 2.8, 0.4, h_, 17, True)
    tb(s, cx + 0.25, 2.5, 3.4, 0.95, b_, 14, False, MUTED)
tb(s, 0.6, 3.85, 6, 0.4, 'Người dùng và vai trò (xác định trong code)', 18, True)
roles = [('Chưa có nhóm', 'groupId = null', 'Chỉ tạo nhóm, đổi ảnh, đổi mật khẩu', RED_S, RED),
         ('Thành viên', 'group.members', 'Xem dữ liệu nhóm, đánh dấu đã mua, CRUD tủ lạnh và công thức', BLUE_S, BLUE_D),
         ('Trưởng nhóm', 'group.adminId', 'Thêm thành viên, tạo danh sách đi chợ, lập bữa ăn', ORANGE_S, ORANGE_D),
         ('Quản trị hệ thống', 'role = "admin"', 'Thêm/sửa/xoá danh mục và đơn vị đo', AMBER_S, AMBER)]
for i, (r_, code, d_, f_, c_) in enumerate(roles):
    cx = 0.6 + i * 3.08
    card(s, cx, 4.4, 2.88, 2.4, f_, None, 0.08)
    tb(s, cx + 0.22, 4.6, 2.5, 0.4, r_, 17, True, c_)
    tb(s, cx + 0.22, 5.02, 2.5, 0.3, code, 12, False, c_, italic=True)
    tb(s, cx + 0.22, 5.45, 2.5, 1.25, d_, 13.5, False, BROWN)
footer(s, 3)

# ============ 4. Phạm vi chức năng ============
s = new('Bảng này tóm tắt phạm vi chức năng và mức độ triển khai giao diện, đánh giá theo mã nguồn chứ không theo API. Màu xanh là đã triển khai đầy đủ, vàng là triển khai một phần, đỏ là chưa có giao diện. Hai điểm một phần đáng chú ý là hồ sơ cá nhân — app chỉ đổi được ảnh và mật khẩu, không sửa được tên hay username dù API có hỗ trợ — và nhóm gia đình, vì tài khoản đăng ký mới không có username nên không thể được thêm vào nhóm. Web Admin chưa được khởi tạo.')
title(s, 'Phạm vi chức năng', 'Đối chiếu mã nguồn')
mods = [('Xác thực', 'Đăng ký · xác minh email · đăng nhập · quên mật khẩu', 'Đầy đủ'), ('Trang chủ', 'Dashboard tủ lạnh · đi chợ · bữa ăn · báo cáo', 'Đầy đủ'),
        ('Đi chợ', 'Danh sách · phân công · thêm món · đánh dấu đã mua', 'Đầy đủ'), ('Tủ lạnh', 'Thêm/sửa/xoá · hạn dùng 3 màu · nhắc hết hạn', 'Đầy đủ'),
        ('Kho thực phẩm', 'Tìm, lọc danh mục · ảnh thực phẩm', 'Đầy đủ'), ('Bữa ăn', 'Lịch 7 ngày × 3 bữa · gợi ý món từ tủ lạnh', 'Đầy đủ'),
        ('Công thức', 'Nguyên liệu động · cách làm HTML', 'Đầy đủ'), ('Báo cáo', '7/30/90 ngày · mua sắm, tiêu thụ, lãng phí, tủ lạnh', 'Đầy đủ'),
        ('Nhóm gia đình', 'Tạo nhóm, thêm/xoá thành viên — cần username', 'Một phần'), ('Hồ sơ cá nhân', 'Chỉ đổi ảnh, mật khẩu; không sửa tên/username', 'Một phần'),
        ('Danh mục & đơn vị', 'Quản trị viên sửa trên mobile', 'Đầy đủ'), ('Web Admin', 'Quản trị người dùng, nhật ký — chỉ có API', 'Chưa có')]
tone = {'Đầy đủ': (GREEN_S, GREEN), 'Một phần': (AMBER_S, AMBER), 'Chưa có': (RED_S, RED)}
for i, (m, d_, st_) in enumerate(mods):
    cx = 0.6 + (i % 3) * 4.1; cy = 1.55 + (i // 3) * 1.33
    f_, c_ = tone[st_]
    card(s, cx, cy, 3.9, 1.18, WHITE, BORDER, 0.1)
    tb(s, cx + 0.2, cy + 0.14, 2.5, 0.35, m, 16, True)
    chip(s, cx + 3.9 - 0.2 - 1.05, cy + 0.15, st_, f_, c_, 11, 1.05)
    tb(s, cx + 0.2, cy + 0.55, 3.55, 0.6, d_, 12.5, False, MUTED)
footer(s, 4)

# ============ 5. IA ============
s = new('Kiến trúc thông tin được dựng từ cây thư mục route của Expo Router. Vùng auth gồm bốn màn hình xác thực. Vùng tabs gồm năm tab: Trang chủ, Đi chợ, Tủ lạnh, Bữa ăn và Cá nhân. Các màn chi tiết như chi tiết danh sách, kho thực phẩm, công thức, báo cáo nằm trên Stack gốc nên thanh tab được ẩn khi mở. Ô màu xanh là modal, ô viền đỏ nét đứt là chức năng chưa có giao diện: lọc tủ lạnh theo danh mục, sửa hồ sơ và toàn bộ Web Admin.')
title(s, 'Information Architecture', 'Cấu trúc giao diện')
picture_fit(s, DG / 'ia_sitemap.png', 0.5, 1.45, 12.33, 5.5)
footer(s, 5)

# ============ 6. User flow ============
s = new('Đây là vòng nghiệp vụ chính của ứng dụng. Mọi thứ bắt đầu từ Kho thực phẩm vì các form đều chọn thực phẩm có sẵn. Trưởng nhóm tạo danh sách, ứng dụng tự mở chi tiết và form thêm món. Thành viên đánh dấu đã mua với cập nhật lạc quan nên phản hồi tức thì. Món được cất vào tủ với hạn dùng, cron 8 giờ sáng gửi nhắc trước 3 ngày. Ở tab Bữa ăn, gợi ý ưu tiên nguyên liệu sắp hết hạn. Ô màu đỏ chỉ ra một điểm chưa liên thông: món đã mua chưa tự chuyển vào tủ lạnh.')
title(s, 'User Flow — vòng Đi chợ → Tủ lạnh → Bữa ăn', 'Cấu trúc giao diện')
picture_fit(s, DG / 'flow_core.png', 0.5, 1.45, 12.33, 5.5)
footer(s, 6)

# ============ 7. Design system ============
s = new('Design system được trích xuất nguyên văn từ thư mục theme. Bảng màu gồm cam, vàng, kem và xanh; quy ước đáng chú ý là màu cam đậm 9A3F00 dùng cho chữ để đủ tương phản, còn cam FF933E chỉ dùng làm nền. Font Be Vietnam Pro được thiết kế cho tiếng Việt, với bảy cấp chữ. Khoảng cách theo bội số 4 và bán kính bo góc 8 đến 24. Đây là design system ở mức token và component trong code; dự án chưa có tài liệu hay Figma riêng.')
title(s, 'Design System trích xuất từ mã nguồn', 'Thiết kế giao diện')
pw, ph = picture_fit(s, DG / 'design_system.png', 0.5, 1.45, 8.6, 5.5)
cx = 9.4
card(s, cx, 1.55, 3.35, 5.3, ORANGE_S, None, 0.06)
tb(s, cx + 0.25, 1.75, 2.9, 0.35, 'Điểm nổi bật', 16, True, ORANGE_D)
bullets(s, cx + 0.25, 2.2, 2.9, 4.5, ['Token màu ngữ nghĩa: primary chỉ làm nền, primaryText cho chữ',
                                       'Be Vietnam Pro — 7 cấp chữ, hiển thị tiếng Việt rõ dấu',
                                       'Spacing 4–32, radius 8–24',
                                       '14 component tự xây, không dùng UI kit',
                                       [('Chữ trắng trên nền cam chỉ đạt 2,21:1', {'bold': True, 'color': RED})]], 13.5, BROWN, 9)
footer(s, 7)

# ============ 8–15. Màn hình ============
screen_slide(8, 'Thiết kế màn hình', 'Trang chủ — tổng quan trong ngày',
             [('10_home', 'Trưởng nhóm có dữ liệu'), ('11_home_no_group', 'Người chưa có nhóm')],
             [('Dashboard dạng thẻ', 'Mỗi thẻ trả lời một câu hỏi: tủ lạnh, đi chợ, bữa ăn, công thức, báo cáo.'),
              ('StatTile theo màu ngữ nghĩa', 'Tổng · Sắp hết hạn · Đã hết hạn; tiến độ mua 3/8 món, 38%.'),
              ('Lối tắt một chạm', 'Xem tất cả, Mở danh sách, Xem lịch, avatar → Cá nhân.'),
              ('Trạng thái chưa có nhóm', 'EmptyState với nút “Thiết lập nhóm”.')],
             'Trang chủ là trạm trung chuyển của ứng dụng. Dải tiêu đề cam chào người dùng kèm thứ ngày. Bên dưới là năm thẻ: tủ lạnh hôm nay với ba ô số liệu, danh sách mua sắm với tiến độ, bữa ăn hôm nay theo sáng trưa tối, và lối vào công thức, báo cáo. Mỗi thẻ có liên kết đi thẳng tới chức năng chi tiết. Ảnh bên phải là trạng thái của người chưa tham gia nhóm: thay vì màn trống, ứng dụng giải thích và đưa nút thiết lập nhóm.')

screen_slide(9, 'Thiết kế màn hình', 'Đi chợ — danh sách và phân công',
             [('20_shopping', 'Danh sách'), ('22_shopping_detail', 'Chi tiết'), ('21_shopping_create_modal', 'Tạo danh sách')],
             [('Thẻ danh sách giàu thông tin', 'Người được giao, badge x/y, progress, 4 món đầu.'),
              ('Đánh dấu ngay trên thẻ', 'Mọi thành viên tick được; cập nhật lạc quan.'),
              ('Hiển thị theo quyền', 'Chỉ trưởng nhóm thấy Tạo, Sửa, Xoá.'),
              ('Bớt một bước', 'Tạo xong tự mở chi tiết và form thêm món.')],
             'Tab Đi chợ hiển thị các danh sách của nhóm. Mỗi thẻ cho biết ai được giao, đã mua bao nhiêu món qua badge và thanh tiến độ, và cho tick món ngay trên thẻ. Món đã mua có dấu tích xanh và gạch ngang. Form tạo danh sách là modal gồm tên, người được giao, ngày và ghi chú; sau khi lưu, ứng dụng tự chuyển sang chi tiết và mở sẵn form thêm món, vì hai thao tác này luôn đi liền nhau. Các nút tạo, sửa, xoá chỉ hiện với trưởng nhóm.', ph_h=5.0)

screen_slide(10, 'Thiết kế màn hình', 'Tủ lạnh — theo dõi hạn sử dụng',
             [('30_fridge', 'Danh sách trong tủ'), ('31_fridge_add_modal', 'Thêm món'), ('32_fridge_datefield', 'Chọn hạn dùng')],
             [('Badge hạn dùng 3 màu', 'Đỏ: đã/hôm nay hết hạn · vàng: ≤ 3 ngày · xanh: còn hạn.'),
              ('Thông tin một dòng', 'Số lượng · vị trí · ngày hết hạn, ảnh hoặc chữ cái đầu.'),
              ('Form gợi ý sẵn', 'Hạn mặc định +7 ngày, vị trí chọn từ 4 lựa chọn.'),
              ('Nhắc trước 3 ngày', 'Cron 08:00 + Expo Push → bấm mở tab Tủ lạnh.')],
             'Tab Tủ lạnh tập trung vào hạn sử dụng. Ba ô số liệu ở đầu cho biết tổng số món, số món sắp hết hạn và đã hết hạn. Mỗi món có badge màu: đỏ khi đã hoặc hôm nay hết hạn, vàng khi còn từ một đến ba ngày, xanh khi còn hạn. Form thêm món đặt sẵn hạn dùng bảy ngày và dùng lịch tháng tự xây dựng, tuần bắt đầu từ thứ hai. Backend gửi thông báo đẩy lúc 8 giờ sáng cho món sắp hết hạn; phần này chưa được kiểm chứng trên điện thoại thật.', ph_h=5.0)

screen_slide(11, 'Thiết kế màn hình', 'Kho thực phẩm — nguồn dữ liệu chung',
             [('35_food', 'Danh sách kho'), ('37_food_add_modal', 'Thêm thực phẩm')],
             [('Nguồn cho mọi form', 'Đi chợ, tủ lạnh, bữa ăn, công thức đều chọn thực phẩm từ kho.'),
              ('Tìm và lọc nhanh', 'Ô tìm kiếm + chip danh mục cuộn ngang.'),
              ('Ảnh thực phẩm', 'Thư viện hoặc camera, ≤ 5MB; thiếu ảnh dùng chữ cái đầu.'),
              ('Quyền sửa/xoá', 'Chỉ người tạo hoặc trưởng nhóm.')],
             'Kho thực phẩm được mở từ tab Tủ lạnh. Đây là danh mục thực phẩm riêng của nhóm và là nguồn dữ liệu cho mọi form khác: khi kho trống, các form đều hiển thị hướng dẫn thêm thực phẩm trước. Màn hình có ô tìm kiếm, chip lọc theo danh mục, mỗi dòng gồm ảnh, tên, danh mục và đơn vị. Form thêm hỗ trợ chọn ảnh từ thư viện hoặc chụp bằng camera. Nút sửa và xoá chỉ hiện với người tạo hoặc trưởng nhóm.')

screen_slide(12, 'Thiết kế màn hình', 'Bữa ăn — lịch và gợi ý món',
             [('40_meal', 'Lịch 7 ngày'), ('41_meal_suggestion', 'Gợi ý từ tủ lạnh')],
             [('Dải 7 ngày', 'Hôm nay có viền, ngày chọn nền cam; 3 thẻ Sáng/Trưa/Tối.'),
              ('Bottom sheet gợi ý', 'Lý do “Dùng Đậu phụ còn 2 ngày”, khớp x/y nguyên liệu.'),
              ('Từ gợi ý đến hành động', 'Xem công thức hoặc Thêm vào bữa ăn với dữ liệu điền sẵn.'),
              ('Theo quyền', 'Thành viên chỉ xem; trưởng nhóm thêm, sửa, xoá.')],
             'Tab Bữa ăn có dải bảy ngày ở đầu để chọn ngày, sau đó là ba thẻ sáng, trưa, tối. Nút gợi ý mở một bottom sheet: mỗi gợi ý ghi rõ lý do, ví dụ dùng đậu phụ còn hai ngày, số nguyên liệu khớp và nguyên liệu còn thiếu. Gợi ý được xếp ưu tiên món dùng nguyên liệu sắp hết hạn, đúng mục tiêu giảm lãng phí. Từ gợi ý, trưởng nhóm thêm ngay vào bữa ăn. Hạn chế là lịch chỉ hiển thị bảy ngày tới và món trong bữa là thực phẩm chứ chưa phải công thức.')

screen_slide(13, 'Thiết kế màn hình', 'Công thức nấu ăn',
             [('50_recipes', 'Danh sách'), ('51_recipe_detail', 'Chi tiết'), ('52_recipe_editor', 'Soạn công thức')],
             [('Tìm kiếm cục bộ', 'Theo tên, thực phẩm, mô tả.'),
              ('Chi tiết dễ đọc', 'Nguyên liệu – định lượng, cách làm hiển thị HTML.'),
              ('Nguyên liệu động', 'Thêm/xoá dòng, không trùng, số lượng dương.'),
              ('Soạn dạng văn bản', 'Mỗi dòng một bước, tự chuyển thành HTML.')],
             'Chức năng Công thức được truy cập từ Trang chủ hoặc Bữa ăn. Danh sách có ô tìm kiếm và thẻ công thức hiển thị số nguyên liệu và mô tả. Màn chi tiết trình bày nguyên liệu kèm định lượng và cách làm được render từ HTML. Form soạn cho phép thêm bớt dòng nguyên liệu, kiểm tra không trùng và số lượng dương; phần cách làm nhập như văn bản thường, mỗi dòng một bước, ứng dụng tự chuyển thành HTML nên người dùng không cần biết định dạng.', ph_h=5.0)

screen_slide(14, 'Thiết kế màn hình', 'Nhóm gia đình và Cá nhân',
             [('60_profile', 'Cá nhân'), ('61_group_manage', 'Quản lý nhóm'), ('64_group_setup', 'Thiết lập nhóm')],
             [('Tài khoản & nhóm', 'Avatar có huy hiệu camera, thông tin nhóm, vai trò.'),
              ('Quản lý thành viên', 'Thêm bằng username, badge “Trưởng nhóm”, rời nhóm.'),
              ('Bảo mật & thông báo', 'Đổi mật khẩu, trạng thái quyền nhận nhắc hết hạn.'),
              ('Hạn chế', 'Không sửa tên/username → tài khoản mới khó vào nhóm.')],
             'Tab Cá nhân gom tài khoản, nhóm gia đình, bảo mật, thông báo và các lối vào phụ như báo cáo, danh mục. Màn quản lý nhóm cho trưởng nhóm thêm thành viên bằng username và xoá thành viên; mọi người đều có thể rời nhóm, trưởng nhóm được cảnh báo về chuyển quyền. Màn thiết lập nhóm hiển thị username để gửi cho trưởng nhóm. Hạn chế quan trọng: ứng dụng không có màn sửa hồ sơ, còn đăng ký không tạo username, nên tài khoản mới không thể được thêm vào nhóm qua ứng dụng.', ph_h=5.0)

screen_slide(15, 'Thiết kế màn hình', 'Báo cáo và thống kê',
             [('70_reports_shopping', 'Tổng quan + Mua sắm'), ('72_reports_waste', 'Lãng phí'), ('73_reports_fridge', 'Tủ lạnh')],
             [('Khoảng thời gian', 'Chip 7 / 30 / 90 ngày.'),
              ('4 nhóm báo cáo', 'Mua sắm · Tiêu thụ · Lãng phí · Tủ lạnh.'),
              ('Biểu đồ tự vẽ', 'BarChart bằng View, cột đôi cần mua / đã mua.'),
              ('Giải thích chỉ số', 'Tỉ lệ lãng phí = bỏ đi / tổng đã xử lý.')],
             'Màn Báo cáo có chip chọn khoảng 7, 30 hoặc 90 ngày, thẻ tổng quan và bốn tab báo cáo. Mỗi tab chỉ tải dữ liệu khi được chọn. Biểu đồ cột được vẽ bằng View thay vì thư viện chart, hỗ trợ cột đôi và cuộn ngang. Ứng dụng giải thích công thức tỉ lệ lãng phí ngay dưới số liệu. Lưu ý: dữ liệu trong ảnh là dữ liệu mẫu tạo trong một ngày nên biểu đồ chỉ có một cột và tỉ lệ 71% không phản ánh người dùng thật.', ph_h=5.0)

# ============ 16. Trạng thái & tương tác ============
s = new('Ứng dụng xử lý trạng thái rất nhất quán. Ba component dùng chung cho đang tải, rỗng và lỗi được áp dụng ở mọi danh sách, luôn kèm câu mô tả theo ngữ cảnh và nút hành động như thử lại hoặc thiết lập nhóm. Form kiểm tra dữ liệu trước khi gửi và hiển thị lỗi bằng banner đỏ; thông báo thành công màu xanh tự ẩn sau 5 giây. Thao tác xoá luôn có hộp thoại xác nhận nêu rõ hậu quả. Ảnh trạng thái tải và lỗi được chụp bằng cách giữ hoặc huỷ request mạng trong trình duyệt kiểm thử.')
title(s, 'Trạng thái và tương tác', 'Thiết kế tương tác')
items = [('90_loading_state', 'Loading', ORANGE_D), ('11_home_no_group', 'Empty', AMBER), ('91_error_state', 'Error', RED), ('02_login_error', 'Validation', BLUE_D)]
x = 0.6
for nm, lb, c_ in items:
    w = phone(s, nm, x, 1.55, 4.5)
    chip(s, x + w / 2 - 0.65, 6.2, lb, ORANGE_S, c_, 12, 1.3)
    x += w + 0.25
cx = x + 0.3
bullets(s, cx, 1.65, SW - 0.6 - cx, 5.2, [[('Loading / Empty / Error', {'bold': True})], 'Một bộ component cho mọi danh sách, luôn có hành động kèm theo',
                                 [('Validation 2 lớp', {'bold': True})], 'Kiểm tra trước khi gửi + thông điệp tiếng Việt từ backend',
                                 [('Phản hồi', {'bold': True})], 'Banner thành công tự ẩn 5 giây, “Đang xoá...”, tick lạc quan',
                                 [('Xác nhận', {'bold': True})], 'Alert trước mọi thao tác xoá, nêu rõ hậu quả'], 13.5, BROWN, 4)
footer(s, 16)

# ============ 17. Đánh giá & hướng phát triển ============
s = new('Về điểm mạnh: giao diện nhất quán nhờ token và component dùng chung, xử lý trạng thái đầy đủ, hiển thị theo quyền và nhiều chi tiết giảm bước thao tác. Về hạn chế: thiếu màn sửa hồ sơ làm tắc luồng tham gia nhóm; chữ trắng trên nền cam không đạt chuẩn tương phản; nhãn thanh tab bị cắt trên bản web cần kiểm tra lại trên máy thật; các module chưa liên thông và Web Admin chưa có. Hướng phát triển được sắp theo ưu tiên ở cột bên phải.')
title(s, 'Đánh giá và hướng phát triển', 'Đánh giá')
card(s, 0.6, 1.55, 3.9, 5.3, GREEN_S, None, 0.05)
tb(s, 0.85, 1.75, 3.4, 0.35, 'Điểm mạnh', 18, True, GREEN)
bullets(s, 0.85, 2.25, 3.45, 4.5, ['Nhất quán nhờ token + 14 component', 'Loading/Empty/Error ở mọi danh sách', 'Hiển thị theo quyền, thông điệp rõ', 'Cập nhật lạc quan, tự mở form tiếp theo', 'Accessibility role/state đầy đủ cho nút, checkbox, tab'], 14, BROWN, 8)
card(s, 4.72, 1.55, 3.9, 5.3, RED_S, None, 0.05)
tb(s, 4.97, 1.75, 3.4, 0.35, 'Hạn chế', 18, True, RED)
bullets(s, 4.97, 2.25, 3.45, 4.5, ['Không có màn sửa hồ sơ / username', 'Chữ trắng trên cam: 2,21 : 1', 'Nhãn tab bị cắt trên bản web', 'Món đã mua chưa tự vào tủ; tủ chưa có lọc', 'Web Admin chưa khởi tạo'], 14, BROWN, 8)
tb(s, 8.9, 1.62, 3.8, 0.35, 'Lộ trình đề xuất', 18, True)
road = [('Cao', 'Màn sửa hồ sơ + username sau đăng ký', ORANGE_S, ORANGE_D), ('Cao', 'Tăng tương phản tiêu đề, kiểm tra tab bar', ORANGE_S, ORANGE_D),
        ('Trung bình', '“Thêm vào tủ lạnh” khi đã mua; lọc tủ', AMBER_S, AMBER), ('Trung bình', 'Tách ModalForm, Chip, Toast dùng chung', AMBER_S, AMBER),
        ('Thấp', 'Dark mode, onboarding, Web Admin', BLUE_S, BLUE_D)]
y = 2.15
for lv, txt, f_, c_ in road:
    card(s, 8.9, y, 3.85, 0.85, WHITE, BORDER, 0.12)
    chip(s, 9.05, y + 0.27, lv, f_, c_, 10.5, 1.15)
    tb(s, 10.3, y + 0.1, 2.35, 0.7, txt, 12.5, False, BROWN, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.95
footer(s, 17)

# ============ 18. Kết luận ============
s = new('Tóm lại, ứng dụng Đi chợ tiện lợi đã có giao diện đầy đủ cho các nghiệp vụ cốt lõi với 17 màn hình quanh năm tab, xây trên một design system ở mức token và component trong code. Báo cáo được lập hoàn toàn từ mã nguồn và ảnh chụp thực tế, phân biệt rõ phần đã triển khai, triển khai một phần và chưa có. Các hướng phát triển có thể thực hiện tuần tự mà không phải thay đổi kiến trúc giao diện. Nhóm xin cảm ơn thầy cô và các bạn đã lắng nghe, rất mong nhận được góp ý.', dark=True, layout='Title Slide')
_pn = card(s, 0.4, 0.5, 7.9, 6.55, ORANGE, None, 0.04)
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

prs.core_properties.title = 'Thiết kế giao diện Đi chợ tiện lợi'
prs.core_properties.author = 'Nhóm Đi chợ tiện lợi'
prs.save(OUT)
print('saved', OUT, len(prs.slides))
