# User Flows — dựng từ navigation và xử lý nghiệp vụ trong code

Ký hiệu trạng thái: ✅ triển khai đầy đủ · ◐ triển khai một phần · ✗ chưa có giao diện.

## 1. Information Architecture (thực tế)

```
Ứng dụng
├── (auth) — chưa đăng nhập
│   ├── Đăng nhập ──► Quên mật khẩu (2 bước)
│   │             └─► Xác minh email (khi lỗi 00044)
│   └── Tạo tài khoản ──► Xác minh email ──► Đăng nhập
└── (tabs) — đã đăng nhập
    ├── Trang chủ          → lối tắt: Tủ lạnh, Đi chợ, Bữa ăn, Công thức, Báo cáo, Cá nhân (avatar), Thiết lập nhóm
    ├── Đi chợ             → Chi tiết danh sách [listId] (modal thêm/sửa món)  · modal tạo/sửa danh sách
    ├── Tủ lạnh            → Kho thực phẩm (food)  · modal thêm/sửa món trong tủ
    ├── Bữa ăn             → bottom sheet Gợi ý món → Chi tiết công thức
    │                      → Công thức (recipes) → Chi tiết công thức [recipeId]
    └── Cá nhân            → Quản lý nhóm / Thiết lập nhóm
                           → Đổi mật khẩu
                           → Báo cáo (reports)
                           → Danh mục & đơn vị (catalog)
```

Các màn con (`shopping/[listId]`, `food`, `recipes`, `recipes/[recipeId]`, `reports`, `catalog`, `change-password`, `group/*`) nằm ở Stack gốc nên **thanh tab bị ẩn** khi mở và quay lại bằng "← Quay lại".

## 2. Các luồng

### F1. Đăng ký và đăng nhập ✅
1. `Đăng nhập` → "Đăng ký ngay" → `Tạo tài khoản` (kiểm tra cục bộ: họ tên 3–30, email, mật khẩu 6–20, khớp nhập lại).
2. `POST /user` thành công → `router.replace('/(auth)/verify-email', {email, token})`.
3. `Xác minh email`: nhập 6 số (`isSixDigitCode`), có "Gửi lại mã" với đếm ngược 60 s → `POST /user/verify-email` → về `Đăng nhập?verified=1` (banner xanh "Email đã được xác minh").
4. `Đăng nhập` → `POST /user/login` → `setSession` (SecureStore) → `/(tabs)`.
5. Nhánh lỗi: tài khoản chưa xác minh (`00044`) → hiện liên kết "Xác minh email ngay →".
6. Phiên: interceptor tự gọi `refresh-token` khi gặp mã `00011/00012` rồi phát lại request.

### F2. Quên mật khẩu ✅
Bước 1 nhập email → `POST /user/forgot-password` → Bước 2 (mã, mật khẩu mới, nhập lại; gửi lại mã có cooldown) → `POST /user/reset-password` → `Đăng nhập?reset=1`. "← Quay lại" ở bước 2 đưa về bước 1 thay vì thoát màn.

### F3. Quản lý nhóm gia đình ✅ (◐ phụ thuộc username)
- Người chưa có nhóm: Trang chủ / Kho / Báo cáo hiển thị EmptyState "Bạn chưa tham gia nhóm" + "Thiết lập nhóm".
- `Thiết lập nhóm`: hiển thị `@username` để gửi trưởng nhóm; tạo nhóm (≤ 50 ký tự) → `authApi.me()` → vào `/(tabs)`; hoặc "Kiểm tra lại" sau khi được thêm.
- `Quản lý nhóm` (trưởng nhóm): thêm thành viên bằng username 3–15 ký tự, xoá thành viên (Alert xác nhận). Mọi thành viên: "Rời nhóm" (cảnh báo chuyển quyền nếu là trưởng nhóm) → về `group/setup`.
- **Hạn chế:** đăng ký không tạo username và app không có màn sửa hồ sơ → tài khoản đăng ký mới hiển thị "Chưa đặt username" và không thể được thêm vào nhóm qua app (chỉ có thể tự tạo nhóm).

### F4. Tạo và quản lý danh sách đi chợ ✅ (chỉ trưởng nhóm)
`Đi chợ` → "Tạo danh sách mua sắm" → modal (tên, giao cho [SelectField thành viên có username], ngày [DateField], ghi chú) → `POST /shopping` → tự chuyển `shopping/[listId]?openAdd=1` và mở sẵn modal "Thêm món cần mua". Sửa/Xoá danh sách từ card hoặc màn chi tiết. Thành viên thường thấy danh sách nhưng không có nút tạo/sửa/xoá.

### F5. Thêm món và đánh dấu đã mua ✅
- Thêm món (trưởng nhóm): chọn thực phẩm có sẵn trong **Kho thực phẩm** + số lượng (> 0, ≤ 1.000.000) → `POST /shopping/task`.
- Đánh dấu đã mua (mọi thành viên): chạm vào vòng tròn ở card hoặc màn chi tiết → `PATCH /shopping/task/:id/complete`; cập nhật lạc quan, rollback khi lỗi; tiến độ (badge, progress, Trang chủ) cập nhật.
- ◐ Đánh dấu đã mua **không tự thêm món vào tủ lạnh** — người dùng phải thêm thủ công ở tab Tủ lạnh.

