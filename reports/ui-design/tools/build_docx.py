# -*- coding: utf-8 -*-
"""Tạo Bao_cao_thiet_ke_giao_dien_Di_cho_tien_loi.docx bằng python-docx."""
from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path('D:/Project/di-cho-tien-loi/reports/ui-design')
SS = ROOT / 'assets/screenshots'
DG = ROOT / 'assets/diagrams'
OUT = ROOT / 'Bao_cao_thiet_ke_giao_dien_Di_cho_tien_loi.docx'
FONT = 'Times New Roman'
BROWN = RGBColor(0x2A, 0x1A, 0x0F)
ACCENT = RGBColor(0x9A, 0x3F, 0x00)

doc = Document()

# ---------------- styles ----------------
def set_font(style_or_run, size=None, bold=None, italic=None, color=None):
    f = style_or_run.font
    f.name = FONT
    rpr = style_or_run.element.get_or_add_rPr() if hasattr(style_or_run.element, 'get_or_add_rPr') else style_or_run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.insert(0, rf)
    for a in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
    for a in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        rf.set(qn(a), FONT)
    if size: f.size = Pt(size)
    if bold is not None: f.bold = bold
    if italic is not None: f.italic = italic
    if color is not None: f.color.rgb = color

st = doc.styles
normal = st['Normal']
set_font(normal, 13)
pf = normal.paragraph_format
pf.line_spacing = 1.3
pf.space_after = Pt(6)
pf.space_before = Pt(0)
pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

for lvl, size, before, after, ital in [(1, 16, 18, 10, False), (2, 14, 14, 6, False), (3, 13, 10, 4, True)]:
    s = st[f'Heading {lvl}']
    set_font(s, size, True, ital, BROWN)
    s.paragraph_format.space_before = Pt(before)
    s.paragraph_format.space_after = Pt(after)
    s.paragraph_format.keep_with_next = True
    s.paragraph_format.line_spacing = 1.2
    s.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
st['Heading 1'].paragraph_format.page_break_before = True

cap = st['Caption']
set_font(cap, 11.5, False, True, RGBColor(0x40, 0x30, 0x25))
cap.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
cap.paragraph_format.space_before = Pt(2)
cap.paragraph_format.space_after = Pt(10)
cap.paragraph_format.line_spacing = 1.1

for nm in ('List Bullet', 'List Number'):
    set_font(st[nm], 13)
    st[nm].paragraph_format.line_spacing = 1.3
    st[nm].paragraph_format.space_after = Pt(3)

# Table text style
tstyle = st.add_style('TableText', 1)
tstyle.base_style = normal
set_font(tstyle, 10.5)
tstyle.paragraph_format.line_spacing = 1.1
tstyle.paragraph_format.space_after = Pt(1)
tstyle.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

# ---------------- page setup ----------------
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21), Cm(29.7)
sec.top_margin, sec.bottom_margin = Cm(2), Cm(2)
sec.left_margin, sec.right_margin = Cm(3), Cm(2)
sec.header_distance = sec.footer_distance = Cm(1.1)
TEXT_W = 16.0  # cm

# ---------------- helpers ----------------
def add_field(par, instr, placeholder=''):
    r = par.add_run(); b = OxmlElement('w:fldChar'); b.set(qn('w:fldCharType'), 'begin'); r._r.append(b)
    r = par.add_run(); t = OxmlElement('w:instrText'); t.set(qn('xml:space'), 'preserve'); t.text = f' {instr} '; r._r.append(t)
    r = par.add_run(); s = OxmlElement('w:fldChar'); s.set(qn('w:fldCharType'), 'separate'); r._r.append(s)
    r = par.add_run(placeholder)
    r = par.add_run(); e = OxmlElement('w:fldChar'); e.set(qn('w:fldCharType'), 'end'); r._r.append(e)


def P(text='', style=None, bold=False, italic=False, align=None, size=None, after=None, color=None, indent=True):
    p = doc.add_paragraph(style=style)
    if text:
        add_rich(p, text, bold, italic, size, color)
    if align is not None: p.alignment = align
    if after is not None: p.paragraph_format.space_after = Pt(after)
    if indent and style is None and align is None:
        p.paragraph_format.first_line_indent = Cm(1)
    return p


def add_rich(p, text, bold=False, italic=False, size=None, color=None):
    """**đậm** và `code` trong chuỗi."""
    import re
    parts = re.split(r'(\*\*[^*]+\*\*|`[^`]+`)', text)
    for part in parts:
        if not part: continue
        if part.startswith('**'):
            r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith('`'):
            r = p.add_run(part[1:-1]); r.font.name = 'Consolas'; r.font.size = Pt((size or 13) - 2)
            r._r.get_or_add_rPr().get_or_add_rFonts().set(qn('w:hAnsi'), 'Consolas')
            continue
        else:
            r = p.add_run(part); r.bold = bold or None
        r.italic = italic or None
        if size: r.font.size = Pt(size)
        if color is not None: r.font.color.rgb = color


def B(items, style='List Bullet'):
    for it in items:
        p = doc.add_paragraph(style=style)
        add_rich(p, it)
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def H(text, lvl):
    return doc.add_heading(text, lvl)


def caption(kind, text):
    p = doc.add_paragraph(style='Caption')
    r = p.add_run(f'{kind} '); r.bold = True; r.italic = False
    add_field(p, f'SEQ {kind} \\* ARABIC', '#')
    r2 = p.runs[-1]
    r = p.add_run('. '); r.bold = True; r.italic = False
    p.add_run(text)
    # số của SEQ cũng in đậm
    for run in p.runs[1:5]:
        run.bold = True; run.italic = False
    return p


def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), hexcolor)
    tcPr.append(sh)


def set_borders(table, color='BFAE9C', none=False):
    tbl = table._tbl
    tblPr = tbl.tblPr
    borders = OxmlElement('w:tblBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'nil' if none else 'single')
        if not none:
            el.set(qn('w:sz'), '4'); el.set(qn('w:space'), '0'); el.set(qn('w:color'), color)
        borders.append(el)
    tblPr.append(borders)


def set_cell_width(cell, cm):
    cell.width = Cm(cm)



def fix_widths(table, widths_cm):
    tbl = table._tbl; tblPr = tbl.tblPr
    total = int(sum(widths_cm) * 567)
    for tag in ('w:tblW', 'w:tblLayout'):
        old = tblPr.find(qn(tag))
        if old is not None: tblPr.remove(old)
    tw = OxmlElement('w:tblW'); tw.set(qn('w:w'), str(total)); tw.set(qn('w:type'), 'dxa'); tblPr.append(tw)
    lay = OxmlElement('w:tblLayout'); lay.set(qn('w:type'), 'fixed'); tblPr.append(lay)
    grid = tbl.tblGrid
    for i, gc in enumerate(grid.findall(qn('w:gridCol'))):
        gc.set(qn('w:w'), str(int(widths_cm[i] * 567)))
    for row in table.rows:
        for i, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            old = tcPr.find(qn('w:tcW'))
            if old is not None: tcPr.remove(old)
            w = OxmlElement('w:tcW'); w.set(qn('w:w'), str(int(widths_cm[i] * 567))); w.set(qn('w:type'), 'dxa'); tcPr.insert(0, w)

def T(headers, rows, widths, cap=None, header_fill='FFE9D6', font=10.5, first_bold=False):
    if cap:
        c = caption('Bảng', cap)
        c.paragraph_format.keep_with_next = True
        c.paragraph_format.space_after = Pt(4)
    t = doc.add_table(rows=1, cols=len(headers))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    set_borders(t)
    for i, h in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]; p.style = 'TableText'
        r = p.add_run(h); r.bold = True; r.font.size = Pt(font)
        shade(cell, header_fill)
        set_cell_width(cell, widths[i])
    # lặp tiêu đề khi sang trang
    trPr = t.rows[0]._tr.get_or_add_trPr(); th = OxmlElement('w:tblHeader'); th.set(qn('w:val'), 'true'); trPr.append(th)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cell = cells[i]; cell.text = ''
            set_cell_width(cell, widths[i])
            p = cell.paragraphs[0]; p.style = 'TableText'
            lines = str(val).split('\n')
            for li, line in enumerate(lines):
                if li: p = cell.add_paragraph(style='TableText')
                add_rich(p, line, bold=(first_bold and i == 0), size=font)
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    # cột độ rộng
    fix_widths(t, widths)
    if len(rows) <= 12:
        for row in t.rows[:-1]:
            for c_ in row.cells:
                for pp in c_.paragraphs: pp.paragraph_format.keep_with_next = True
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr(); cs = OxmlElement('w:cantSplit'); cs.set(qn('w:val'), 'true'); trPr.append(cs)
    sp = doc.add_paragraph(); sp.paragraph_format.space_after = Pt(0); sp.paragraph_format.line_spacing = 0.8
    return t


def FIG(path, width_cm, cap):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(str(path), width=Cm(width_cm))
    caption('Hình', cap)


def SHOTS(items, cap, width_cm=4.4):
    """items: [(file, nhãn)] — ảnh chụp thật đặt cạnh nhau trong bảng không viền."""
    t = doc.add_table(rows=2, cols=len(items))
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_borders(t, none=True)
    for i, (f, label) in enumerate(items):
        c = t.rows[0].cells[i]; p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(); run.add_picture(str(SS / f'{f}.png'), width=Cm(width_cm))
        c2 = t.rows[1].cells[i]; p2 = c2.paragraphs[0]; p2.style = 'TableText'; p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p2.add_run(label); r.italic = True; r.font.size = Pt(10.5)
        for c_ in (c, c2): c_.width = Cm(width_cm + 0.6)
    # giữ hàng ảnh không bị tách trang
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr(); cs = OxmlElement('w:cantSplit'); cs.set(qn('w:val'), 'true'); trPr.append(cs)
    fix_widths(t, [width_cm + 0.6] * len(items))
    for c_ in t.rows[0].cells + t.rows[1].cells:
        for pp in c_.paragraphs: pp.paragraph_format.keep_with_next = True
    caption('Hình', cap)


def SCREEN(rows):
    """Bảng mô tả màn hình: [(thuộc tính, mô tả)]."""
    T(['Thuộc tính', 'Mô tả'], rows, [3.2, 12.8], font=10.5, first_bold=True)


