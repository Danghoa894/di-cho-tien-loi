# Design System Audit

> Kết luận chung: dự án **có bộ design token** (màu ngữ nghĩa, spacing, radius, font, typography) tập trung ở `mobile/src/theme/` và **bộ component cơ sở** ở `mobile/src/components/ui/`. Đây là một design system ở mức "token + component trong code"; **chưa có** tài liệu design system riêng, file Figma, Storybook hay quy tắc sử dụng ngoài comment trong code.

## 1. Màu sắc (`theme/colors.ts`)

Palette gốc (Color Hunt): `#FF933E` cam · `#FFCB56` vàng · `#FFE9A9` kem · `#73A5CA` xanh. Quy ước trong code: `primary` chỉ dùng làm nền; chữ cam trên nền sáng dùng `primaryText` để đủ tương phản.

| Token | Giá trị | Dùng cho |
|---|---|---|
| `primary` | `#FF933E` | Header boxed của 5 tab, tab chip/preset đang chọn, cột "Cần mua" của biểu đồ, thanh progress |
| `primaryText` | `#9A3F00` | Link, tab active, focus viền input, chữ cam |
| `primarySoft` | `#FFE9D6` | Nền StatTile primary, icon tròn EmptyState, Thumbnail fallback |
| `secondary` / `secondarySoft` | `#FFCB56` / `#FFF3D1` | Ít dùng trực tiếp |
| `accent` | `#73A5CA` | **Nền nút primary**, viền nút outline, cột "Đã mua" |
| `accentText` | `#2F6F99` | Chữ nút outline |
| `onAccent` | `#0E2A3A` | Chữ trên nút primary |
| `background` | `#FFFBF5` | Nền màn hình (trắng ấm) |
| `surface` | `#FFFFFF` | Card, input, tab bar |
| `highlight` | `#FFE9A9` | Hình tròn trang trí AuthLayout, splash |
| `border` | `#F0DFC8` | Viền card/input |
| `text` / `textMuted` | `#2A1A0F` / `#7A6656` | Chữ chính / phụ |
| `success` / `warning` / `danger` / `info` (+ `Soft`) | `#2E7D32` / `#8A5A00` / `#C62828` / `#2F6F99` | Badge hạn dùng, StatTile, FormMessage |
| `overlay` | `rgba(42,26,15,.45)` | Nền mờ modal |
| `chartColors` | 6 màu theo palette gốc | Khai báo nhưng biểu đồ hiện dùng trực tiếp `primary`, `accent`, `success`, `danger` |

Chế độ: chỉ giao diện sáng (`app.json: userInterfaceStyle: light`); comment trong code ghi rõ dark mode chưa làm.

### Kiểm tra tương phản (WCAG 2.1, tính từ mã màu)

| Cặp màu | Tỉ lệ | Đánh giá |
|---|---|---|
| `text` trên `background` | 16.26 : 1 | Đạt AAA |
| `textMuted` trên `background` | 5.27 : 1 | Đạt AA |
| `primaryText` trên `surface` | 6.81 : 1 | Đạt AA |
| `onAccent` trên `accent` (nút primary) | 5.64 : 1 | Đạt AA |
| `accentText` trên `surface` (nút outline) | 5.45 : 1 | Đạt AA |
| StatTile primary / warning / danger / success | 5.80 / 5.36 / 4.92 / 4.56 : 1 | Đạt AA |
| **Chữ trắng trên header `primary`** | **2.21 : 1** | **Không đạt** AA kể cả chữ lớn (cần ≥ 3 : 1) |
| (tham khảo) `onPrimary` `#2A1608` trên `primary` | 7.80 : 1 | Token đã có nhưng header không dùng |

## 2. Typography (`theme/index.ts`)

Font: **Be Vietnam Pro** (thiết kế cho tiếng Việt) — 4 weight 400/500/600/700, nạp trong root layout trước khi ẩn splash.

| Variant | Cỡ / line-height | Weight | Dùng cho |
|---|---|---|---|
| `display` | 28 / 34 | Bold | Tiêu đề màn xác thực |
| `title` | 22 / 28 | Bold | Tiêu đề màn hình, số trong StatTile |
| `heading` | 18 / 24 | SemiBold | Tiêu đề SectionCard, modal |
| `body` | 16 / 22 | Regular | Nội dung |
| `bodyStrong` | 16 / 22 | SemiBold | Nút, tên món, link quan trọng |
| `caption` | 13 / 18 | Regular | Gợi ý, mô tả phụ |
| `label` | 12 / 16 | SemiBold | Nhãn input, badge, tab (ghi đè 11 px) |

Ngoại lệ: input dùng 17 px; mã OTP 24 px letter-spacing 8.

## 3. Spacing & radius

| Token | xs | sm | md | lg | xl | xxl |
|---|---|---|---|---|---|---|
| spacing (px) | 4 | 8 | 12 | 16 | 24 | 32 |

| Radius | sm 8 | md 12 | lg 16 | xl 24 | pill 999 |
|---|---|---|---|---|---|
| Dùng cho | — | Nút, input, StatTile, Thumbnail | SectionCard | Modal card | Chip |

Lề màn hình 16 px (`Screen`), lề AuthLayout 24 px; khoảng cách giữa card 16 px.

## 4. Icon
`@expo/vector-icons`: Ionicons (home, cart, restaurant, person, checkmark-circle, ellipse-outline, calendar, chevron, camera, cloud-offline, people, book, nutrition, search…) và MaterialCommunityIcons (fridge). Không có bộ icon/illustration riêng.

## 5. Component cơ sở (tóm tắt)

| Thành phần | Quy cách |
|---|---|
| Button | 3 biến thể primary/outline/ghost; cao ≥ 52; bo 12; pressed opacity .82; disabled opacity .5; loading spinner |
| Input | Nhãn trên; cao ≥ 58; viền 1 px `border`, focus `primaryText`, lỗi `danger`; toggle "Hiện/Ẩn" mật khẩu |
| Select / Date | Dropdown & lịch inline tự xây, cùng khung với Input |
| Card | `SectionCard` nền trắng, viền, bo 16, padding 16 |
| Navigation | Bottom tabs 5 mục, header boxed màu cam cho tab, "← Quay lại" chữ cho màn con |
| Feedback | FormMessage, Loading/Empty/Error state, Alert hệ thống |

## 6. Đánh giá mức độ trưởng thành

| Tiêu chí | Hiện trạng |
|---|---|
| Token tập trung | Có (màu ngữ nghĩa, spacing, radius, typography) |
| Mọi màn dùng token | Phần lớn; vẫn còn giá trị cứng (vd. `fontSize: 11`, `24`, `rgba(255,255,255,.88)`, `#F59E0B` cho đèn kênh thông báo Android) |
| Component tái sử dụng | 13 component UI + AuthLayout |
| Mẫu lặp lại chưa tách | Modal form, InfoRow, các loại chip |
| Dark mode | Chưa |
| Tài liệu hoá | Chưa (chỉ comment trong `colors.ts`) |
| Kiểm thử giao diện | Không có test UI / snapshot trong `mobile/` |
