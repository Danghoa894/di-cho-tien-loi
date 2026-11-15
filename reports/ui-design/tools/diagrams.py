"""Sinh sơ đồ PNG từ HTML (Playwright). Nội dung sơ đồ dựng theo source code đã khảo sát."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
import base64
_FD = 'D:/Project/di-cho-tien-loi/mobile/node_modules/@expo-google-fonts/be-vietnam-pro'
def _f(w, n):
    return 'data:font/ttf;base64,' + base64.b64encode(open(f'{_FD}/{w}/BeVietnamPro_{w}.ttf', 'rb').read()).decode()
F4, F6, F7 = _f('400Regular', 0), _f('600SemiBold', 0), _f('700Bold', 0)
BASE_CSS = f"""
@font-face{{font-family:BVP;src:url('{F4}');font-weight:400}}
@font-face{{font-family:BVP;src:url('{F6}');font-weight:600}}
@font-face{{font-family:BVP;src:url('{F7}');font-weight:700}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:BVP;background:#FFFFFF;color:#2A1A0F;padding:28px;display:inline-block}}
h1{{font-size:26px;font-weight:700;margin-bottom:6px}}
.sub{{color:#7A6656;font-size:15px;margin-bottom:22px}}
.box{{border-radius:12px;padding:10px 14px;font-size:15px;border:1.5px solid #F0DFC8;background:#fff}}
.tab{{background:#FF933E;color:#2A1608;font-weight:700;border:none}}
.child{{background:#FFFBF5}}
.modal{{background:#E7F1F8;border-color:#73A5CA}}
.admin{{background:#FFF3D1;border-color:#FFCB56}}
.miss{{background:#FFEBEE;border-color:#C62828;border-style:dashed;color:#C62828}}
.small{{font-size:12.5px;color:#7A6656;font-weight:400}}
.legend{{display:flex;gap:18px;margin-top:20px;font-size:13px;color:#7A6656;align-items:center;flex-wrap:wrap}}
.legend span.sw{{display:inline-block;width:18px;height:14px;border-radius:4px;margin-right:6px;vertical-align:middle;border:1.5px solid #F0DFC8}}
"""


def legend():
    return """<div class="legend"><div><span class="sw" style="background:#FF933E;border:none"></span>Tab chính</div>
<div><span class="sw" style="background:#FFFBF5"></span>Màn hình (Stack)</div>
<div><span class="sw" style="background:#E7F1F8;border-color:#73A5CA"></span>Modal / bottom sheet</div>
<div><span class="sw" style="background:#FFF3D1;border-color:#FFCB56"></span>Chỉ admin hệ thống sửa</div>
<div><span class="sw" style="background:#FFEBEE;border-color:#C62828;border-style:dashed"></span>Chưa triển khai</div></div>"""


IA = f"""<html><head><style>{BASE_CSS}
.root{{display:flex;flex-direction:column;align-items:center}}
.app{{background:#2A1A0F;color:#fff;font-weight:700;border:none;padding:12px 26px;font-size:17px}}
.row{{display:flex;gap:16px;align-items:flex-start;margin-top:26px;width:100%;justify-content:center}}
.col{{display:flex;flex-direction:column;gap:9px;width:236px}}
.col .box{{position:relative}}
.ind{{margin-left:18px}}
.grp{{border:1.5px dashed #C9B49C;border-radius:16px;padding:14px;}}
.grp h3{{font-size:14px;color:#7A6656;font-weight:600;margin-bottom:10px;text-transform:uppercase;letter-spacing:1px}}
</style></head><body>
<h1>Information Architecture — ứng dụng di động</h1><div class="sub">Dựng từ cây route <b>mobile/src/app</b> (Expo Router) và các lời gọi <b>router.push/navigate</b> trong từng màn hình</div>
<div class="root"><div class="box app">Đi chợ tiện lợi</div></div>
<div class="row">
 <div class="grp" style="width:250px"><h3>(auth) · chưa đăng nhập</h3><div class="col" style="width:220px">
  <div class="box child"><b>Đăng nhập</b><div class="small">login.tsx</div></div>
  <div class="box child ind">Tạo tài khoản<div class="small">register.tsx</div></div>
  <div class="box child ind">Xác minh email<div class="small">verify-email.tsx · mã 6 số</div></div>
  <div class="box child ind">Quên mật khẩu<div class="small">forgot-password.tsx · 2 bước</div></div>
 </div></div>
 <div class="grp"><h3>(tabs) · đã đăng nhập — 5 tab</h3>
 <div style="display:flex;gap:12px">
  <div class="col" style="width:178px"><div class="box tab">Trang chủ</div>
   <div class="small" style="padding:0 4px">Dashboard, lối tắt tới mọi module</div>
   <div class="box child">Công thức<div class="small">recipes.tsx</div></div>
   <div class="box child">Báo cáo<div class="small">reports.tsx</div></div>
   <div class="box child">Thiết lập nhóm<div class="small">khi chưa có nhóm</div></div></div>
  <div class="col" style="width:178px"><div class="box tab">Đi chợ</div>
   <div class="box modal">Tạo / sửa danh sách</div>
   <div class="box child">Chi tiết danh sách<div class="small">shopping/[listId].tsx</div></div>
   <div class="box modal ind">Thêm / sửa món</div></div>
  <div class="col" style="width:178px"><div class="box tab">Tủ lạnh</div>
   <div class="box modal">Thêm / sửa món trong tủ</div>
   <div class="box child">Kho thực phẩm<div class="small">food.tsx · tìm, lọc, ảnh</div></div>
   <div class="box modal ind">Thêm / sửa thực phẩm</div>
   <div class="box miss">Lọc tủ theo danh mục</div></div>
  <div class="col" style="width:178px"><div class="box tab">Bữa ăn</div>
   <div class="box child">Lịch 7 ngày × 3 bữa</div>
   <div class="box modal">Thêm / sửa món vào bữa</div>
   <div class="box modal">Gợi ý món từ tủ lạnh</div>
   <div class="box child">Công thức<div class="small">recipes.tsx</div></div>
   <div class="box child ind">Chi tiết công thức<div class="small">recipes/[recipeId].tsx</div></div></div>
  <div class="col" style="width:178px"><div class="box tab">Cá nhân</div>
   <div class="box child">Quản lý nhóm<div class="small">group/manage.tsx</div></div>
   <div class="box child">Thiết lập nhóm<div class="small">group/setup.tsx</div></div>
   <div class="box child">Đổi mật khẩu</div>
   <div class="box child">Báo cáo</div>
   <div class="box admin">Danh mục &amp; đơn vị<div class="small">catalog.tsx</div></div>
   <div class="box miss">Sửa hồ sơ (tên, username…)</div></div>
 </div></div>
 <div class="grp" style="width:200px"><h3>Web admin</h3><div class="col" style="width:170px">
  <div class="box miss">Quản trị người dùng</div><div class="box miss">Nhật ký hệ thống</div><div class="box miss">Danh mục / đơn vị (web)</div>
  <div class="small">Chỉ có API backend (/admin/*); thư mục admin/ chưa khởi tạo</div></div></div>
</div>{legend()}</body></html>"""

NAV = f"""<html><head><style>{BASE_CSS}
.lvl{{display:flex;gap:18px;justify-content:center;margin:14px 0}}
.arrow{{text-align:center;color:#9A3F00;font-size:22px;line-height:1}}
.guard{{background:#2A1A0F;color:#fff;border:none;max-width:780px;margin:0 auto;text-align:center}}
code{{font-size:13px;background:#FFF4E4;padding:1px 5px;border-radius:4px}}
</style></head><body>
<h1>Cấu trúc điều hướng (Navigation)</h1><div class="sub">Root Stack (header ẩn) → nhóm (auth) Stack, (tabs) Bottom Tabs và các màn con cùng cấp — thanh tab ẩn khi mở màn con</div>
<div class="box guard">Root layout <code style="background:#4a3426;color:#fff">src/app/_layout.tsx</code><div style="font-size:13px;opacity:.85;margin-top:4px">Nạp font Be Vietnam Pro · hydrate phiên từ SecureStore · guard: chưa có token → /(auth)/login; có token mà ở ngoài các màn hợp lệ → /(tabs) · đăng ký push</div></div>
<div class="arrow">▼</div>
<div class="lvl">
 <div class="box child" style="width:300px"><b>(auth) Stack</b> · slide_from_right<div class="small">login · register · verify-email · forgot-password</div></div>
 <div class="box tab" style="width:420px;text-align:center">(tabs) Bottom Tabs · fade 180 ms<div style="font-weight:400;font-size:13px;margin-top:4px">Trang chủ · Đi chợ · Tủ lạnh · Bữa ăn · Cá nhân</div></div>
 <div class="box child" style="width:340px"><b>Màn con trên Root Stack</b><div class="small">shopping/[listId] · food · recipes · recipes/[recipeId] · reports · catalog · change-password · group/setup · group/manage</div></div>
</div>
<div class="arrow">▼</div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:12px;max-width:1180px;margin:0 auto">
 <div class="box"><b>Trang chủ</b><div class="small">→ Tủ lạnh, Đi chợ, Bữa ăn (navigate tab) · Công thức, Báo cáo, Thiết lập nhóm (push) · avatar → Cá nhân</div></div>
 <div class="box"><b>Đi chợ</b><div class="small">→ Chi tiết danh sách (push) · tạo xong tự mở chi tiết với ?openAdd=1</div></div>
 <div class="box"><b>Tủ lạnh</b><div class="small">→ Kho thực phẩm (push) · thông báo hết hạn mở tab này</div></div>
 <div class="box"><b>Bữa ăn</b><div class="small">→ Công thức, Chi tiết công thức (push) · gợi ý rỗng → Tủ lạnh</div></div>
 <div class="box"><b>Cá nhân</b><div class="small">→ Quản lý / Thiết lập nhóm, Đổi mật khẩu, Báo cáo, Danh mục (push) · Đăng xuất → login</div></div>
</div></body></html>"""


def flow_html(title, sub, steps_rows, note=''):
    rows = ''
    for row in steps_rows:
        cells = ''
        for i, (kind, text, small) in enumerate(row):
            if i:
                cells += '<div class="ar">→</div>'
            cells += f'<div class="box {kind}" style="min-width:150px;max-width:230px"><b>{text}</b><div class="small">{small}</div></div>'
        rows += f'<div class="fr">{cells}</div>'
    return f"""<html><head><style>{BASE_CSS}
.fr{{display:flex;align-items:center;gap:8px;margin:12px 0;flex-wrap:wrap;max-width:1180px;row-gap:10px;padding-bottom:12px;border-bottom:1px dashed #F0DFC8}}
.ar{{color:#9A3F00;font-size:24px;font-weight:700}}
.dec{{background:#FFF3D1;border-color:#FFCB56}}
.api{{background:#E8F5E9;border-color:#2E7D32}}
.err{{background:#FFEBEE;border-color:#C62828}}
.lbl{{font-size:13px;color:#7A6656;margin:14px 0 2px;font-weight:600;text-transform:uppercase;letter-spacing:1px}}
</style></head><body><h1>{title}</h1><div class="sub">{sub}</div>{rows}
<div class="legend"><div><span class="sw" style="background:#FFFBF5"></span>Màn hình</div><div><span class="sw" style="background:#E7F1F8;border-color:#73A5CA"></span>Modal / sheet</div>
<div><span class="sw" style="background:#FFF3D1;border-color:#FFCB56"></span>Kiểm tra / quyết định</div><div><span class="sw" style="background:#E8F5E9;border-color:#2E7D32"></span>Gọi API</div><div><span class="sw" style="background:#FFEBEE;border-color:#C62828"></span>Nhánh lỗi / chưa có</div></div>
{note}</body></html>"""


FLOW_AUTH = flow_html('User flow — Đăng ký, xác minh và đăng nhập', 'Theo register.tsx → verify-email.tsx → login.tsx, forgot-password.tsx và interceptor api/client.ts', [
    [('child', 'Đăng nhập', '"Đăng ký ngay"'), ('child', 'Tạo tài khoản', 'họ tên, email, mật khẩu ×2'), ('dec', 'Kiểm tra cục bộ', 'tên 3–30 · email · 6–20 ký tự · khớp'), ('api', 'POST /user', 'gửi mã 6 số qua email'), ('child', 'Xác minh email', 'nhập mã · gửi lại (60 s)'), ('api', 'POST /user/verify-email', ''), ('child', 'Đăng nhập', 'banner "Email đã được xác minh"')],
    [('child', 'Đăng nhập', 'email + mật khẩu'), ('api', 'POST /user/login', ''), ('dec', 'Kết quả', ''), ('child', '/(tabs) Trang chủ', 'lưu token vào SecureStore')],
    [('err', 'Lỗi 00044', 'chưa xác minh'), ('child', '"Xác minh email ngay →"', 'mở verify-email'), ('err', 'Lỗi khác', 'FormMessage đỏ, giữ dữ liệu form')],
    [('child', 'Quên mật khẩu', 'bước 1: email'), ('api', 'POST /user/forgot-password', 'nhận resetToken'), ('child', 'Bước 2', 'mã + mật khẩu mới ×2'), ('api', 'POST /user/reset-password', ''), ('child', 'Đăng nhập', 'banner "Mật khẩu đã được đặt lại"')],
    [('api', 'Request hết hạn token', 'mã 00011 / 00012'), ('api', 'POST /user/refresh-token', 'tự động, 1 lần'), ('dec', 'Thành công?', ''), ('child', 'Phát lại request', 'người dùng không bị đăng xuất')],
])

FLOW_CORE = flow_html('User flow — Vòng nghiệp vụ chính: Đi chợ → Tủ lạnh → Bữa ăn', 'Theo shopping.tsx, shopping/[listId].tsx, fridge.tsx, meal.tsx, recipes*.tsx — phân quyền lấy từ services backend', [
    [('child', 'Kho thực phẩm', 'tạo thực phẩm: tên, danh mục, đơn vị, ảnh'), ('dec', 'Trưởng nhóm?', 'group.adminId'), ('modal', 'Tạo danh sách', 'tên, giao cho, ngày, ghi chú'), ('api', 'POST /shopping', ''), ('child', 'Chi tiết danh sách', 'tự mở "Thêm món cần mua"'), ('modal', 'Thêm món', 'thực phẩm từ kho + số lượng')],
    [('child', 'Đi chợ / Chi tiết', 'mọi thành viên'), ('child', 'Chạm vòng tròn', 'đánh dấu đã mua'), ('api', 'PATCH …/complete', 'cập nhật lạc quan, rollback khi lỗi'), ('child', 'Tiến độ cập nhật', 'badge x/y, progress, Trang chủ'), ('err', 'Tự chuyển vào tủ', 'chưa có — thêm tay')],
    [('child', 'Tủ lạnh', '"Thêm thực phẩm"'), ('modal', 'Thêm món vào tủ', 'số lượng, hạn (+7 ngày), vị trí, ghi chú'), ('api', 'POST /fridge', ''), ('child', 'Badge hạn dùng', 'đỏ ≤ 0 · vàng ≤ 3 · xanh > 3 ngày'), ('api', 'Cron 08:00 + Expo Push', 'nhắc trước 3 ngày → mở tab Tủ lạnh')],
    [('child', 'Bữa ăn', 'chọn ngày trong 7 ngày'), ('modal', 'Gợi ý món từ tủ lạnh', 'GET /meal/suggestion · ưu tiên món sắp hết hạn'), ('dec', 'Chọn', ''), ('child', 'Chi tiết công thức', 'nguyên liệu + cách làm HTML'), ('modal', 'Thêm vào bữa ăn', 'trưởng nhóm · bữa trưa mặc định')],
    [('child', 'Tủ lạnh: Xoá món', 'Alert xác nhận'), ('api', 'DELETE /fridge/:id', 'backend ghi consumed / expired'), ('child', 'Báo cáo', 'Tiêu thụ · Lãng phí · tỉ lệ lãng phí')],
])

FLOW_GROUP = flow_html('User flow — Nhóm gia đình', 'Theo group/setup.tsx, group/manage.tsx, profile.tsx và group.service.js', [
    [('child', 'Đăng nhập lần đầu', 'groupId = null'), ('child', 'Trang chủ', 'EmptyState "Bạn chưa tham gia nhóm"'), ('child', 'Thiết lập nhóm', 'hiển thị @username'), ('modal', 'Tạo nhóm', 'tên ≤ 50 ký tự'), ('api', 'POST /user/group', 'trở thành trưởng nhóm'), ('child', '/(tabs)', 'dữ liệu nhóm')],
    [('child', 'Thiết lập nhóm', 'gửi username cho trưởng nhóm'), ('child', 'Trưởng nhóm: Quản lý nhóm', 'nhập username 3–15'), ('api', 'POST /user/group/add', ''), ('child', 'Thành viên: "Kiểm tra lại"', 'GET /user → có groupId'), ('child', '/(tabs)', '')],
    [('err', 'Tài khoản đăng ký mới', 'không có username'), ('err', 'Không có màn sửa hồ sơ', 'PUT /user có nhưng UI chưa dùng'), ('err', 'Không thể được thêm vào nhóm', 'chỉ tự tạo nhóm được')],
    [('child', 'Quản lý nhóm', 'mọi thành viên'), ('modal', 'Alert "Rời nhóm"', 'cảnh báo chuyển quyền nếu là trưởng nhóm'), ('api', 'POST /user/group/leave', ''), ('child', 'Thiết lập nhóm', '')],
])


def ds_html():
    sw = lambda n, v, t='#2A1A0F': f'<div class="sw2"><div class="chip" style="background:{v};color:{t}">{v}</div><div class="nm">{n}</div></div>'
    cols = [('primary', '#FF933E'), ('primaryText', '#9A3F00', '#fff'), ('primarySoft', '#FFE9D6'), ('secondary', '#FFCB56'), ('highlight', '#FFE9A9'),
            ('accent', '#73A5CA'), ('accentText', '#2F6F99', '#fff'), ('onAccent', '#0E2A3A', '#fff'), ('background', '#FFFBF5'), ('surface', '#FFFFFF'),
            ('border', '#F0DFC8'), ('text', '#2A1A0F', '#fff'), ('textMuted', '#7A6656', '#fff'), ('success', '#2E7D32', '#fff'), ('warning', '#8A5A00', '#fff'),
            ('danger', '#C62828', '#fff'), ('info', '#2F6F99', '#fff'), ('successSoft', '#E8F5E9'), ('warningSoft', '#FFF3D1'), ('dangerSoft', '#FFEBEE')]
    swatches = ''.join(sw(*c) for c in cols)
    typo = [('display', 28, 34, 700, 'Đăng nhập'), ('title', 22, 28, 700, 'Tủ lạnh hôm nay'), ('heading', 18, 24, 600, 'Danh sách mua sắm'),
            ('body', 16, 22, 400, 'Còn 5 món cần mua trong 2 danh sách.'), ('bodyStrong', 16, 22, 600, 'Thêm thực phẩm'),
            ('caption', 13, 18, 400, 'Hạn dùng: 09/11/2026'), ('label', 12, 16, 600, 'SẮP HẾT HẠN')]
    trows = ''.join(f'<tr><td class="tk">{n}</td><td class="tk">{s}/{l} · {w}</td><td style="font-size:{s}px;line-height:{l}px;font-weight:{w}">{ex}</td></tr>' for n, s, l, w, ex in typo)
    sp = ''.join(f'<div style="display:flex;align-items:center;gap:10px;margin:5px 0"><div class="tk" style="width:44px">{n}</div><div style="height:14px;width:{v*4}px;background:#FF933E;border-radius:3px"></div><div class="tk">{v}px</div></div>' for n, v in [('xs', 4), ('sm', 8), ('md', 12), ('lg', 16), ('xl', 24), ('xxl', 32)])
    rd = ''.join(f'<div style="text-align:center"><div style="width:64px;height:64px;border:2px solid #73A5CA;background:#E7F1F8;border-radius:{v}px"></div><div class="tk">{n} {v if v < 999 else "∞"}</div></div>' for n, v in [('sm', 8), ('md', 12), ('lg', 16), ('xl', 24), ('pill', 999)])
    return f"""<html><head><style>{BASE_CSS}
.grid{{display:grid;grid-template-columns:1.25fr 1fr;gap:26px}}
.card{{border:1.5px solid #F0DFC8;border-radius:16px;padding:18px}}
.card h2{{font-size:18px;font-weight:600;margin-bottom:12px}}
.sws{{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}}
.chip{{height:54px;border-radius:12px;border:1px solid #F0DFC8;display:flex;align-items:flex-end;padding:6px;font-size:11px}}
.nm{{font-size:12px;margin-top:4px;font-weight:600}}
.tk{{font-size:12px;color:#7A6656}}
table{{border-collapse:collapse;width:100%}} td{{padding:5px 6px;border-bottom:1px solid #F0DFC8;vertical-align:middle}}
.btn{{min-height:52px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:16px;margin:8px 0}}
.inp{{min-height:58px;border-radius:12px;border:1px solid #F0DFC8;display:flex;align-items:center;padding:0 16px;color:#7A6656;font-size:17px;background:#fff}}
.tile{{flex:1;border-radius:12px;padding:12px 8px;text-align:center}}
.tile b{{font-size:22px;display:block}}
.badge{{display:inline-block;border-radius:999px;padding:3px 10px;font-size:12px;font-weight:600;margin-right:6px}}
</style></head><body>
<h1>Design system trích xuất từ mã nguồn</h1><div class="sub">Giá trị lấy nguyên văn từ <b>mobile/src/theme/colors.ts</b>, <b>theme/index.ts</b> và các component trong <b>components/ui</b> — font Be Vietnam Pro</div>
<div class="grid"><div>
 <div class="card"><h2>Màu ngữ nghĩa (colors)</h2><div class="sws">{swatches}</div></div>
 <div class="card" style="margin-top:20px"><h2>Typography</h2><table>{trows}</table></div>
</div><div>
 <div class="card"><h2>Spacing &amp; radius</h2><div style="display:flex;gap:30px"><div>{sp}</div><div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">{rd}</div></div></div>
 <div class="card" style="margin-top:20px"><h2>Component cơ sở</h2>
  <div class="tk">AppButton — primary / outline / disabled</div>
  <div class="btn" style="background:#73A5CA;color:#0E2A3A">Thêm thực phẩm</div>
  <div class="btn" style="border:1.5px solid #73A5CA;color:#2F6F99">Kho thực phẩm</div>
  <div class="btn" style="background:#73A5CA;color:#0E2A3A;opacity:.5">Lưu</div>
  <div class="tk" style="margin-top:8px">AppInput</div><div class="inp">Nhập tên thực phẩm...</div>
  <div class="tk" style="margin-top:10px">StatTile — primary / warning / danger / success</div>
  <div style="display:flex;gap:8px;margin-top:6px">
   <div class="tile" style="background:#FFE9D6;color:#9A3F00"><b>9</b>Tổng</div><div class="tile" style="background:#FFF3D1;color:#8A5A00"><b>4</b>Sắp hết hạn</div>
   <div class="tile" style="background:#FFEBEE;color:#C62828"><b>1</b>Đã hết hạn</div><div class="tile" style="background:#E8F5E9;color:#2E7D32"><b>3</b>Đã mua</div></div>
  <div class="tk" style="margin-top:10px">Badge hạn dùng (FridgeRow)</div>
  <div style="margin-top:6px"><span class="badge" style="background:#FFEBEE;color:#C62828">Đã hết hạn</span><span class="badge" style="background:#FFF3D1;color:#8A5A00">Còn 2 ngày</span><span class="badge" style="background:#E8F5E9;color:#2E7D32">Còn 12 ngày</span></div>
 </div>
</div></div></body></html>"""


ARCH = f"""<html><head><style>{BASE_CSS}
.lay{{display:flex;gap:22px;align-items:stretch}}
.layer{{border:1.5px dashed #C9B49C;border-radius:16px;padding:14px;flex:1}}
.layer h3{{font-size:14px;color:#7A6656;margin-bottom:10px;letter-spacing:1px;text-transform:uppercase}}
.layer .box{{margin:7px 0}}
.ar{{align-self:center;font-size:28px;color:#9A3F00}}
</style></head><body><h1>Kiến trúc tổng thể liên quan đến giao diện</h1><div class="sub">Theo package.json, src/api/client.ts, server/src/app.js và docs/01-KE-HOACH-KIEN-TRUC.md</div>
<div class="lay">
 <div class="layer"><h3>Client</h3>
  <div class="box tab">Mobile app — React Native 0.88 + Expo SDK 58 + TypeScript</div>
  <div class="box child">Expo Router (file-based) · 5 tab</div>
  <div class="box child">TanStack Query (cache, refetch, optimistic) · Zustand (phiên)</div>
  <div class="box child">Axios + interceptor refresh token · SecureStore</div>
  <div class="box child">expo-notifications · expo-image-picker · react-native-render-html</div>
  <div class="box miss">Web admin React + Vite + Ant Design — chưa khởi tạo</div></div>
 <div class="ar">⇄</div>
 <div class="layer"><h3>Backend /it4788</h3>
  <div class="box child">Express 5 · routes → middlewares → controllers → services → models</div>
  <div class="box child">Response thống nhất {{ code, message, data }} — message tiếng Việt hiển thị thẳng trên UI</div>
  <div class="box child">Joi validate · JWT · rate limit · audit log</div>
  <div class="box child">Cron 08:00 quét hạn sử dụng (≤ 3 ngày)</div></div>
 <div class="ar">⇄</div>
 <div class="layer" style="flex:.8"><h3>Dịch vụ ngoài</h3>
  <div class="box child">MongoDB Atlas (Mongoose)</div><div class="box child">Cloudinary — ảnh avatar, thực phẩm</div>
  <div class="box child">Gmail SMTP — mã xác minh, đặt lại mật khẩu</div><div class="box child">Expo Push Service → thiết bị</div></div>
</div></body></html>"""

PAGES = {'ia_sitemap': (IA, 1500), 'navigation_structure': (NAV, 1300), 'flow_auth': (FLOW_AUTH, 1300),
         'flow_core': (FLOW_CORE, 1300), 'flow_group': (FLOW_GROUP, 1300), 'design_system': (ds_html(), 1500), 'architecture': (ARCH, 1400)}

with sync_playwright() as p:
    b = p.chromium.launch()
    for name, (html, width) in PAGES.items():
        pg = b.new_page(viewport={'width': width, 'height': 600}, device_scale_factor=2)
        pg.set_content(html); pg.wait_for_timeout(600)
        pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(300)
        pg.locator('body').screenshot(path=str(OUT / f'{name}.png'))
        print('saved', name, pg.evaluate('document.body.scrollWidth'), width)
        pg.close()
    b.close()