# ---------------- header / footer ----------------
sec.different_first_page_header_footer = True
hp = sec.header.paragraphs[0]
hp.text = ''
hr = hp.add_run('Báo cáo phân tích và thiết kế giao diện — Hệ thống Đi chợ tiện lợi')
hr.italic = True; hr.font.size = Pt(10); hr.font.color.rgb = RGBColor(0x7A, 0x66, 0x56)
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
pPr = hp._p.get_or_add_pPr(); bdr = OxmlElement('w:pBdr'); bt = OxmlElement('w:bottom')
bt.set(qn('w:val'), 'single'); bt.set(qn('w:sz'), '4'); bt.set(qn('w:space'), '1'); bt.set(qn('w:color'), 'C9B49C'); bdr.append(bt); pPr.append(bdr)
fp = sec.footer.paragraphs[0]; fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = fp.add_run('IT4788 – Phát triển ứng dụng đa nền tảng   ·   Trang '); r.font.size = Pt(10)
add_field(fp, 'PAGE', '1')
for rr in fp.runs: rr.font.size = Pt(10)

# ================= TRANG BÌA =================
def cover_line(text, size, bold=False, before=0, after=6, color=BROWN, italic=False):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(before); p.paragraph_format.space_after = Pt(after)
    r = p.add_run(text); r.bold = bold; r.italic = italic; r.font.size = Pt(size); r.font.color.rgb = color
    return p

cover_line('ĐẠI HỌC BÁCH KHOA HÀ NỘI', 14, True, 0, 2)
cover_line('Học phần IT4788 – Phát triển ứng dụng đa nền tảng', 13, False, 0, 2)
cover_line('_______________________', 12, False, 0, 40, ACCENT)
cover_line('BÁO CÁO', 18, True, 30, 6)
cover_line('PHÂN TÍCH VÀ THIẾT KẾ GIAO DIỆN', 22, True, 0, 4, ACCENT)
cover_line('HỆ THỐNG ĐI CHỢ TIỆN LỢI', 22, True, 0, 26, ACCENT)
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run().add_picture(str(ROOT / 'assets/illustrations/mockup_10_home.png'), height=Cm(8.2))
p.add_run('    ')
p.add_run().add_picture(str(ROOT / 'assets/illustrations/mockup_30_fridge.png'), height=Cm(8.2))
p.add_run('    ')
p.add_run().add_picture(str(ROOT / 'assets/illustrations/mockup_40_meal.png'), height=Cm(8.2))
cover_line('Ảnh chụp giao diện thực tế của ứng dụng (React Native + Expo + TypeScript)', 11, False, 4, 30, RGBColor(0x7A, 0x66, 0x56), True)
cover_line('Nhóm thực hiện: ………………………………………………', 13, False, 0, 4)
cover_line('Giảng viên hướng dẫn: ………………………………………', 13, False, 0, 30)
cover_line('Hà Nội, tháng 11 năm 2026', 13, True, 0, 0)

# ================= MỤC LỤC =================
p = doc.add_paragraph(); p.add_run().add_break(WD_BREAK.PAGE)
cover_line('MỤC LỤC', 16, True, 0, 12)
p = doc.add_paragraph(); add_field(p, 'TOC \\o "1-3" \\h \\z \\u', 'Nhấn F9 để cập nhật mục lục.')
p = doc.add_paragraph(); p.add_run().add_break(WD_BREAK.PAGE)
cover_line('DANH MỤC HÌNH', 16, True, 0, 12)
p = doc.add_paragraph(); add_field(p, 'TOC \\h \\z \\c "Hình"', 'Nhấn F9 để cập nhật danh mục hình.')
cover_line('DANH MỤC BẢNG', 16, True, 18, 12)
p = doc.add_paragraph(); add_field(p, 'TOC \\h \\z \\c "Bảng"', 'Nhấn F9 để cập nhật danh mục bảng.')

# ================= CHƯƠNG 1 =================
H('CHƯƠNG 1. GIỚI THIỆU', 1)
H('1.1. Tổng quan dự án', 2)
P('“Đi chợ tiện lợi” là bài tập lớn của học phần IT4788 – Phát triển ứng dụng đa nền tảng. Sản phẩm gồm một ứng dụng di động đa nền tảng xây dựng bằng React Native, Expo và TypeScript, kết nối với một backend Node.js/Express sử dụng cơ sở dữ liệu MongoDB. Ứng dụng giúp một gia đình cùng quản lý danh sách đi chợ, theo dõi thực phẩm trong tủ lạnh, nhận nhắc nhở trước khi thực phẩm hết hạn, lên kế hoạch bữa ăn, lưu công thức nấu ăn và xem báo cáo mua sắm – tiêu thụ – lãng phí; toàn bộ dữ liệu được chia sẻ trong phạm vi một **nhóm gia đình**.')
P('Báo cáo này phân tích và mô tả thiết kế giao diện **dựa trên sản phẩm thực tế**: mọi màn hình, thành phần và luồng thao tác được trình bày đều được đối chiếu trực tiếp với mã nguồn trong repository (thư mục `mobile/src`, `server/src`) tại commit `335e386`. Hình ảnh giao diện là ảnh chụp ứng dụng đang chạy, không phải mockup vẽ lại. Những chức năng chỉ có ở backend hoặc chỉ là định hướng trong tài liệu kế hoạch được đánh dấu rõ là chưa có giao diện.')
H('1.2. Mục tiêu hệ thống', 2)
B(['Giảm thời gian và sự trùng lặp khi đi chợ nhờ danh sách mua sắm dùng chung, có phân công người đi chợ và theo dõi tiến độ theo thời gian thực.',
   'Giảm lãng phí thực phẩm bằng cách theo dõi hạn sử dụng, phân loại món sắp hết hạn bằng màu sắc và gửi thông báo đẩy trước 3 ngày.',
   'Hỗ trợ lập kế hoạch bữa ăn theo ngày và gợi ý món nấu được từ nguyên liệu đang có, ưu tiên nguyên liệu sắp hết hạn.',
   'Lưu trữ công thức nấu ăn của gia đình và cung cấp số liệu thống kê để gia đình điều chỉnh thói quen mua sắm.'])
H('1.3. Đối tượng sử dụng', 2)
P('Người dùng chính là các thành viên trong một hộ gia đình sử dụng điện thoại thông minh. Trong mã nguồn, quyền hạn được phân thành ba mức: **thành viên nhóm**, **trưởng nhóm** (người tạo nhóm, `group.adminId`) và **quản trị viên hệ thống** (`role = admin`). Ngoài ra, ứng dụng xử lý riêng trạng thái **người dùng chưa thuộc nhóm nào**.')
H('1.4. Phạm vi thiết kế', 2)
P('Phạm vi khảo sát bao gồm toàn bộ giao diện của ứng dụng di động: 17 màn hình nghiệp vụ, 5 tab điều hướng chính, các modal/bottom sheet và hộp thoại xác nhận. Backend được khảo sát ở mức các API, trường dữ liệu, quy tắc nghiệp vụ và phân quyền có ảnh hưởng tới giao diện. Trang quản trị web (Web Admin) được xác định là **chưa triển khai**: repository không có thư mục `admin/`, tài liệu `docs/README.md` ghi rõ mục “Chưa làm: Trang admin web”; phần quản trị duy nhất có giao diện là màn “Danh mục & đơn vị” trong ứng dụng di động.')
H('1.5. Công nghệ', 2)
T(['Thành phần', 'Công nghệ (theo package.json)', 'Vai trò đối với giao diện'], [
    ['Nền tảng di động', 'Expo SDK ~58, React Native 0.88.1, React 19.3, TypeScript ~6.0', 'Một mã nguồn cho Android và iOS; React Compiler được bật'],
    ['Điều hướng', 'Expo Router ~58 (file-based routing), react-native-screens', 'Mỗi file trong `src/app` là một màn hình; nhóm `(auth)`, `(tabs)`'],
    ['Dữ liệu', 'TanStack Query 5, Zustand 5, Axios', 'Cache, làm mới, cập nhật lạc quan; lưu phiên; tự làm mới token'],
    ['Giao diện', 'Thành phần tự xây dựng, font Be Vietnam Pro, @expo/vector-icons', 'Không dùng UI kit bên thứ ba'],
    ['Thiết bị', 'expo-image-picker, expo-notifications, expo-secure-store', 'Chụp/chọn ảnh, thông báo đẩy, lưu token an toàn'],
    ['Nội dung', 'react-native-render-html, dayjs (locale vi)', 'Hiển thị cách làm công thức dạng HTML; định dạng ngày tiếng Việt'],
    ['Backend', 'Node.js, Express 5, Mongoose 9, Joi, JWT, Cloudinary, Nodemailer, node-cron', 'Cung cấp API `/it4788`, thông điệp lỗi tiếng Việt hiển thị trực tiếp trên UI'],
], [3.2, 6.6, 6.2], 'Công nghệ sử dụng trong dự án')
FIG(DG / 'architecture.png', 16, 'Kiến trúc tổng thể liên quan đến giao diện')

# ================= CHƯƠNG 2 =================
H('CHƯƠNG 2. PHÂN TÍCH YÊU CẦU', 1)
H('2.1. Bài toán thực tế', 2)
P('Trong một gia đình, việc đi chợ thường do nhiều người đảm nhận vào những thời điểm khác nhau. Khi danh sách cần mua chỉ được ghi trên giấy hoặc trao đổi qua tin nhắn, các thành viên dễ mua trùng, mua thiếu, hoặc không biết trong tủ lạnh còn gì. Thực phẩm bị quên lâu ngày dẫn tới hết hạn và phải bỏ đi. Việc lên thực đơn hằng ngày cũng tốn công khi không nắm được nguyên liệu sẵn có. Bài toán đặt ra là xây dựng một ứng dụng di động cho phép cả gia đình chia sẻ cùng một nguồn dữ liệu về mua sắm, tủ lạnh và bữa ăn.')
H('2.2. Người dùng và vai trò', 2)
T(['Vai trò', 'Xác định trong code', 'Quyền trên giao diện (đã đối chiếu service backend)'], [
    ['Người dùng chưa có nhóm', '`user.groupId = null`; API trả mã `00096`, `00185`, `00385`', 'Thấy trạng thái “Bạn chưa tham gia nhóm”, chỉ có thể tạo nhóm, đổi ảnh, đổi mật khẩu'],
    ['Thành viên nhóm', 'Thuộc `group.members`', 'Xem mọi dữ liệu nhóm; đánh dấu đã mua; thêm/sửa/xoá món trong tủ lạnh; thêm/sửa/xoá công thức; thêm thực phẩm vào kho (sửa/xoá thực phẩm do mình tạo)'],
    ['Trưởng nhóm', '`group.adminId === user.id`', 'Thêm quyền: thêm/xoá thành viên; tạo/sửa/xoá danh sách đi chợ và món cần mua; lập/sửa/xoá kế hoạch bữa ăn; sửa/xoá mọi thực phẩm trong kho'],
    ['Quản trị viên hệ thống', '`user.role === "admin"`', 'Thêm/sửa/xoá danh mục và đơn vị đo (màn Danh mục & đơn vị). Quản trị người dùng và nhật ký chỉ có API, chưa có giao diện'],
], [3.4, 4.6, 8.0], 'Vai trò người dùng và quyền hạn trên giao diện')
H('2.3. Nhu cầu sử dụng', 2)
B(['Nắm nhanh tình hình trong ngày: tủ lạnh còn gì, món nào sắp hết hạn, còn bao nhiêu món cần mua, hôm nay ăn gì.',
   'Phân công và theo dõi việc đi chợ: ai được giao, đã mua được bao nhiêu món.',
   'Ghi nhận thực phẩm cất vào tủ cùng hạn sử dụng và vị trí, được nhắc trước khi hết hạn.',
   'Lên thực đơn, nhận gợi ý món nấu được từ nguyên liệu đang có, xem cách nấu.',
   'Theo dõi số liệu mua sắm, tiêu thụ và lãng phí trong một khoảng thời gian.'])
