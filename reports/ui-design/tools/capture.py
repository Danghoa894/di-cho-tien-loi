"""Chụp ảnh giao diện thật của app (Expo web build từ source) bằng Playwright.
Ảnh lưu vào reports/ui-design/assets/screenshots/. Không chỉnh sửa ảnh, không mockup."""
import json, sys, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

APP = 'http://localhost:8095'
API = 'http://localhost:5050/it4788'
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
ONLY = set(sys.argv[2:])


def api(method, url, token=None, body=None):
    req = urllib.request.Request(API + url, method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Content-Type': 'application/json',
                                          **({'Authorization': f'Bearer {token}'} if token else {})})
    try:
        with urllib.request.urlopen(req) as r:
            return json.load(r)['data']
    except urllib.error.HTTPError as e:
        print('API error', url, e.read()[:200])
        return None


def session(email, pw='Matkhau@123'):
    return api('POST', '/user/login', body={'email': email, 'password': pw})


def want(name):
    return not ONLY or any(name.startswith(o) for o in ONLY)


def shot(page, name, wait=1.2, full_height=None):
    if not want(name):
        return
    time.sleep(wait)
    page.evaluate("() => document.activeElement && document.activeElement.blur && document.activeElement.blur()")
    if full_height:
        extra = page.evaluate("""() => { let m = 0; for (const e of document.querySelectorAll('div')) {
            const cs = getComputedStyle(e); if ((cs.overflowY === 'auto' || cs.overflowY === 'scroll') && e.clientHeight > 300)
              m = Math.max(m, e.scrollHeight - e.clientHeight); } return m; }""")
        page.set_viewport_size({'width': 390, 'height': min(844 + int(extra) + 4, 4000)})
        time.sleep(0.8)
    for attempt in range(6):
        try:
            page.get_by_text('Bundling', exact=False).first.wait_for(state='detached', timeout=30000)
        except Exception:
            pass
        page.screenshot(path=str(OUT / f'{name}.png'))
        from PIL import Image, ImageStat
        im = Image.open(OUT / f'{name}.png').convert('L').crop((0, 0, 780, 1200))
        if ImageStat.Stat(im).stddev[0] > 12:
            break
        print('  blank, retry', name); time.sleep(2.5)
    if full_height:
        page.set_viewport_size({'width': 390, 'height': 844})
        time.sleep(0.4)
    print('saved', name)


def login_ctx(browser, sess):
    ctx = browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2,
                              locale='vi-VN', timezone_id='Asia/Ho_Chi_Minh', color_scheme='light')
    if sess:
        ctx.add_init_script(
            "localStorage.setItem('accessToken', %s);localStorage.setItem('refreshToken', %s);localStorage.setItem('user', %s);"
            % (json.dumps(sess['accessToken']), json.dumps(sess['refreshToken']), json.dumps(json.dumps(sess['user']))))
    return ctx


def go(page, path, wait_text=None):
    page.goto(APP + path)
    if wait_text:
        page.get_by_text(wait_text, exact=False).first.wait_for(timeout=60000)
    time.sleep(1.0)


def click(page, text, exact=True, nth=0):
    page.get_by_text(text, exact=exact).nth(nth).click()


