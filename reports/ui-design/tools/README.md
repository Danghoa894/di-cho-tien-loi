# Công cụ tái tạo tài liệu thiết kế giao diện

Các script dùng để tạo ảnh chụp, sơ đồ và hai file DOCX/PPTX trong `reports/ui-design/`.
Không có script nào chỉnh sửa mã nguồn sản phẩm; harness chạy trên **bản sao** của `mobile/` và `server/`.

| File | Vai trò |
|---|---|
| `harness/run-local.js` | Đặt vào bản sao `server/`: MongoDB in-memory + `seed-sample-data.js` + seed admin, chạy API ở cổng 5050 |
| `harness/seed-api.js` | Tạo dữ liệu demo qua REST API (danh mục, thực phẩm, tủ lạnh, danh sách đi chợ, bữa ăn, công thức, user chưa có nhóm) |
| `harness/metro.config.js`, `harness/shims/*` | Đặt vào bản sao `mobile/` (thư mục `harness-shims/`): thay `expo-secure-store`, `expo-notifications` trên web |
| `capture.py` | Playwright chụp 51 ảnh màn hình (390×844 @2x) → `assets/screenshots/` |
| `diagrams.py` | HTML → PNG cho IA, navigation, user flow, design system, kiến trúc → `assets/diagrams/` |
| `mockup.py` | Đặt ảnh chụp thật vào khung điện thoại → `assets/illustrations/` |
| `build_docx.py`, `word_update.ps1` | Tạo báo cáo Word (python-docx), cập nhật mục lục và xuất PDF bằng Microsoft Word |
| `build_pptx.py`, `ppt_pdf.ps1` | Tạo slide (python-pptx) và xuất PDF bằng PowerPoint để kiểm tra |

Lưu ý: bản sao `mobile/` phải nằm cùng ổ đĩa với `node_modules` (Expo Router dùng đường dẫn tương đối tới `src/app`).
Đường dẫn tuyệt đối trong script cần chỉnh lại theo máy.