### F6. Quản lý thực phẩm trong tủ lạnh ✅
`Tủ lạnh` → "Thêm thực phẩm" → modal (thực phẩm từ kho, số lượng, hạn dùng mặc định +7 ngày, vị trí: Ngăn mát/Ngăn đá/Cánh tủ/Ngoài tủ, ghi chú) → `POST /fridge`. Sửa (không đổi được thực phẩm), Xoá (Alert "được ghi nhận vào báo cáo" → `DELETE /fridge/:itemId`, backend tự ghi `consumed` hoặc `expired`). Chưa có thực phẩm → vào "Kho thực phẩm" để tạo (tên, danh mục, đơn vị, ảnh).

### F7. Theo dõi thực phẩm sắp hết hạn ✅
- Trong app: thống kê "Sắp hết hạn / Đã hết hạn" (Trang chủ, Tủ lạnh, Báo cáo), badge màu từng món, câu nhắc "n món cần dùng sớm để tránh lãng phí".
- Push: cron 08:00 gửi thông báo cho món hết hạn trong 3 ngày; bấm thông báo (`type = EXPIRY_REMINDER`) → mở tab Tủ lạnh. Cá nhân hiển thị trạng thái quyền và nút "Bật thông báo". (Không kiểm chứng được trên thiết bị thật — xem giới hạn.)

### F8. Lập kế hoạch bữa ăn ✅ (chỉ trưởng nhóm sửa)
`Bữa ăn` → chọn ngày trên dải 7 ngày → mỗi bữa Sáng/Trưa/Tối có "Thêm" → modal (thực phẩm, bữa, ngày) → `POST /meal`; Sửa/Xoá từng món. Thành viên chỉ xem. ◐ Không xem được ngày quá khứ; món ăn trong kế hoạch là **thực phẩm** (food), không phải công thức.

### F9. Gợi ý món ăn ✅
`Bữa ăn` → "Gợi ý món từ tủ lạnh (n)" → bottom sheet: mỗi gợi ý có tên công thức, lý do (vd. "Dùng Đậu phụ còn 2 ngày"), "Khớp x/y nguyên liệu · Thiếu …/Đủ nguyên liệu", "Xem công thức", "Thêm vào bữa ăn" (trưởng nhóm; mở modal với bữa trưa và nguyên liệu khớp đầu tiên). Rỗng → gợi ý "Mở tủ lạnh" / "Xem công thức".

### F10. Quản lý công thức ✅
Vào từ Trang chủ hoặc Bữa ăn → `Công thức`: tìm kiếm cục bộ theo tên/mô tả; thêm/sửa trong modal với danh sách nguyên liệu động (thêm/xoá dòng, không trùng thực phẩm) và "Cách làm" (mỗi dòng → một `<p>`); Chi tiết hiển thị HTML bằng `RenderHTML`; "Sửa công thức" → quay về danh sách với `?editId` và tự mở form.

### F11. Xem báo cáo ✅
Từ Trang chủ hoặc Cá nhân → `Báo cáo`: chọn 7/30/90 ngày → Tổng quan (4 StatTile + câu tóm tắt tủ lạnh) → tab Mua sắm (biểu đồ cột đôi cần mua/đã mua, theo danh mục, theo người được giao), Tiêu thụ, Lãng phí (tỉ lệ = bỏ đi / đã xử lý, theo lý do), Tủ lạnh (theo vị trí, danh mục, "Cần dùng sớm").

### F12. Quản trị danh mục & đơn vị ◐
`Cá nhân` → "Danh mục & đơn vị": user thường chỉ xem (banner info); `role=admin` thêm/sửa/xoá. Quản trị người dùng và nhật ký: ✗ (chỉ có API, web admin chưa khởi tạo).

### F13. Hồ sơ cá nhân ◐
Đổi ảnh đại diện (thư viện/camera, ≤ 5 MB), đổi mật khẩu (đăng xuất mọi phiên), đăng xuất. ✗ Sửa họ tên/username/giới tính/ngày sinh, ✗ xoá tài khoản, ✗ gọi API logout phía server.

## 3. Bảng tổng hợp

| Luồng | Trạng thái | Ghi chú chính |
|---|---|---|
| Đăng ký, xác minh, đăng nhập | ✅ | |
| Quên mật khẩu | ✅ | |
| Nhóm gia đình | ✅ / ◐ | Thiếu cách đặt username trong app |
| Danh sách đi chợ | ✅ | Chỉ trưởng nhóm tạo/sửa |
| Thêm món, đánh dấu đã mua | ✅ / ◐ | Không tự chuyển vào tủ lạnh |
| Tủ lạnh | ✅ / ◐ | Không lọc theo danh mục; không chọn lý do "bỏ đi" |
| Theo dõi hết hạn | ✅ | Push chưa kiểm chứng trên thiết bị |
| Kế hoạch bữa ăn | ✅ / ◐ | Chỉ 7 ngày tới |
| Gợi ý món | ✅ | |
| Công thức | ✅ | |
| Báo cáo | ✅ | |
| Quản trị (web admin) | ✗ | Chỉ có API + màn Danh mục trên mobile |
| Sửa hồ sơ | ✗ | API có, UI không có |