H('2.4. Yêu cầu chức năng', 2)
T(['Mã', 'Yêu cầu chức năng', 'Màn hình đáp ứng', 'Trạng thái giao diện'], [
    ['FR01', 'Đăng ký, xác minh email bằng mã 6 số, đăng nhập, quên mật khẩu', 'Đăng nhập, Tạo tài khoản, Xác minh email, Quên mật khẩu', 'Đã triển khai'],
    ['FR02', 'Tạo nhóm, thêm/xoá thành viên theo username, rời nhóm', 'Thiết lập nhóm, Quản lý nhóm', 'Đã triển khai (phụ thuộc username)'],
    ['FR03', 'Tạo danh sách đi chợ, phân công, thêm món, đánh dấu đã mua', 'Đi chợ, Chi tiết danh sách', 'Đã triển khai'],
    ['FR04', 'Quản lý kho thực phẩm (tên, danh mục, đơn vị, ảnh)', 'Kho thực phẩm', 'Đã triển khai'],
    ['FR05', 'Quản lý thực phẩm trong tủ lạnh, hạn sử dụng, vị trí', 'Tủ lạnh', 'Đã triển khai; chưa lọc theo danh mục'],
    ['FR06', 'Nhắc thực phẩm sắp hết hạn (trước 3 ngày)', 'Trang chủ, Tủ lạnh, thông báo đẩy', 'Đã triển khai; push chưa kiểm chứng trên thiết bị'],
    ['FR07', 'Lập kế hoạch bữa ăn sáng/trưa/tối theo ngày', 'Bữa ăn', 'Đã triển khai (7 ngày tới)'],
    ['FR08', 'Gợi ý món ăn từ nguyên liệu trong tủ', 'Bữa ăn (bottom sheet)', 'Đã triển khai'],
    ['FR09', 'Quản lý công thức nấu ăn (nguyên liệu, cách làm)', 'Công thức, Chi tiết công thức', 'Đã triển khai'],
    ['FR10', 'Báo cáo mua sắm, tiêu thụ, lãng phí, tủ lạnh', 'Báo cáo', 'Đã triển khai'],
    ['FR11', 'Quản lý hồ sơ cá nhân', 'Cá nhân, Đổi mật khẩu', 'Một phần: chỉ đổi ảnh và mật khẩu'],
    ['FR12', 'Quản trị danh mục, đơn vị, người dùng, nhật ký', 'Danh mục & đơn vị', 'Một phần: chưa có Web Admin'],
], [1.3, 6.0, 4.6, 4.1], 'Yêu cầu chức năng và mức độ đáp ứng trên giao diện')
H('2.5. Yêu cầu phi chức năng', 2)
T(['Nhóm', 'Yêu cầu', 'Cách mã nguồn đáp ứng'], [
    ['Ngôn ngữ', 'Giao diện tiếng Việt đầy đủ dấu', 'Toàn bộ chuỗi tiếng Việt; font Be Vietnam Pro; ngày định dạng `dddd, DD/MM` locale vi; thông điệp lỗi tiếng Việt từ backend'],
    ['Hiệu năng cảm nhận', 'Phản hồi nhanh khi thao tác', 'TanStack Query cache 30 s; cập nhật lạc quan khi tick món; tải lười dữ liệu kho chỉ khi mở form'],
    ['Liên tục phiên', 'Không bị đăng xuất đột ngột', 'Interceptor tự làm mới token khi gặp mã `00011`/`00012` rồi phát lại request'],
    ['Bảo mật', 'Bảo vệ token và phân quyền', 'Token lưu trong SecureStore; ẩn nút theo quyền; đổi mật khẩu đăng xuất mọi phiên'],
    ['Khả dụng', 'Dễ dùng một tay, nút đủ lớn', 'Nút cao ≥ 52 pt, ô nhập ≥ 58 pt, tab bar dưới đáy; kéo để làm mới'],
    ['Khả năng tiếp cận', 'Hỗ trợ trình đọc màn hình', '`accessibilityRole/State/Label` cho nút, checkbox, tab, ô nhập; `accessibilityLiveRegion` cho thông báo'],
    ['Nền tảng', 'Android và iOS, hướng dọc', '`orientation: portrait`; `supportsTablet: false`; chỉ giao diện sáng'],
], [3.0, 4.4, 8.6], 'Yêu cầu phi chức năng')

