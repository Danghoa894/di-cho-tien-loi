from PIL import Image, ImageDraw
from pathlib import Path
R=Path("D:/Project/di-cho-tien-loi/reports/ui-design/assets")
out=R/'illustrations'; out.mkdir(exist_ok=True)
def frame(name):
    sc=Image.open(R/'screenshots'/f'{name}.png').convert('RGBA')   # 780x1688
    w,h=sc.size; b=26; W,H=w+2*b,h+2*b
    ss=2  # supersample for smooth corners
    img=Image.new('RGBA',(W*ss,H*ss),(0,0,0,0)); d=ImageDraw.Draw(img)
    d.rounded_rectangle((0,0,W*ss-1,H*ss-1),radius=110*ss,fill=(28,24,22,255))
    d.rounded_rectangle((6*ss,6*ss,W*ss-7*ss,H*ss-7*ss),radius=104*ss,outline=(70,62,58,255),width=3*ss)
    img=img.resize((W,H),Image.LANCZOS)
    mask=Image.new('L',(w*ss,h*ss),0); ImageDraw.Draw(mask).rounded_rectangle((0,0,w*ss-1,h*ss-1),radius=84*ss,fill=255); mask=mask.resize((w,h),Image.LANCZOS)
    img.paste(sc,(b,b),mask)
    d=ImageDraw.Draw(img); cx=W//2; d.rounded_rectangle((cx-70,b+12,cx+70,b+44),radius=16,fill=(28,24,22,255))
    img.save(out/f'mockup_{name}.png'); return name
names=['01_login','10_home','11_home_no_group','20_shopping','22_shopping_detail','21_shopping_create_modal','30_fridge','31_fridge_add_modal','35_food','37_food_add_modal','40_meal','41_meal_suggestion','50_recipes','51_recipe_detail','52_recipe_editor','60_profile','61_group_manage','64_group_setup','70_reports_shopping','72_reports_waste','73_reports_fridge','90_loading_state','91_error_state','02_login_error','24_shopping_member','81_catalog_admin','32_fridge_datefield','04_verify_email','71_reports_consumption']
for n in names: frame(n)
print(len(names))
