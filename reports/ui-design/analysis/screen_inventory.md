# Screen Inventory — Ứng dụng di động "Đi chợ tiện lợi"

> Lập từ toàn bộ file route trong `mobile/src/app/` (23 file). Trạng thái triển khai được đánh giá theo mã nguồn thực tế:
> **Đã triển khai** = có UI + gọi API + xử lý trạng thái; **Một phần** = có UI nhưng thiếu chức năng đáng kể so với đặc tả / API sẵn có; **Không dùng** = file tồn tại nhưng không phải màn hình thực tế.

| STT | Module | Screen (tiêu đề hiển thị) | File Path | Chức năng | Thành phần UI | Trạng thái triển khai |
|---|---|---|---|---|---|---|
| 1 | Xác thực | Đăng nhập | `src/app/(auth)/login.tsx` | Đăng nhập email + mật khẩu; thông báo sau xác minh/đặt lại mật khẩu; liên kết "Xác minh email ngay" khi tài khoản chưa xác minh (mã `00044`) | AuthLayout, AppInput (email, mật khẩu ẩn/hiện), FormMessage, Link, AppButton | Đã triển khai |
| 2 | Xác thực | Tạo tài khoản | `src/app/(auth)/register.tsx` | Đăng ký (họ tên 3–30, email, mật khẩu 6–20, nhập lại) → chuyển sang xác minh email | AuthLayout, 4×AppInput, FormMessage, AppButton | Đã triển khai |
| 3 | Xác thực | Xác minh email | `src/app/(auth)/verify-email.tsx` | Nhập mã 6 số; gửi lại mã có đếm ngược 60 s; nhánh nhập email khi chưa có token | AuthLayout, AppInput (mã OTP căn giữa, letter-spacing), 2×AppButton | Đã triển khai |
| 4 | Xác thực | Quên mật khẩu | `src/app/(auth)/forgot-password.tsx` | Hai bước: nhập email → nhập mã + mật khẩu mới; gửi lại mã có đếm ngược | AuthLayout, AppInput, AppButton (primary/outline) | Đã triển khai |
| 5 | Xác thực | (chuyển hướng) | `src/app/(auth)/index.tsx` | `<Redirect href="/(auth)/login">` | — | Điều hướng, không có UI |
| 6 | Tab Trang chủ | Xin chào, {tên} | `src/app/(tabs)/index.tsx` | Dashboard: thống kê tủ lạnh, tiến độ danh sách mua sắm, bữa ăn hôm nay, lối tắt Công thức, Báo cáo; trạng thái "chưa tham gia nhóm" | ScreenHeader (boxed, avatar), SectionCard ×5, StatTile, ProgressBar, LinkText, AppButton, Loading/Empty/ErrorState | Đã triển khai |
| 7 | Tab Đi chợ | Đi chợ | `src/app/(tabs)/shopping.tsx` | Danh sách các list của nhóm; thống kê; tick món nhanh; trưởng nhóm tạo/sửa/xoá list (modal) | ScreenHeader, StatTile ×3, ShoppingCard (badge, ProgressBar, TaskPreview), Modal (AppInput, SelectField, DateField), Alert xác nhận | Đã triển khai |
| 8 | Đi chợ | Chi tiết danh sách | `src/app/shopping/[listId].tsx` | Xem món, tick đã mua, trưởng nhóm thêm/sửa/xoá món, xoá danh sách; tự mở form thêm món sau khi tạo list (`?openAdd=1`) | ScreenHeader (back), SectionCard, ProgressBar, TaskRow (checkbox), Modal (SelectField, AppInput) | Đã triển khai |
| 9 | Tab Tủ lạnh | Tủ lạnh | `src/app/(tabs)/fridge.tsx` | Danh sách thực phẩm trong tủ, nhãn hạn dùng 3 màu, thêm/sửa/xoá món, lối vào Kho thực phẩm | ScreenHeader, StatTile ×3, FridgeRow (Thumbnail, badge hạn), Modal (SelectField, DateField, SelectField vị trí), 2 AppButton chân trang | Đã triển khai (chưa có lọc theo danh mục như kế hoạch `docs/01` mục 5.2) |
| 10 | Tủ lạnh | Kho thực phẩm | `src/app/food.tsx` | Tìm kiếm, lọc chip theo danh mục, CRUD thực phẩm của nhóm kèm ảnh (thư viện/camera, ≤ 5 MB) | ScreenHeader (back), AppInput tìm kiếm, FilterChip (cuộn ngang), FoodRow, Modal (Thumbnail 88, SelectField ×2) | Đã triển khai |
| 11 | Tab Bữa ăn | Bữa ăn | `src/app/(tabs)/meal.tsx` | Dải 7 ngày; 3 bữa sáng/trưa/tối; trưởng nhóm thêm/sửa/xoá món; bottom sheet "Gợi ý món từ tủ lạnh" | ScreenHeader, week strip, AppButton outline, SectionCard ×3, MealList, Modal form, Modal bottom sheet (SuggestionRow) | Đã triển khai |
| 12 | Bữa ăn | Công thức | `src/app/recipes.tsx` | Tìm kiếm, danh sách công thức, thêm/sửa (nhiều nguyên liệu động, cách làm dạng text → HTML), xoá | ScreenHeader (back), AppInput tìm kiếm, SectionCard/recipe card, Modal (ingredient rows: SelectField + AppInput) | Đã triển khai |
| 13 | Bữa ăn | Chi tiết công thức | `src/app/recipes/[recipeId].tsx` | Mô tả, nguyên liệu + định lượng, cách làm render HTML, sửa/xoá | ScreenHeader, SectionCard ×3, RenderHTML, 2 AppButton | Đã triển khai |
| 14 | Tab Cá nhân | Cá nhân | `src/app/(tabs)/profile.tsx` | Thông tin tài khoản, đổi ảnh đại diện, thông tin nhóm, đổi mật khẩu, trạng thái thông báo, lối vào Báo cáo, Danh mục & đơn vị, Đăng xuất | ScreenHeader, SectionCard ×5, Thumbnail tròn + badge camera, role badge, InfoRow, AppButton outline | **Một phần**: không sửa được họ tên, username, giới tính, ngày sinh dù API `PUT /user` hỗ trợ; không có xoá tài khoản |
| 15 | Cá nhân | Nhóm gia đình (thiết lập) | `src/app/group/setup.tsx` | Hiển thị username để gửi trưởng nhóm, tạo nhóm mới, "Kiểm tra lại" sau khi được thêm | ScreenHeader (back), SectionCard ×3, usernameBox, AppInput, AppButton | Đã triển khai (phụ thuộc username — xem hạn chế #1) |
| 16 | Cá nhân | Quản lý nhóm | `src/app/group/manage.tsx` | Thông tin nhóm, thêm thành viên theo username (trưởng nhóm), danh sách thành viên + xoá, rời nhóm (chuyển quyền trưởng nhóm) | ScreenHeader, InfoRow, AppInput, member row (Thumbnail tròn, badge "Trưởng nhóm"), Alert | Đã triển khai |
| 17 | Cá nhân | Đổi mật khẩu | `src/app/change-password.tsx` | Mật khẩu hiện tại / mới / xác nhận; đăng xuất mọi phiên sau khi đổi | AuthLayout (back), 3×AppInput secure, AppButton, hint | Đã triển khai |
| 18 | Cá nhân / Trang chủ | Báo cáo | `src/app/reports.tsx` | Khoảng 7/30/90 ngày; tổng quan; 4 tab Mua sắm/Tiêu thụ/Lãng phí/Tủ lạnh với biểu đồ cột và bảng phân rã | ScreenHeader, preset chips, StatTile, tab chips, BarChart (tự vẽ bằng View), BreakdownCard, ProgressBar | Đã triển khai |
| 19 | Cá nhân | Danh mục & đơn vị | `src/app/catalog.tsx` | Segment Danh mục/Đơn vị; user thường chỉ xem; `role=admin` thêm/sửa/xoá | ScreenHeader, segment control, FormMessage info, list có số thứ tự, Modal | Đã triển khai (đây là phần quản trị duy nhất có giao diện) |
| 20 | Hệ thống | Root layout | `src/app/_layout.tsx` | Font, splash, hydrate phiên, guard điều hướng, đăng ký push | — | Hạ tầng điều hướng |
| 21 | Hệ thống | Tabs layout | `src/app/(tabs)/_layout.tsx` | Thanh tab 5 mục, icon outline/filled theo trạng thái | Tabs (Ionicons, MaterialCommunityIcons) | Hạ tầng điều hướng |
| 22 | Hệ thống | Auth layout | `src/app/(auth)/_layout.tsx` | Stack, hiệu ứng `slide_from_right` | — | Hạ tầng điều hướng |
| 23 | — | "Edit src/app/index.tsx…" | `src/app/index.tsx` | File mẫu còn sót của create-expo-app; guard ở root layout chuyển hướng trước khi người dùng thấy | Text | Không dùng (nên xoá) |

**Tổng hợp:** 17 màn hình nghiệp vụ có giao diện (STT 1–4, 6–19), 4 file layout/redirect, 1 file mẫu không dùng.

## Màn hình dự kiến trong `docs/01-KE-HOACH-KIEN-TRUC.md` (mục 5.2) — đối chiếu

| # kế hoạch | Màn hình dự kiến | Thực tế | Ghi chú |
|---|---|---|---|
| 1–3 | Đăng nhập, Đăng ký, Xác minh email | Có | Bổ sung Quên mật khẩu |
| 4 | Trang chủ | Có | |
| 5 | Tủ lạnh + lọc theo danh mục + cảnh báo màu | Một phần | Có cảnh báo màu; **không có lọc theo danh mục** |
| 6 | Thêm/sửa đồ tủ lạnh | Có (modal trong tab Tủ lạnh) | Không phải màn riêng |
| 7–9 | Danh sách đi chợ, Chi tiết list, Tạo list & phân công | Có | Tạo list là modal |
| 10 | Lịch bữa ăn theo ngày/tuần | Có | Dải 7 ngày tới; không xem lùi ngày quá khứ |
| 11 | Gợi ý món ăn | Có (bottom sheet) | |
| 12 | Kho thực phẩm | Có | Kế hoạch là `food/[id].tsx`, thực tế là `food.tsx` + modal |
| 13 | Công thức nấu ăn | Có | |
| 14 | Quản lý nhóm | Có | |
| 15 | Hồ sơ cá nhân (sửa tên, ảnh, đổi mật khẩu) | Một phần | Chỉ đổi ảnh + đổi mật khẩu; **không sửa tên** |
| 16 | Thống kê | Có | |
| — | Web admin | **Chưa triển khai** | Chỉ có API backend |

## Chức năng có API nhưng **không có** giao diện (không lấy API làm bằng chứng UI)

| API | Mô tả | Ghi chú |
|---|---|---|
| `PUT /user` (name, username, gender, birthday, language, timezone) | Sửa hồ sơ | Mobile chỉ dùng để upload avatar |
| `DELETE /user` | Xoá tài khoản | Không có UI |
| `POST /user/logout` | Thu hồi refresh token | `authStore.logout()` chỉ xoá token cục bộ, không gọi API |
| `GET /fridge/item?foodName=` | Xem một mục tủ lạnh | Không dùng |
| `DELETE /fridge` với `reason` (`discarded`) | Ghi nhận "bỏ đi" | UI chỉ gọi `DELETE /fridge/:itemId`, backend tự suy ra `consumed`/`expired` |
| `GET /admin/logs`, `/admin/user*` | Nhật ký, quản trị người dùng | Dành cho web admin chưa có |