# ================= CHƯƠNG 3 =================
H('CHƯƠNG 3. PHÂN TÍCH CẤU TRÚC GIAO DIỆN', 1)
H('3.1. Information Architecture', 2)
P('Kiến trúc thông tin được dựng từ cây thư mục route `mobile/src/app` (Expo Router) và các lời gọi `router.push`, `router.navigate` trong từng màn hình. Ứng dụng chia thành hai vùng: vùng **(auth)** cho người chưa đăng nhập và vùng **(tabs)** với năm tab chính. Các màn hình chi tiết (chi tiết danh sách, kho thực phẩm, công thức, báo cáo, nhóm, danh mục, đổi mật khẩu) nằm trên Stack gốc nên khi mở, thanh tab được ẩn để dành toàn bộ không gian cho nội dung.')
FIG(DG / 'ia_sitemap.png', 16, 'Information Architecture của ứng dụng di động (dựng từ mã nguồn)')
P('Năm tab chính và các chức năng trực thuộc được xác định như sau:')
T(['Tab', 'File', 'Chức năng chính', 'Màn hình con / thành phần trực thuộc'], [
    ['Trang chủ', '`(tabs)/index.tsx`', 'Dashboard tổng hợp trong ngày', 'Lối tắt tới Tủ lạnh, Đi chợ, Bữa ăn, Công thức, Báo cáo; avatar → Cá nhân; Thiết lập nhóm khi chưa có nhóm'],
    ['Đi chợ', '`(tabs)/shopping.tsx`', 'Danh sách mua sắm của nhóm', 'Modal tạo/sửa danh sách; Chi tiết danh sách `shopping/[listId]` với modal thêm/sửa món'],
    ['Tủ lạnh', '`(tabs)/fridge.tsx`', 'Thực phẩm trong tủ và hạn dùng', 'Modal thêm/sửa món trong tủ; Kho thực phẩm `food.tsx`'],
    ['Bữa ăn', '`(tabs)/meal.tsx`', 'Kế hoạch bữa ăn 7 ngày', 'Modal thêm/sửa món; bottom sheet Gợi ý món; Công thức và Chi tiết công thức'],
    ['Cá nhân', '`(tabs)/profile.tsx`', 'Tài khoản, nhóm, cài đặt', 'Quản lý nhóm, Thiết lập nhóm, Đổi mật khẩu, Báo cáo, Danh mục & đơn vị, Đăng xuất'],
], [2.2, 3.4, 3.9, 6.5], 'Năm tab chính và chức năng trực thuộc')
H('3.2. Sitemap và Screen Inventory', 2)
P('Bảng dưới đây liệt kê toàn bộ màn hình có giao diện được tìm thấy trong mã nguồn. Ngoài 17 màn hình này, thư mục route còn có 4 file layout/chuyển hướng và một file `src/app/index.tsx` là mẫu còn sót lại của công cụ khởi tạo dự án (hiển thị dòng chữ “Edit src/app/index.tsx to edit this screen.”); file này không được người dùng nhìn thấy vì bộ điều hướng gốc chuyển hướng trước. Danh sách đầy đủ kèm thành phần UI chi tiết nằm trong file `analysis/screen_inventory.md`.')
T(['STT', 'Module', 'Màn hình', 'File (mobile/src/app)', 'Trạng thái'], [
    ['1', 'Xác thực', 'Đăng nhập', '(auth)/login.tsx', 'Đã triển khai'],
    ['2', 'Xác thực', 'Tạo tài khoản', '(auth)/register.tsx', 'Đã triển khai'],
    ['3', 'Xác thực', 'Xác minh email', '(auth)/verify-email.tsx', 'Đã triển khai'],
    ['4', 'Xác thực', 'Quên mật khẩu', '(auth)/forgot-password.tsx', 'Đã triển khai'],
    ['5', 'Trang chủ', 'Trang chủ (dashboard)', '(tabs)/index.tsx', 'Đã triển khai'],
    ['6', 'Đi chợ', 'Đi chợ', '(tabs)/shopping.tsx', 'Đã triển khai'],
    ['7', 'Đi chợ', 'Chi tiết danh sách', 'shopping/[listId].tsx', 'Đã triển khai'],
    ['8', 'Tủ lạnh', 'Tủ lạnh', '(tabs)/fridge.tsx', 'Đã triển khai (chưa lọc danh mục)'],
    ['9', 'Tủ lạnh', 'Kho thực phẩm', 'food.tsx', 'Đã triển khai'],
    ['10', 'Bữa ăn', 'Bữa ăn + Gợi ý món', '(tabs)/meal.tsx', 'Đã triển khai'],
    ['11', 'Bữa ăn', 'Công thức', 'recipes.tsx', 'Đã triển khai'],
    ['12', 'Bữa ăn', 'Chi tiết công thức', 'recipes/[recipeId].tsx', 'Đã triển khai'],
    ['13', 'Cá nhân', 'Cá nhân', '(tabs)/profile.tsx', 'Một phần (không sửa hồ sơ)'],
    ['14', 'Cá nhân', 'Thiết lập nhóm', 'group/setup.tsx', 'Đã triển khai'],
    ['15', 'Cá nhân', 'Quản lý nhóm', 'group/manage.tsx', 'Đã triển khai'],
    ['16', 'Cá nhân', 'Đổi mật khẩu', 'change-password.tsx', 'Đã triển khai'],
    ['17', 'Báo cáo', 'Báo cáo', 'reports.tsx', 'Đã triển khai'],
    ['18', 'Quản trị', 'Danh mục & đơn vị', 'catalog.tsx', 'Đã triển khai'],
    ['—', 'Web Admin', 'Quản trị người dùng, nhật ký', '(không có)', 'Chưa triển khai'],
], [1.1, 2.4, 4.3, 4.8, 3.4], 'Screen Inventory — các màn hình tìm thấy trong mã nguồn')
P('Ghi chú: màn Bữa ăn và bottom sheet Gợi ý món nằm trong cùng một file nên được tính là một màn hình; tổng số màn hình nghiệp vụ là 17 (STT 1–18, trong đó STT 10 gộp hai trạng thái hiển thị).', indent=False)
H('3.3. Cấu trúc điều hướng (Navigation)', 2)
P('Root layout (`src/app/_layout.tsx`) đảm nhiệm bốn việc trước khi hiển thị nội dung: nạp bốn độ đậm của font Be Vietnam Pro, giữ màn hình splash (`#FFE9A9`) cho tới khi nạp xong phiên đăng nhập từ SecureStore, đăng ký thông báo đẩy và làm “người gác cổng” điều hướng. Nếu chưa có token, mọi đường dẫn bị chuyển về `/(auth)/login`; nếu đã có token nhưng đang ở vùng không hợp lệ, người dùng được đưa về `/(tabs)`. Nhờ vậy giao diện không bao giờ hiển thị màn hình cần dữ liệu khi chưa đăng nhập.')
FIG(DG / 'navigation_structure.png', 16, 'Cấu trúc điều hướng: Root Stack, (auth) Stack và Bottom Tabs')
P('Thanh tab dưới đáy dùng biểu tượng dạng viền (outline) khi chưa chọn và dạng đặc (filled) khi được chọn, kết hợp đổi màu từ `textMuted` sang `primaryText`. Hiệu ứng chuyển tab là fade 180 ms; thanh tab tự ẩn khi bàn phím mở. Các màn con dùng nút chữ “← Quay lại” thống nhất ở góc trên bên trái thay vì header hệ thống.')
H('3.4. User Flow', 2)
P('Các luồng sử dụng dưới đây được dựng lại từ các lời gọi điều hướng, kiểm tra hợp lệ và API trong mã nguồn. Ký hiệu màu thống nhất: màn hình (nền kem), modal (xanh nhạt), điểm kiểm tra (vàng), gọi API (xanh lá) và nhánh lỗi hoặc chức năng chưa có (đỏ).')
FIG(DG / 'flow_auth.png', 16, 'User flow đăng ký, xác minh email, đăng nhập và quên mật khẩu')
FIG(DG / 'flow_core.png', 16, 'User flow vòng nghiệp vụ chính: Đi chợ → Tủ lạnh → Bữa ăn → Báo cáo')
FIG(DG / 'flow_group.png', 16, 'User flow quản lý nhóm gia đình')
T(['Luồng', 'Trạng thái', 'Nhận xét từ mã nguồn'], [
    ['Đăng ký và đăng nhập', 'Đầy đủ', 'Có xác minh email, gửi lại mã có đếm ngược, liên kết xác minh khi đăng nhập tài khoản chưa xác minh'],
    ['Quản lý nhóm gia đình', 'Một phần', 'Tài khoản đăng ký mới không có username và không có màn sửa hồ sơ nên không thể được trưởng nhóm thêm vào qua app'],
    ['Tạo và quản lý danh sách đi chợ', 'Đầy đủ', 'Chỉ trưởng nhóm; tạo xong tự mở chi tiết và form thêm món'],
    ['Thêm và đánh dấu món đã mua', 'Đầy đủ', 'Cập nhật lạc quan; chưa tự chuyển món đã mua vào tủ lạnh'],
    ['Quản lý thực phẩm trong tủ lạnh', 'Đầy đủ', 'Chưa có lọc/tìm kiếm trong tủ; khi xoá không chọn được lý do “bỏ đi”'],
    ['Theo dõi thực phẩm sắp hết hạn', 'Đầy đủ', 'Badge 3 màu, thống kê, thông báo đẩy 08:00 (chưa kiểm chứng trên thiết bị)'],
    ['Lập kế hoạch bữa ăn', 'Đầy đủ', 'Chỉ 7 ngày kể từ hôm nay; thành viên chỉ xem'],
    ['Gợi ý món ăn', 'Đầy đủ', 'Bottom sheet, hiển thị lý do và nguyên liệu thiếu'],
    ['Quản lý công thức', 'Đầy đủ', 'Nguyên liệu động, cách làm nhập dạng văn bản chuyển thành HTML'],
    ['Xem báo cáo', 'Đầy đủ', 'Khoảng 7/30/90 ngày, 4 nhóm báo cáo, biểu đồ cột tự vẽ'],
], [4.6, 2.2, 9.2], 'Tổng hợp trạng thái các luồng sử dụng')
H('3.5. Mối quan hệ giữa các màn hình', 2)
P('Trang chủ đóng vai trò “trạm trung chuyển”: mỗi thẻ trên dashboard có liên kết tới tab hoặc màn hình tương ứng, nên người dùng có thể đi từ tổng quan tới chi tiết trong một lần chạm. Giữa các module tồn tại một quan hệ phụ thuộc dữ liệu quan trọng: **Kho thực phẩm** là nguồn chung cho danh sách đi chợ, tủ lạnh, bữa ăn và nguyên liệu công thức (các form đều dùng `SelectField` chọn thực phẩm có sẵn trong kho). Khi kho trống, mỗi form hiển thị thông báo hướng dẫn “Kho thực phẩm đang trống. Thêm thực phẩm trước…”. Danh mục và đơn vị (do quản trị viên tạo) lại là điều kiện để tạo thực phẩm.')
T(['Từ màn hình', 'Tới màn hình', 'Cách điều hướng'], [
    ['Trang chủ', 'Tủ lạnh / Đi chợ / Bữa ăn', '`router.navigate` (đổi tab)'],
    ['Trang chủ, Bữa ăn', 'Công thức', '`router.push`'],
    ['Trang chủ, Cá nhân', 'Báo cáo', '`router.push`'],
    ['Đi chợ', 'Chi tiết danh sách', '`router.push` với `listId`; sau khi tạo kèm `openAdd=1`'],
    ['Tủ lạnh', 'Kho thực phẩm', '`router.push`'],
    ['Bữa ăn (gợi ý)', 'Chi tiết công thức; Tủ lạnh', '`router.push` / `router.navigate`'],
    ['Chi tiết công thức', 'Công thức (mở form sửa)', '`router.replace` với `editId`'],
    ['Cá nhân', 'Quản lý nhóm, Thiết lập nhóm, Đổi mật khẩu, Danh mục', '`router.push`'],
    ['Thông báo đẩy hết hạn', 'Tủ lạnh', '`router.navigate` khi `type = EXPIRY_REMINDER`'],
], [4.2, 5.6, 6.2], 'Quan hệ điều hướng giữa các màn hình')

# ================= CHƯƠNG 4 =================
H('CHƯƠNG 4. THIẾT KẾ GIAO DIỆN', 1)
H('4.1. Định hướng UI/UX', 2)
P('Giao diện hướng tới cảm giác **ấm áp, gần gũi của căn bếp gia đình**: nền trắng ngà (`#FFFBF5`), màu chủ đạo cam (`#FF933E`) cho dải tiêu đề của các tab, xanh lam dịu (`#73A5CA`) cho nút hành động và vàng kem cho các điểm nhấn trang trí. Bố cục theo dạng thẻ (card) xếp dọc, mỗi thẻ trả lời một câu hỏi của người dùng (tủ lạnh hôm nay thế nào, còn bao nhiêu món cần mua, hôm nay ăn gì). Ngôn ngữ trên giao diện ngắn gọn, thân thiện và mang tính hướng dẫn, ví dụ “4 món cần dùng sớm để tránh lãng phí.” hay “Kho thực phẩm đang trống. Thêm thực phẩm trước khi lập danh sách.”.')
P('Một số nguyên tắc thiết kế nhất quán được nhận diện từ mã nguồn:')
B(['**Hiển thị theo quyền**: nút tạo, sửa, xoá chỉ xuất hiện với người có quyền; người không có quyền nhận được thông điệp giải thích thay vì nút bị vô hiệu hoá.',
   '**Ba trạng thái dữ liệu thống nhất**: mọi danh sách đều có trạng thái đang tải, rỗng (kèm hành động gợi ý) và lỗi (kèm “Thử lại”).',
   '**Phản hồi tại chỗ**: thông báo thành công/lỗi xuất hiện ngay đầu màn hình, nhãn “Đang xoá...” thay cho nút xoá trong khi xử lý.',
   '**Form trong modal**: tạo và sửa dữ liệu diễn ra trong modal phủ trên màn hình hiện tại để người dùng không mất ngữ cảnh.'])
