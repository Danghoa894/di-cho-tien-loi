import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
A = Path(sys.argv[1]); OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
RED = (192, 32, 52); GOLD = (229, 156, 10)
# 1) Logo chính thức (dọc, chữ xám) — dùng nguyên file image13
Image.open(A / 'image13.png').save(OUT / 'hust_logo_full.png')
# 2) Logo ngang trên footer template (image3) — cắt theo bbox phần không trắng, bỏ đường kẻ đỏ
im3 = Image.open(A / 'image3.png').convert('RGB')
reg = im3.crop((0, 3900, 2300, 4500))
bg = Image.new('RGB', reg.size, (255, 255, 255))
bbox = ImageChops.difference(reg, bg).point(lambda v: 255 if v > 20 else 0).convert('L').getbbox()
logo_h = reg.crop((max(bbox[0] - 10, 0), max(bbox[1] - 10, 0), bbox[2] + 10, bbox[3] + 10))
logo_h.save(OUT / 'hust_logo_horizontal.png'); print('horizontal logo', logo_h.size, bbox)
# 3) Wordmark HUST trắng từ ảnh bìa (image1)
im1 = Image.open(A / 'image1.png').convert('RGB')
c = im1.crop((2400, 1300, 5600, 2700))
mask = c.convert('L').point(lambda v: 255 if v > 200 else 0)
wb = mask.getbbox(); print('wordmark bbox', wb)
wm = c.crop((wb[0] - 30, wb[1] - 30, wb[2] + 30, wb[3] + 30)); wm.save(OUT / 'hust_wordmark_red.png')
# 4) Họa tiết vòng chấm tròn (image2: nền trắng)
im2 = Image.open(A / 'image2.png').convert('RGB')
ring = im2.crop((3000, 0, 8000, 4500))
ring = Image.blend(ring, Image.new('RGB', ring.size, (255, 255, 255)), 0.35)
# 5) Nền trang bìa A4 300dpi: trắng + vòng chấm bên phải + dải đỏ đáy có vạch vàng và wordmark
W, H = 2480, 3508
page = Image.new('RGB', (W, H), (255, 255, 255))
rh = 1060; rw = int(ring.width * rh / ring.height)
r = ring.resize((rw, rh), Image.LANCZOS)
canvas = Image.new('RGB', (W, H), (255, 255, 255)); canvas.paste(r, (W - rw, 0))
page = ImageChops.darker(page, canvas)
band = 300
d = ImageDraw.Draw(page)
d.rectangle((0, H - band, W, H), fill=RED)
d.rectangle((0, H - band - 26, W, H - band - 10), fill=GOLD)
wmh = 170; wmw = int(wm.width * wmh / wm.height)
page.paste(wm.resize((wmw, wmh), Image.LANCZOS), (W - wmw - 300, H - band + (band - wmh) // 2))
page.save(OUT / 'cover_bg_a4.png', dpi=(300, 300))
# 6) Vạch đỏ ngắn trang trí
Image.new('RGB', (600, 24), RED).save(OUT / 'red_rule.png')
print('ok')