with sync_playwright() as p:
    browser = p.chromium.launch()

    # ---------- Chưa đăng nhập ----------
    ctx = login_ctx(browser, None); page = ctx.new_page()
    go(page, '/login', 'Đăng nhập'); shot(page, '01_login')
    page.get_by_placeholder('ban@example.com').fill('an.nguyen@')
    page.get_by_placeholder('Tối thiểu 6 ký tự').fill('123')
    page.get_by_role('button', name='Đăng nhập').click(); shot(page, '02_login_error', 0.8)
    go(page, '/register', 'Tạo tài khoản'); shot(page, '03_register')
    go(page, '/verify-email?email=cuong.le%40example.com&token=demo', 'Xác minh email'); shot(page, '04_verify_email')
    go(page, '/forgot-password', 'Quên mật khẩu'); shot(page, '05_forgot_password')
    ctx.close()

    an = session('an.nguyen@example.com')
    tok = an['accessToken']
    lists = api('GET', '/shopping', tok) or []
    recipes = api('GET', '/recipe', tok) or []

    # ---------- Trưởng nhóm (An) ----------
    ctx = login_ctx(browser, an); page = ctx.new_page()
    go(page, '/', 'Tủ lạnh hôm nay'); shot(page, '10_home')
    shot(page, '10_home_full', full_height=1700)

    go(page, '/shopping', 'Đi chợ cuối tuần'); shot(page, '20_shopping')
    shot(page, '20_shopping_full', full_height=1500)
    if want('21'):
        click(page, 'Tạo danh sách mua sắm'); time.sleep(0.6)
        page.get_by_placeholder('Ví dụ: Đi chợ cuối tuần').fill('Mua đồ ăn sáng')
        shot(page, '21_shopping_create_modal')
        click(page, 'Nguyễn Văn An (@annguyen)'); shot(page, '21b_shopping_select_member', 0.6)
    if lists:
        go(page, f"/shopping/{lists[0]['id']}", 'Các món cần mua'); shot(page, '22_shopping_detail')
        shot(page, '22_shopping_detail_full', full_height=1300)
        if want('23'):
            click(page, 'Thêm món'); time.sleep(0.6)
            click(page, 'Chọn thực phẩm'); shot(page, '23_shopping_add_task_modal', 1.2)

    go(page, '/fridge', 'Danh sách thực phẩm'); shot(page, '30_fridge')
    shot(page, '30_fridge_full', full_height=1500)
    if want('31'):
        click(page, 'Thêm thực phẩm'); time.sleep(0.8)
        shot(page, '31_fridge_add_modal')
    if want('32'):
        go(page, '/fridge', 'Danh sách thực phẩm')
        click(page, 'Thêm thực phẩm'); time.sleep(0.8)
        # mở lịch chọn ngày (DateField)
        import re
        page.get_by_text(re.compile(r'^\d{2}/\d{2}/\d{4}$')).last.click(); shot(page, '32_fridge_datefield', 0.8)

    go(page, '/food', 'Danh sách thực phẩm'); shot(page, '35_food')
    shot(page, '35_food_full', full_height=1700)
    if want('36'):
        click(page, 'Rau củ'); shot(page, '36_food_filter', 1.2)
        click(page, 'Tất cả'); time.sleep(1)
        page.get_by_role('button', name='Thêm thực phẩm').last.click(); shot(page, '37_food_add_modal', 1.0)

    go(page, '/meal', 'Gợi ý món từ tủ lạnh'); shot(page, '40_meal')
    shot(page, '40_meal_full', full_height=1500)
    if want('41'):
        click(page, 'Gợi ý món từ tủ lạnh', exact=False); shot(page, '41_meal_suggestion', 1.5)
    if want('42'):
        go(page, '/meal', 'Gợi ý món từ tủ lạnh')
        click(page, 'Thêm', nth=0); shot(page, '42_meal_add_modal', 1.0)

    go(page, '/recipes', 'Canh cà chua trứng'); shot(page, '50_recipes')
    if recipes:
        rid = next((r['id'] for r in recipes if r['name'] == 'Canh cà chua trứng'), recipes[0]['id'])
        go(page, f'/recipes/{rid}', 'Cách làm'); shot(page, '51_recipe_detail')
        shot(page, '51_recipe_detail_full', full_height=1200)
    if want('52'):
        go(page, '/recipes', 'Canh cà chua trứng')
        page.get_by_role('button', name='Thêm công thức').last.click(); shot(page, '52_recipe_editor', 1.2)

    go(page, '/profile', 'Nhóm gia đình'); shot(page, '60_profile')
    shot(page, '60_profile_full', full_height=1600)
    go(page, '/group/manage', 'Thành viên'); shot(page, '61_group_manage')
    shot(page, '61_group_manage_full', full_height=1300)
    go(page, '/change-password', 'Đổi mật khẩu'); shot(page, '63_change_password')

    go(page, '/reports', 'Tổng quan'); shot(page, '70_reports_shopping')
    shot(page, '70_reports_shopping_full', full_height=2000)
    for key, label in [('71_reports_consumption', 'Tiêu thụ'), ('72_reports_waste', 'Lãng phí'), ('73_reports_fridge', 'Tủ lạnh')]:
        if want(key):
            go(page, '/reports', 'Tổng quan')
            page.get_by_role('tab', name=label).click(); time.sleep(1.5)
            page.mouse.wheel(0, 520); shot(page, key, 1.0)

    go(page, '/catalog', 'Danh mục'); shot(page, '80_catalog_user')

    # Trạng thái tải / lỗi: chặn hoặc làm chậm request API (UI là code thật)
    if want('90'):
        held = []
        page.route('**/it4788/fridge', lambda r: held.append(r))
        page.goto(APP + '/fridge'); page.get_by_text('Đang mở tủ lạnh...').wait_for(timeout=60000)
        page.screenshot(path=str(OUT / '90_loading_state.png')); print('saved 90_loading_state')
        page.unroute('**/it4788/fridge')
        for r in held:
            try: r.continue_()
            except Exception: pass
    if want('91'):
        page.route('**/it4788/report/overview*', lambda r: r.abort())
        page.goto(APP + '/reports'); page.get_by_text('Không tải được dữ liệu').wait_for(timeout=60000)
        shot(page, '91_error_state', 0.5)
        page.unroute('**/it4788/report/overview*')
    ctx.close()

    # ---------- Thành viên thường (Bình) ----------
    binh = session('binh.tran@example.com')
    ctx = login_ctx(browser, binh); page = ctx.new_page()
    go(page, '/shopping', 'Đi chợ cuối tuần'); shot(page, '24_shopping_member')
    go(page, '/meal', 'Gợi ý món từ tủ lạnh'); shot(page, '43_meal_member')
    go(page, '/group/manage', 'Thành viên'); shot(page, '62_group_manage_member')
    ctx.close()

    # ---------- Admin hệ thống ----------
    adm = session('admin@example.com', 'Admin@123')
    ctx = login_ctx(browser, adm); page = ctx.new_page()
    go(page, '/catalog', 'Danh mục'); shot(page, '81_catalog_admin')
    if want('82'):
        click(page, 'Thêm', nth=0); shot(page, '82_catalog_add_modal', 0.8)
    ctx.close()

    # ---------- Người dùng chưa có nhóm (Cường) ----------
    cuong = session('cuong.le@example.com')
    ctx = login_ctx(browser, cuong); page = ctx.new_page()
    go(page, '/', 'Bạn chưa tham gia nhóm'); shot(page, '11_home_no_group')
    go(page, '/group/setup', 'Tạo nhóm mới'); shot(page, '64_group_setup')
    go(page, '/profile', 'Nhóm gia đình'); shot(page, '65_profile_no_group')
    ctx.close()
    browser.close()