H('4.2. Design System', 2)
P('Dự án có một bộ **design token** tập trung trong `mobile/src/theme/` (màu ngữ nghĩa, khoảng cách, bo góc, font, cấp chữ) và một bộ **component cơ sở** trong `mobile/src/components/ui/`. Đây là design system ở mức mã nguồn; dự án chưa có tài liệu hướng dẫn sử dụng riêng, chưa có thư viện thiết kế (Figma) hay Storybook. Hình dưới đây tổng hợp các giá trị được trích xuất trực tiếp từ code.')
FIG(DG / 'design_system.png', 16, 'Design system trích xuất từ mã nguồn (token màu, typography, spacing, component)')
H('4.3. Màu sắc và Typography', 2)
P('Bảng màu gốc gồm bốn màu cam `#FF933E`, vàng `#FFCB56`, kem `#FFE9A9` và xanh `#73A5CA`. Điểm đáng chú ý là quy ước trong `colors.ts`: màu `primary` chỉ dùng làm màu nền, còn chữ và biểu tượng màu cam trên nền sáng dùng tông đậm `primaryText` (`#9A3F00`) để đảm bảo độ tương phản. Các trạng thái success/warning/danger/info đều có cặp màu đậm – nhạt dùng cho badge và ô thống kê.')
T(['Cặp màu (chữ / nền)', 'Tỉ lệ tương phản', 'Đánh giá WCAG 2.1'], [
    ['`text` #2A1A0F / `background` #FFFBF5', '16,26 : 1', 'Đạt AAA'],
    ['`textMuted` #7A6656 / `background`', '5,27 : 1', 'Đạt AA'],
    ['`primaryText` #9A3F00 / `surface` #FFFFFF', '6,81 : 1', 'Đạt AA'],
    ['`onAccent` #0E2A3A / `accent` #73A5CA (nút primary)', '5,64 : 1', 'Đạt AA'],
    ['`accentText` #2F6F99 / `surface` (nút outline)', '5,45 : 1', 'Đạt AA'],
    ['StatTile primary / warning / danger / success', '5,80 / 5,36 / 4,92 / 4,56 : 1', 'Đạt AA'],
    ['Chữ trắng / `primary` #FF933E (dải tiêu đề tab)', '2,21 : 1', 'Không đạt (cần ≥ 3 : 1 với chữ lớn)'],
], [7.2, 4.0, 4.8], 'Kiểm tra độ tương phản của các cặp màu chính (tính từ mã màu)')
P('Typography dùng **Be Vietnam Pro**, một họ chữ được thiết kế cho tiếng Việt nên dấu thanh hiển thị cân đối ở mọi cỡ chữ. Hệ thống gồm bảy cấp chữ: display 28/34, title 22/28, heading 18/24, body 16/22, bodyStrong 16/22, caption 13/18 và label 12/16. Ô nhập dùng cỡ 17 để dễ đọc khi gõ; mã xác minh OTP dùng cỡ 24 với khoảng cách ký tự 8 để dễ đối chiếu.')
H('4.4. Layout', 2)
P('Mọi màn hình trong vùng đã đăng nhập dùng component `Screen`: vùng an toàn phía trên, nội dung cuộn dọc với lề ngang 16 pt và lề dưới 32 pt, hỗ trợ kéo để làm mới. Năm tab chính dùng `ScreenHeader` dạng **boxed** — dải màu cam tràn viền chứa tiêu đề và phụ đề — trong khi các màn con dùng tiêu đề chữ đậm trên nền sáng kèm “← Quay lại”, giúp người dùng phân biệt cấp điều hướng. Nội dung được nhóm trong `SectionCard` (nền trắng, viền `#F0DFC8`, bo góc 16, đệm 16), khoảng cách giữa các thẻ 16 pt. Các màn xác thực dùng `AuthLayout` riêng với hai hình tròn trang trí màu kem và xanh nhạt ở hai góc, nội dung giới hạn bề rộng 560 pt.')
T(['Vùng', 'Thông số (từ code)'], [
    ['Lề màn hình', '16 pt (Screen), 24 pt (AuthLayout)'],
    ['Dải tiêu đề tab (boxed)', 'Nền `primary`, đệm 16 × 12, đổ bóng nhẹ, tràn hết bề ngang'],
    ['Thẻ nội dung', 'Bo góc 16, viền 1 px `border`, đệm 16, cách nhau 16'],
    ['Nút', 'Cao tối thiểu 52, bo góc 12; outline viền 1,5 px'],
    ['Ô nhập', 'Cao tối thiểu 58, bo góc 12, nhãn phía trên cỡ 13'],
    ['Thanh tab', 'Cao 60 + vùng an toàn dưới, nhãn cỡ 11, biểu tượng 22'],
    ['Modal', 'Thẻ trắng bo góc 24 giữa màn hình trên lớp phủ `rgba(42,26,15,.45)`'],
], [4.5, 11.5], 'Thông số bố cục chính')
H('4.5. Navigation', 2)
P('Điều hướng hai cấp (tab → màn con) giúp người dùng luôn biết mình đang ở đâu: ở cấp tab có dải tiêu đề màu và thanh tab; ở cấp màn con có nút quay lại và tiêu đề là tên đối tượng đang xem (ví dụ tên danh sách hoặc tên công thức). Một quyết định đáng chú ý là chức năng Công thức và Báo cáo không có tab riêng mà được truy cập từ Trang chủ, Bữa ăn và Cá nhân — giữ thanh tab ở năm mục theo đúng định hướng, đổi lại hai chức năng này cần thêm một lần chạm.')
H('4.6. Thiết kế từng nhóm màn hình', 2)
P('Các hình trong mục này là ảnh chụp ứng dụng đang chạy với dữ liệu mẫu (khung 390 × 844 pt, độ phân giải ×2). Cách thức chụp và giới hạn kiểm chứng được trình bày ở Phụ lục A.')

H('4.6.1. Nhóm màn hình xác thực', 3)
SHOTS([('01_login', 'Đăng nhập'), ('03_register', 'Tạo tài khoản'), ('04_verify_email', 'Xác minh email')], 'Giao diện nhóm màn hình xác thực')
SCREEN([
    ('Mục đích', 'Cho phép người dùng tạo tài khoản, xác minh email và đăng nhập vào ứng dụng; khôi phục mật khẩu khi quên.'),
    ('Thành phần UI', 'AuthLayout (nhãn thương hiệu “ĐI CHỢ TIỆN LỢI”, tiêu đề cỡ 28, hai hình tròn trang trí), AppInput có nhãn, nút “Hiện/Ẩn” mật khẩu, liên kết “Quên mật khẩu?”, AppButton primary, liên kết chân trang.'),
    ('Thao tác', 'Nhập email/mật khẩu; đăng ký với họ tên, email, mật khẩu và nhập lại; nhập mã 6 số; “Gửi lại mã” khả dụng sau 60 giây.'),
    ('Luồng điều hướng', 'Đăng nhập ↔ Tạo tài khoản → Xác minh email → Đăng nhập (kèm thông báo đã xác minh) → Trang chủ. Đăng nhập → Quên mật khẩu (2 bước) → Đăng nhập.'),
    ('Trạng thái giao diện', 'Nút bị làm mờ khi còn trường trống; spinner trong nút khi đang gửi; banner đỏ khi lỗi kiểm tra hoặc lỗi từ máy chủ; banner xanh sau khi xác minh/đặt lại mật khẩu thành công.'),
])

H('4.6.2. Trang chủ', 3)
SHOTS([('10_home', 'Trưởng nhóm có dữ liệu'), ('10_home_full', 'Toàn bộ nội dung cuộn'), ('11_home_no_group', 'Người dùng chưa có nhóm')], 'Giao diện Trang chủ')
SCREEN([
    ('Mục đích', 'Cung cấp bức tranh tổng quan trong ngày và lối tắt tới mọi chức năng.'),
    ('Thành phần UI', 'Dải tiêu đề cam “Xin chào, {tên}” + thứ/ngày + avatar; 5 SectionCard: Tủ lạnh hôm nay (3 StatTile), Danh sách mua sắm (x/y món, % và ProgressBar), Bữa ăn hôm nay (Sáng/Trưa/Tối), Công thức nấu ăn, Báo cáo & thống kê (đã tiêu thụ, tỉ lệ lãng phí).'),
    ('Thao tác', 'Chạm “Xem tất cả”, “Mở danh sách”, “Xem lịch”, “Mở công thức”, “Xem báo cáo”, avatar; kéo xuống để làm mới cả ba nguồn dữ liệu.'),
    ('Luồng điều hướng', 'Tới tab Tủ lạnh, Đi chợ, Bữa ăn, Cá nhân; tới màn Công thức, Báo cáo; tới Thiết lập nhóm khi chưa có nhóm.'),
    ('Trạng thái giao diện', 'Đang tải (“Đang tổng hợp dữ liệu hôm nay...”), chưa có nhóm (EmptyState + “Thiết lập nhóm”), lỗi (ErrorState + “Thử lại”), từng thẻ có thông điệp riêng khi rỗng (“Chưa có món nào trong danh sách đi chợ.”).'),
])

H('4.6.3. Đi chợ', 3)
SHOTS([('20_shopping', 'Danh sách (trưởng nhóm)'), ('22_shopping_detail', 'Chi tiết danh sách'), ('21_shopping_create_modal', 'Modal tạo danh sách')], 'Giao diện chức năng Đi chợ')
SCREEN([
    ('Mục đích', 'Quản lý các danh sách mua sắm của nhóm, phân công người đi chợ và theo dõi tiến độ mua.'),
    ('Thành phần UI', '3 StatTile (Danh sách, Cần mua, Đã mua); ShoppingCard gồm tên, “Giao cho …”, badge x/y (chuyển xanh khi xong), ProgressBar, 4 món đầu kèm checkbox tròn, “Xem thêm n món”, ghi chú, ngày, “Còn n món”; hành động Chi tiết/Sửa/Xoá. Modal tạo: tên, SelectField thành viên, DateField, ghi chú.'),
    ('Thao tác', 'Chạm vòng tròn để đánh dấu đã mua (mọi thành viên); trưởng nhóm tạo/sửa/xoá danh sách và thêm/sửa/xoá món (chọn thực phẩm từ kho, nhập số lượng).'),
    ('Luồng điều hướng', 'Đi chợ → Chi tiết danh sách; sau khi tạo danh sách, ứng dụng tự mở chi tiết và form “Thêm món cần mua”. Xoá danh sách ở màn chi tiết → quay lại.'),
    ('Trạng thái giao diện', 'Món đã mua có dấu tích xanh và chữ gạch ngang; rỗng (“Chưa có danh sách nào” với lời nhắn khác nhau cho trưởng nhóm và thành viên); “Đang xoá...”; thông báo thành công tự ẩn sau 5 giây.'),
])
SHOTS([('23_shopping_add_task_modal', 'Thêm món (SelectField mở)'), ('24_shopping_member', 'Góc nhìn thành viên')], 'Form thêm món và giao diện của thành viên thường (không có nút tạo/sửa/xoá)')

H('4.6.4. Tủ lạnh', 3)
SHOTS([('30_fridge', 'Danh sách trong tủ'), ('31_fridge_add_modal', 'Modal thêm món'), ('32_fridge_datefield', 'Chọn hạn sử dụng')], 'Giao diện tab Tủ lạnh')
SCREEN([
    ('Mục đích', 'Theo dõi thực phẩm đang có trong tủ, số lượng, vị trí và hạn sử dụng.'),
    ('Thành phần UI', '3 StatTile (Tổng, Sắp hết hạn, Đã hết hạn); FridgeRow: Thumbnail (ảnh hoặc chữ cái đầu), tên, badge hạn dùng 3 màu (đỏ “Đã hết hạn”/“Hết hạn hôm nay”, vàng “Còn 1–3 ngày”, xanh “Còn n ngày”), “số lượng đơn vị · vị trí”, “Hạn dùng: DD/MM/YYYY”; hai nút chân trang “Kho thực phẩm” và “Thêm thực phẩm”.'),
    ('Thao tác', 'Thêm món (chọn thực phẩm, số lượng, hạn dùng mặc định +7 ngày qua lịch tháng, vị trí: Ngăn mát/Ngăn đá/Cánh tủ/Ngoài tủ, ghi chú); sửa (không đổi được thực phẩm); xoá có xác nhận “được ghi nhận vào báo cáo”.'),
    ('Luồng điều hướng', 'Tủ lạnh → Kho thực phẩm. Bấm thông báo đẩy “sắp hết hạn” → mở tab Tủ lạnh.'),
    ('Trạng thái giao diện', 'Đang tải (“Đang mở tủ lạnh...”), rỗng (“Tủ lạnh đang trống … nhận nhắc nhở trước 3 ngày”), lỗi; danh sách sắp xếp theo hạn gần nhất (thứ tự từ backend).'),
])

H('4.6.5. Kho thực phẩm', 3)
SHOTS([('35_food', 'Danh sách kho'), ('36_food_filter', 'Lọc theo danh mục'), ('37_food_add_modal', 'Thêm thực phẩm')], 'Giao diện Kho thực phẩm')
SCREEN([
    ('Mục đích', 'Quản lý danh mục thực phẩm riêng của nhóm — nguồn dữ liệu cho tủ lạnh, đi chợ, bữa ăn và công thức.'),
    ('Thành phần UI', 'Ô tìm kiếm (trì hoãn bằng `useDeferredValue`), hàng chip lọc danh mục cuộn ngang (“Tất cả” + danh mục), FoodRow (Thumbnail, tên, “danh mục · đơn vị”), modal với khung ảnh 88 pt, “Chọn ảnh”/“Chụp ảnh”, giới hạn “Tối đa 5MB · JPG, PNG, WEBP, GIF”, SelectField danh mục và đơn vị.'),
    ('Thao tác', 'Tìm và lọc; thêm/sửa thực phẩm kèm ảnh từ thư viện hoặc camera (có xin quyền); xoá có cảnh báo dữ liệu tủ lạnh liên quan cũng bị xoá.'),
    ('Luồng điều hướng', 'Truy cập từ tab Tủ lạnh; quay lại bằng “← Quay lại”.'),
    ('Trạng thái giao diện', 'Sửa/Xoá chỉ hiển thị với người tạo hoặc trưởng nhóm; thông báo khi chưa có danh mục/đơn vị (“Nhờ quản trị viên tạo trước…”); rỗng có nút “Thêm thực phẩm”.'),
])

H('4.6.6. Bữa ăn và gợi ý món', 3)
SHOTS([('40_meal', 'Lịch bữa ăn'), ('41_meal_suggestion', 'Gợi ý món từ tủ lạnh'), ('42_meal_add_modal', 'Thêm món vào bữa')], 'Giao diện tab Bữa ăn')
SCREEN([
    ('Mục đích', 'Lập kế hoạch bữa sáng, trưa, tối cho 7 ngày tới và gợi ý món nấu được từ nguyên liệu trong tủ.'),
    ('Thành phần UI', 'Dải 7 ngày (thứ viết tắt + ngày, hôm nay có viền, ngày chọn nền cam); nút outline “Gợi ý món từ tủ lạnh (n)”; 3 SectionCard Sáng/Trưa/Tối với “Thêm”; bottom sheet có tay nắm, mỗi gợi ý gồm tên, lý do (“Dùng Đậu phụ còn 2 ngày”), “Khớp x/y nguyên liệu · Thiếu …/Đủ nguyên liệu”.'),
    ('Thao tác', 'Chọn ngày; trưởng nhóm thêm/sửa/xoá món theo bữa; mở gợi ý, “Xem công thức”, “Thêm vào bữa ăn” (mở form với bữa trưa và nguyên liệu khớp đầu tiên).'),
    ('Luồng điều hướng', 'Bữa ăn → Chi tiết công thức (từ gợi ý) / Công thức; gợi ý rỗng → “Mở tủ lạnh” hoặc “Xem công thức”.'),
    ('Trạng thái giao diện', 'Bữa chưa có món hiển thị chữ nghiêng “Chưa có món nào cho bữa này.”; thành viên thường không thấy “Thêm/Sửa/Xoá”; bottom sheet có trạng thái tải, lỗi và rỗng riêng.'),
])

H('4.6.7. Công thức nấu ăn', 3)
SHOTS([('50_recipes', 'Danh sách công thức'), ('51_recipe_detail', 'Chi tiết công thức'), ('52_recipe_editor', 'Thêm/sửa công thức')], 'Giao diện chức năng Công thức')
SCREEN([
    ('Mục đích', 'Lưu và chia sẻ cách nấu các món của gia đình kèm nguyên liệu định lượng.'),
    ('Thành phần UI', 'Ô tìm kiếm (theo tên, thực phẩm, mô tả); thẻ công thức (tên, “n nguyên liệu”, mô tả 2 dòng, Xem/Sửa/Xoá); màn chi tiết gồm mô tả, bảng nguyên liệu – định lượng, “Cách làm” hiển thị HTML; form với danh sách nguyên liệu động (SelectField + số lượng, “Thêm nguyên liệu”, “Xoá nguyên liệu”) và ô “Cách làm” mỗi bước một dòng.'),
    ('Thao tác', 'Tìm kiếm; thêm/sửa (kiểm tra: tên ≤ 200, mô tả ≤ 2.000, ít nhất 1 nguyên liệu, không trùng nguyên liệu, số lượng dương); xoá có xác nhận.'),
    ('Luồng điều hướng', 'Truy cập từ Trang chủ hoặc Bữa ăn; Chi tiết → “Sửa công thức” quay về danh sách và tự mở form sửa.'),
    ('Trạng thái giao diện', 'Rỗng (“Chưa có công thức nào”), không tìm thấy (“Thử từ khóa khác.”), công thức thiếu nguyên liệu hiển thị “0 nguyên liệu” (dữ liệu cũ chỉ có `foodId`).'),
])

H('4.6.8. Cá nhân và nhóm gia đình', 3)
SHOTS([('60_profile', 'Cá nhân'), ('61_group_manage', 'Quản lý nhóm (trưởng nhóm)'), ('64_group_setup', 'Thiết lập nhóm')], 'Giao diện Cá nhân và Nhóm gia đình')
SCREEN([
    ('Mục đích', 'Quản lý tài khoản, nhóm gia đình, bảo mật, thông báo và truy cập các chức năng phụ.'),
    ('Thành phần UI', 'Thẻ người dùng (avatar tròn 64 có huy hiệu camera, tên, email, nhãn vai trò hệ thống, “Đổi ảnh đại diện”); thẻ Nhóm gia đình (InfoRow: tên nhóm, vai trò, trưởng nhóm, số thành viên); thẻ Bảo mật & thông báo (trạng thái quyền thông báo, “Bật thông báo”); thẻ Báo cáo; thẻ Dữ liệu dùng chung; nút Đăng xuất. Quản lý nhóm: thông tin nhóm, form thêm thành viên bằng username, danh sách thành viên với badge “Trưởng nhóm”, “Rời nhóm”.'),
    ('Thao tác', 'Đổi ảnh đại diện (thư viện/camera, ≤ 5 MB); đổi mật khẩu; bật thông báo; trưởng nhóm thêm/xoá thành viên; rời nhóm (cảnh báo chuyển quyền); tạo nhóm hoặc “Kiểm tra lại” khi chưa có nhóm.'),
    ('Luồng điều hướng', 'Cá nhân → Quản lý nhóm / Thiết lập nhóm / Đổi mật khẩu / Báo cáo / Danh mục & đơn vị; Đăng xuất → Đăng nhập; Rời nhóm → Thiết lập nhóm.'),
    ('Trạng thái giao diện', 'Chưa có nhóm (thẻ hướng dẫn + “Thiết lập nhóm”); đang tải ảnh (spinner phủ avatar, “Đang tải ảnh...”); thành viên thường thấy dòng “Chỉ trưởng nhóm mới có quyền thêm hoặc xoá thành viên.”'),
])
P('Nhận xét: nhãn “Thành viên” trong thẻ người dùng là vai trò hệ thống (`user.role`), trong khi dòng “Vai trò: Trưởng nhóm” ngay bên dưới là vai trò trong nhóm. Hai khái niệm cùng chữ “vai trò” đặt cạnh nhau có thể gây nhầm lẫn (ảnh “Cá nhân” ở hình trên). Ngoài ra màn Cá nhân không có chức năng sửa họ tên hoặc username dù API `PUT /user` hỗ trợ.')

H('4.6.9. Báo cáo', 3)
SHOTS([('70_reports_shopping', 'Tổng quan + Mua sắm'), ('72_reports_waste', 'Lãng phí'), ('73_reports_fridge', 'Tủ lạnh')], 'Giao diện màn Báo cáo')
SCREEN([
    ('Mục đích', 'Thống kê mua sắm, tiêu thụ và lãng phí trong một khoảng thời gian để gia đình điều chỉnh thói quen.'),
    ('Thành phần UI', 'Chip khoảng thời gian 7/30/90 ngày; thẻ Tổng quan (4 StatTile + câu tóm tắt tủ lạnh); thanh tab dạng chip Mua sắm/Tiêu thụ/Lãng phí/Tủ lạnh; BarChart tự vẽ (cột đôi Cần mua/Đã mua có chú giải); BreakdownCard theo danh mục, người được giao, lý do, vị trí; ProgressBar “Đã tiêu thụ x / y”.'),
    ('Thao tác', 'Đổi khoảng thời gian; đổi tab báo cáo (dữ liệu từng tab chỉ tải khi được chọn); kéo để làm mới.'),
    ('Luồng điều hướng', 'Truy cập từ Trang chủ hoặc Cá nhân.'),
    ('Trạng thái giao diện', 'Đang tổng hợp; chưa có nhóm; lỗi; biểu đồ rỗng (“Chưa có dữ liệu trong khoảng này.”); chú thích công thức “Tỉ lệ lãng phí = số lượng bỏ đi / tổng số lượng đã xử lý”.'),
])
P('Ghi chú về dữ liệu ảnh chụp: dữ liệu mẫu được tạo trong cùng một ngày nên biểu đồ theo ngày chỉ có một cột; tỉ lệ lãng phí 71% là kết quả của dữ liệu thử nghiệm, không phản ánh dữ liệu người dùng thật.')

H('4.6.10. Danh mục và đơn vị (chức năng quản trị trên mobile)', 3)
SHOTS([('80_catalog_user', 'Người dùng thường (chỉ xem)'), ('81_catalog_admin', 'Quản trị viên hệ thống'), ('82_catalog_add_modal', 'Modal thêm danh mục')], 'Giao diện Danh mục & đơn vị theo vai trò')
P('Màn hình dùng segmented control hai lựa chọn “Danh mục (n)” và “Đơn vị (n)”, danh sách có số thứ tự trong vòng tròn. Người dùng thường thấy banner thông tin “Bạn chỉ có thể xem…”, quản trị viên hệ thống có thêm “Thêm”, “Sửa”, “Xoá”. Đây là phần quản trị duy nhất đã có giao diện; các chức năng quản trị người dùng và xem nhật ký mới chỉ tồn tại ở API backend.')

H('4.7. Mô tả các component quan trọng', 2)
T(['Component', 'Đặc điểm thiết kế', 'Phạm vi sử dụng'], [
    ['AppButton', '3 biến thể primary (nền xanh `accent`), outline (viền 1,5 px), ghost; cao ≥ 52; spinner khi loading; mờ 50% khi disabled; `accessibilityState`', '18 màn hình'],
    ['AppInput', 'Nhãn phía trên, viền đổi màu khi focus/lỗi, nút Hiện/Ẩn mật khẩu, cỡ chữ 17', '13 màn hình'],
    ['SelectField', 'Dropdown tự xây mở ngay dưới ô, có ô “Tìm...”, đánh dấu ✓ mục đang chọn — thay picker hệ điều hành để giao diện đồng nhất trên Android/iOS', '6 màn hình'],
    ['DateField', 'Lịch tháng inline, tuần bắt đầu từ Thứ 2, nhãn T2…CN, nút “Hôm nay”', '3 màn hình'],
    ['SectionCard', 'Thẻ nội dung có tiêu đề và hành động phụ bên phải', '13 màn hình'],
    ['StatTile', 'Ô số liệu 5 tông màu ngữ nghĩa', '4 màn hình'],
    ['FormMessage', 'Banner error/success/info; success tự ẩn sau 5 giây; `accessibilityLiveRegion`', '15 màn hình'],
    ['Loading/Empty/ErrorState', 'Ba trạng thái dữ liệu thống nhất có biểu tượng và hành động', '11 màn hình'],
    ['Thumbnail', 'Ảnh thực phẩm/avatar, tự thay bằng chữ cái đầu khi không có ảnh', '6 màn hình'],
    ['BarChart', 'Biểu đồ cột bằng View, cột đôi, cuộn ngang khi > 14 điểm', 'Báo cáo'],
], [3.2, 9.4, 3.4], 'Các component giao diện quan trọng')

# ================= CHƯƠNG 5 =================
H('CHƯƠNG 5. THIẾT KẾ TƯƠNG TÁC', 1)
H('5.1. Luồng thao tác', 2)
P('Các luồng thao tác được thiết kế để giảm số bước ở những tác vụ lặp lại hằng ngày. Ví dụ điển hình: sau khi trưởng nhóm tạo danh sách đi chợ, ứng dụng tự chuyển sang màn chi tiết với tham số `openAdd=1` và mở sẵn form “Thêm món cần mua” vì hai thao tác này luôn đi liền nhau. Việc đánh dấu đã mua có thể thực hiện ngay trên thẻ danh sách ở tab Đi chợ mà không cần mở chi tiết. Từ gợi ý món ăn, người dùng chuyển thẳng sang form thêm vào bữa với thực phẩm đã được điền sẵn.')
H('5.2. Form và validation', 2)
P('Validation được thực hiện hai lớp: kiểm tra phía client trước khi gửi (hàm trong `utils/validation.ts` và điều kiện trong từng màn) và thông điệp lỗi từ backend (Joi) được hiển thị nguyên văn. Nút gửi bị làm mờ khi trường bắt buộc còn trống; lỗi hiển thị bằng `FormMessage` màu đỏ trong form hoặc modal. Các form sửa đều kiểm tra “Chưa có thay đổi nào.” để tránh gửi request không cần thiết.')
SHOTS([('02_login_error', 'Lỗi kiểm tra email'), ('63_change_password', 'Form đổi mật khẩu'), ('05_forgot_password', 'Quên mật khẩu – bước 1')], 'Form và trạng thái validation')
T(['Trường / form', 'Quy tắc kiểm tra phía client', 'Thông điệp'], [
    ['Email', 'Bỏ khoảng trắng, chữ thường, mẫu `x@y.z`', '“Email không hợp lệ.”'],
    ['Mật khẩu', '6–20 ký tự; nhập lại phải khớp', '“Mật khẩu phải từ 6 đến 20 ký tự.”, “Mật khẩu nhập lại không khớp.”'],
    ['Họ tên', '3–30 ký tự', '“Họ tên phải từ 3 đến 30 ký tự.”'],
    ['Mã xác minh', 'Đúng 6 chữ số', '“Mã xác minh phải gồm đúng 6 chữ số.”'],
    ['Đổi mật khẩu', 'Mật khẩu mới khác mật khẩu cũ', '“Mật khẩu mới không được giống mật khẩu hiện tại.”'],
    ['Số lượng', 'Số dương ≤ 1.000.000, chấp nhận dấu phẩy thập phân', '“Số lượng phải là số dương, tối đa 1.000.000.”'],
    ['Tên nhóm / danh mục', '≤ 50 ký tự, không rỗng', '“Tên nhóm tối đa 50 ký tự.”'],
    ['Username thành viên', '3–15 ký tự', '“Username phải từ 3 đến 15 ký tự.”'],
    ['Công thức', 'Tên ≤ 200, mô tả ≤ 2.000, ≥ 1 nguyên liệu, không trùng', '“Mỗi nguyên liệu chỉ được chọn một lần.”'],
    ['Ảnh', '≤ 5 MB; JPG, PNG, WEBP, GIF', '“Ảnh vượt quá 5MB. Vui lòng chọn ảnh nhỏ hơn.”'],
], [3.4, 6.2, 6.4], 'Quy tắc validation trên giao diện')
H('5.3. Trạng thái Loading, Empty, Success và Error', 2)
P('Ứng dụng xây dựng ba component trạng thái dùng chung trong `StateView.tsx` và áp dụng nhất quán cho mọi danh sách. Trạng thái **Loading** gồm spinner màu `primaryText` và câu mô tả theo ngữ cảnh (“Đang mở tủ lạnh...”, “Đang tổng hợp báo cáo...”). Trạng thái **Empty** gồm biểu tượng trong vòng tròn cam nhạt, tiêu đề, mô tả và nút hành động phù hợp vai trò. Trạng thái **Error** dùng biểu tượng mất kết nối, tiêu đề “Không tải được dữ liệu”, thông điệp từ backend hoặc câu mặc định “Không kết nối được máy chủ. Vui lòng thử lại.” và nút “Thử lại”. Trạng thái **Success** được thể hiện bằng banner xanh (ví dụ “Đã thêm "Cà chua" vào tủ lạnh.”) tự ẩn sau 5 giây.')
SHOTS([('90_loading_state', 'Loading'), ('11_home_no_group', 'Empty (chưa có nhóm)'), ('91_error_state', 'Error (mất kết nối)')], 'Ba trạng thái dữ liệu: đang tải, rỗng và lỗi')
P('Để chụp được trạng thái đang tải và lỗi, request API tương ứng đã được giữ lại hoặc huỷ trong trình duyệt kiểm thử; giao diện hiển thị là mã nguồn thật của ứng dụng phản ứng với tình huống mạng đó.', indent=False, italic=True, size=11.5)
H('5.4. Dialog và xác nhận', 2)
P('Mọi thao tác xoá hoặc không thể hoàn tác đều đi qua hộp thoại hệ thống `Alert.alert` với nút “Huỷ” (kiểu cancel) và nút hành động kiểu destructive: xoá danh sách, xoá món, xoá thực phẩm, xoá công thức, xoá thành viên, rời nhóm, xoá danh mục/đơn vị. Nội dung hộp thoại nêu rõ hậu quả, ví dụ “Xoá "Cà chua" khỏi kho? Mục trong tủ lạnh và dữ liệu liên quan cũng sẽ bị xoá.” hoặc cảnh báo chuyển quyền khi trưởng nhóm rời nhóm. Hộp thoại cũng được dùng để chọn nguồn ảnh (Thư viện / Chụp ảnh / Huỷ).')
H('5.5. Notification', 2)
P('Thông báo đẩy được xử lý trong hook `usePushNotifications`: sau khi đăng nhập, ứng dụng xin quyền, tạo kênh Android “Thực phẩm sắp hết hạn” (mức quan trọng cao), lấy Expo push token và gửi lên backend qua `PUT /user/device-token`. Backend chạy cron lúc 08:00 hằng ngày (giờ Việt Nam), gửi nhắc cho các món hết hạn trong 3 ngày tới. Khi người dùng chạm vào thông báo có `type = EXPIRY_REMINDER`, ứng dụng mở tab Tủ lạnh. Màn Cá nhân hiển thị trạng thái quyền (đã bật, chưa cấp quyền, thiết bị không hỗ trợ…) và cho phép bật lại; màn này cố ý không tự bật hộp thoại xin quyền. Chức năng này **chưa được kiểm chứng trên thiết bị thật** trong phạm vi báo cáo.')
H('5.6. Responsive và khả năng tiếp cận', 2)
P('Ứng dụng khoá hướng dọc và không hỗ trợ tablet trên iOS. Bố cục dùng flex nên co giãn theo bề rộng điện thoại; các màn xác thực giới hạn bề rộng 560 pt; dải tiêu đề và thanh tab tôn trọng vùng an toàn (safe area). Về khả năng tiếp cận, mã nguồn có nhiều điểm tích cực: nút khai báo `accessibilityRole="button"` và `accessibilityState` (disabled, busy, selected, expanded); checkbox món đi chợ khai báo `accessibilityRole="checkbox"` kèm trạng thái checked; chip báo cáo dùng vai trò `tab`; ô nhập tự lấy nhãn làm `accessibilityLabel`; thông báo dùng `accessibilityLiveRegion="polite"`; nút và ô nhập có kích thước chạm lớn.')
P('Các điểm cần cải thiện: chữ trắng trên dải tiêu đề cam chỉ đạt tương phản 2,21 : 1; các liên kết hành động dạng chữ (Sửa, Xoá) có vùng chạm nhỏ (chỉ mở rộng bằng `hitSlop` 8); nút “← Quay lại” không khai báo vai trò button; ứng dụng chưa hỗ trợ chế độ tối; chưa kiểm tra với cỡ chữ hệ thống phóng to. Trên bản chạy web dùng để chụp ảnh, nhãn chữ của thanh tab bị cắt do chiều cao thanh tab cố định 60 pt; hiện tượng này cần được kiểm chứng lại trên thiết bị Android/iOS.')

# ================= CHƯƠNG 6 =================
H('CHƯƠNG 6. ĐÁNH GIÁ VÀ KẾT LUẬN', 1)
H('6.1. Đánh giá giao diện', 2)
P('Giao diện đạt mức nhất quán cao nhờ dùng chung bộ token và component: cùng một kiểu thẻ, nút, ô nhập, trạng thái dữ liệu trên mọi màn. Bảng màu ấm phù hợp chủ đề gia đình – bếp núc, màu ngữ nghĩa cho hạn sử dụng (đỏ – vàng – xanh) giúp nhận biết nhanh món cần ưu tiên. Font Be Vietnam Pro hiển thị tiếng Việt rõ ràng. Hạn chế chính về mặt thị giác là độ tương phản của dải tiêu đề tab và việc hai màu chức năng (cam cho tiêu đề, xanh cho nút) cùng mang tính nhấn mạnh khiến thứ bậc thị giác ở một số màn chưa thật rõ.')
H('6.2. Đánh giá trải nghiệm', 2)
T(['Nguyên tắc (Nielsen)', 'Điểm tốt', 'Điểm cần cải thiện'], [
    ['Hiển thị trạng thái hệ thống', 'Loading/Empty/Error thống nhất; tiến độ x/y, %; “Đang xoá...”', 'Không có toast nổi; thông báo nằm đầu trang có thể khuất khi đang cuộn'],
    ['Khớp với thế giới thực', 'Ngôn ngữ đời thường, vị trí “Ngăn mát/Ngăn đá/Cánh tủ”, bữa sáng/trưa/tối', 'Kế hoạch bữa ăn chọn “thực phẩm” thay vì “món ăn/công thức”'],
    ['Kiểm soát và tự do', 'Huỷ trong mọi modal; xác nhận trước khi xoá; quay lại bước 1 khi quên mật khẩu', 'Không có hoàn tác (undo) sau khi xoá'],
    ['Nhất quán và chuẩn mực', 'Component dùng chung, vị trí nút cố định', 'Bốn kiểu “chip chọn” khác nhau; nhãn “vai trò” trùng nghĩa ở màn Cá nhân'],
    ['Phòng ngừa lỗi', 'Validation trước khi gửi, nút mờ khi thiếu dữ liệu, chọn thực phẩm từ danh sách', 'Đánh dấu đã mua không tự cập nhật tủ lạnh — dễ quên nhập'],
    ['Nhận biết hơn ghi nhớ', 'SelectField có tìm kiếm, badge hạn dùng', 'Tủ lạnh chưa có tìm kiếm/lọc khi số món lớn'],
    ['Linh hoạt và hiệu quả', 'Tick món ngay trên thẻ, tự mở form thêm món, lối tắt từ Trang chủ', 'Công thức, Báo cáo không có tab riêng'],
    ['Thẩm mỹ và tối giản', 'Thẻ rõ ràng, khoảng trắng hợp lý', 'Dashboard dài, cần cuộn để thấy thẻ Báo cáo'],
    ['Giúp nhận biết và khắc phục lỗi', 'Thông điệp tiếng Việt cụ thể từ backend, nút “Thử lại”', '—'],
    ['Trợ giúp và hướng dẫn', 'Gợi ý ngữ cảnh khi kho trống, khi chưa có nhóm', 'Không có hướng dẫn lần đầu (onboarding)'],
], [3.8, 6.1, 6.1], 'Đánh giá trải nghiệm theo 10 nguyên tắc khả dụng của Nielsen')
H('6.3. Những hạn chế', 2)
B(['**Thiếu màn sửa hồ sơ**: không đổi được họ tên, username, giới tính, ngày sinh; tài khoản đăng ký mới không có username nên không thể được thêm vào nhóm qua ứng dụng.',
   '**Web Admin chưa triển khai**: quản trị người dùng và nhật ký hệ thống chỉ có API.',
   '**Tủ lạnh chưa có lọc theo danh mục / tìm kiếm** như kế hoạch ban đầu; khi xoá không chọn được lý do “bỏ đi” dù API hỗ trợ.',
   '**Liên kết giữa các module còn rời**: món đã mua không tự chuyển vào tủ lạnh; kế hoạch bữa ăn dùng thực phẩm thay vì công thức; lịch bữa ăn chỉ xem 7 ngày tới.',
   '**Khả năng tiếp cận**: tương phản dải tiêu đề tab thấp, vùng chạm của liên kết chữ nhỏ, chưa có dark mode.',
   '**Kỹ thuật giao diện**: modal form, InfoRow và các kiểu chip được viết lặp lại ở nhiều file; còn file mẫu `src/app/index.tsx`; đăng xuất không gọi API thu hồi refresh token; chưa có kiểm thử giao diện.'])
H('6.4. Hướng phát triển', 2)
T(['Ưu tiên', 'Đề xuất', 'Lý do'], [
    ['Cao', 'Bổ sung màn Sửa hồ sơ (họ tên, username) và gợi ý đặt username ngay sau đăng ký', 'Gỡ chặn luồng tham gia nhóm'],
    ['Cao', 'Đổi chữ trên dải tiêu đề tab sang `onPrimary` hoặc làm đậm nền', 'Đạt chuẩn tương phản WCAG'],
    ['Cao', 'Kiểm tra lại chiều cao thanh tab trên thiết bị thật', 'Tránh nhãn tab bị cắt'],
    ['Trung bình', 'Khi đánh dấu đã mua, đề xuất “Thêm vào tủ lạnh” với số lượng sẵn có', 'Khép kín vòng Đi chợ → Tủ lạnh'],
    ['Trung bình', 'Tìm kiếm và lọc theo danh mục/vị trí trong tủ lạnh; chọn lý do khi lấy món ra', 'Đúng kế hoạch, báo cáo chính xác hơn'],
    ['Trung bình', 'Tách component ModalForm, InfoRow, Chip; thêm Toast', 'Giảm trùng lặp, đồng nhất tương tác'],
    ['Thấp', 'Dark mode (đã chuẩn bị bằng token ngữ nghĩa), onboarding lần đầu', 'Nâng cao trải nghiệm'],
    ['Thấp', 'Khởi tạo Web Admin (React + Vite + Ant Design) cho quản trị người dùng và nhật ký', 'Hoàn thiện phạm vi đề bài'],
], [2.2, 8.6, 5.2], 'Đề xuất hướng phát triển giao diện')
H('6.5. Kết luận', 2)
P('Ứng dụng “Đi chợ tiện lợi” đã triển khai đầy đủ giao diện cho các nghiệp vụ cốt lõi: xác thực, nhóm gia đình, đi chợ, tủ lạnh, kho thực phẩm, bữa ăn, gợi ý món, công thức và báo cáo, với 17 màn hình nghiệp vụ tổ chức quanh năm tab. Giao diện được xây dựng trên một bộ design token và component tự phát triển, nhất quán về màu sắc, chữ, bố cục và cách xử lý trạng thái; nhiều chi tiết tương tác cho thấy sự quan tâm tới trải nghiệm như cập nhật lạc quan, tự mở form tiếp theo, hiển thị theo quyền và thông điệp tiếng Việt rõ ràng. Các hạn chế còn lại tập trung ở phần hồ sơ người dùng, độ tương phản của dải tiêu đề, sự liên thông giữa các module và Web Admin chưa được khởi tạo. Những hướng phát triển đề xuất trong mục 6.4 có thể thực hiện tuần tự mà không cần thay đổi kiến trúc giao diện hiện có.')

# ================= PHỤ LỤC =================
H('PHỤ LỤC', 1)
H('A. Phương pháp và giới hạn kiểm chứng', 2)
B(['Mã nguồn được đọc trực tiếp: 23 file route, 14 file component, 13 file API, hook, store, theme của `mobile/`; routes, models, services, validations của `server/`; tài liệu trong `docs/`.',
   'Ứng dụng được chạy bằng `expo start --web` (react-native-web) từ một bản sao mã nguồn tại commit `335e386`; backend chạy cục bộ với MongoDB in-memory, dữ liệu mẫu tạo bằng script `seed-sample-data.js` của dự án và các lời gọi API thông thường.',
   'Vì `expo-secure-store` và `expo-notifications` không chạy trên web, bản sao dùng để chụp ảnh thay hai module này bằng lớp giả lập tối thiểu (lưu token vào localStorage; thông báo không khả dụng). Mã nguồn sản phẩm không bị chỉnh sửa.',
   'Ảnh được chụp tự động bằng Playwright (Chromium) ở khung 390 × 844, tỉ lệ điểm ảnh ×2. Không có ảnh nào được vẽ lại hay chỉnh sửa nội dung; khung điện thoại trong slide chỉ là viền minh hoạ bao quanh ảnh chụp thật.',
   '**Chưa kiểm chứng**: hiển thị trên thiết bị Android/iOS thật (font, vùng an toàn, chiều cao thanh tab), thông báo đẩy, chọn/chụp ảnh từ camera và thư viện, hộp thoại `Alert.alert` (không hiển thị trên web), hiệu ứng chuyển cảnh, hành vi bàn phím, tải ảnh lên Cloudinary.'])
H('B. Danh sách tài liệu phân tích đi kèm', 2)
T(['File', 'Nội dung'], [
    ['analysis/project_structure.md', 'Cấu trúc repository, dependency, phân quyền, trạng thái Web Admin'],
    ['analysis/screen_inventory.md', 'Danh sách đầy đủ 23 file route, thành phần UI, đối chiếu kế hoạch, API chưa có UI'],
    ['analysis/component_inventory.md', 'Thống kê component dùng chung, điều hướng, form, feedback, modal'],
    ['analysis/user_flows.md', 'Information Architecture và 13 luồng sử dụng'],
    ['analysis/design_system_audit.md', 'Token màu, tương phản, typography, spacing, mức độ trưởng thành'],
    ['assets/screenshots/', '51 ảnh chụp giao diện thực tế (PNG), gồm 11 ảnh toàn trang'],
    ['assets/diagrams/', '7 sơ đồ IA, điều hướng, user flow, design system, kiến trúc'],
], [6.0, 10.0], 'Tài liệu và tài nguyên đi kèm báo cáo')

doc.core_properties.title = 'Báo cáo phân tích và thiết kế giao diện hệ thống Đi chợ tiện lợi'
doc.core_properties.subject = 'IT4788 – Phát triển ứng dụng đa nền tảng'
doc.core_properties.author = 'Nhóm Đi chợ tiện lợi'
doc.save(OUT)
print('saved', OUT)
