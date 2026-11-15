# Component Inventory — mobile/src

> Thống kê từ `mobile/src/components/` (14 file) và các component cục bộ khai báo bên trong file màn hình.
> "Số nơi dùng" = số file màn hình import component (đếm bằng grep trên `src/app`).

## 1. Shared components (`src/components/ui`)

| Component | File | Props chính | Vai trò | Số nơi dùng |
|---|---|---|---|---|
| `AppButton` | `ui/AppButton.tsx` | `title`, `onPress`, `loading`, `disabled`, `variant: primary \| outline \| ghost` | Nút bấm chuẩn: cao tối thiểu 52 px, bo 12 px; primary nền xanh `accent`, outline viền xanh 1.5 px; loading thay chữ bằng `ActivityIndicator`; `accessibilityState {disabled, busy}` | 18 |
| `AppInput` | `ui/AppInput.tsx` | `label`, `error`, `secure` + mọi `TextInputProps` | Ô nhập có nhãn phía trên, cao 58 px, viền đổi màu khi focus (`primaryText`) và lỗi (`danger`); `secure` có nút "Hiện/Ẩn" | 13 |
| `SelectField` | `ui/SelectField.tsx` | `label`, `value`, `options[{id,name,label?}]`, `onChange`, `disabled` | Dropdown tự xây (không dùng picker hệ điều hành): mở inline, ô "Tìm…" lọc lựa chọn, dấu ✓ cho mục đang chọn | 6 |
| `DateField` | `ui/DateField.tsx` | `label`, `value: Date`, `onChange` | Ô ngày định dạng DD/MM/YYYY + lịch tháng inline (T2…CN), nút "Hôm nay", "Đóng" | 3 |
| `FormMessage` | `ui/FormMessage.tsx` | `type: error \| success \| info`, `message`, `autoHideMs=5000` | Thông báo nội tuyến kiểu banner có chấm màu; **success tự ẩn sau 5 s**, error/info giữ nguyên; `accessibilityLiveRegion="polite"` | 15 |
| `LinkText` | `ui/LinkText.tsx` | `children`, `onPress` | Hành động dạng chữ màu `primaryText` (Sửa, Xoá, Xem tất cả…), `hitSlop 8` | 10 |
| `Screen` | `ui/Screen.tsx` | `scroll`, `refreshing`, `onRefresh`, `footer` | Khung màn hình: SafeArea (top), ScrollView, kéo để làm mới (RefreshControl) | 13 |
| `ScreenHeader` | `ui/Screen.tsx` | `title`, `subtitle`, `right`, `onBack`, `boxed` | Tiêu đề màn hình; `boxed` = dải màu cam full-width cho 5 tab chính; `onBack` hiện "← Quay lại" cho màn con | 13 |
| `SectionCard` | `ui/SectionCard.tsx` | `title`, `action`, `children` | Thẻ nội dung nền trắng, viền `border`, bo 16 px, padding 16; tiêu đề + hành động bên phải | 13 |
| `StatTile` | `ui/StatTile.tsx` | `label`, `value`, `tone: primary \| warning \| danger \| success \| accent` | Ô số liệu nền màu nhạt theo tông, số cỡ 22 px | 4 |
| `ProgressBar` | `ui/ProgressBar.tsx` | `value`, `total` | Thanh tiến độ (tỉ lệ đã mua, đã tiêu thụ) | 4 |
| `Thumbnail` | `ui/Thumbnail.tsx` | `uri`, `label`, `size`, `round` | Ảnh (expo-image) hoặc fallback chữ cái đầu trên nền cam nhạt | 6 |
| `BarChart` | `ui/BarChart.tsx` | `data`, `color`, `secondaryValue`, `labelEvery`, `legend` | Biểu đồ cột tự vẽ bằng `View` (không thư viện chart), cuộn ngang khi > 14 điểm, hỗ trợ cột đôi | 1 (Báo cáo) |
| `LoadingState` / `EmptyState` / `ErrorState` | `ui/StateView.tsx` | `message`; `title`, `icon`, `materialIcon`, `action`; `message`, `onRetry` | Ba trạng thái dữ liệu thống nhất: spinner + chữ; icon tròn + tiêu đề + mô tả + nút; icon `cloud-offline` + "Không tải được dữ liệu" + "Thử lại" | 11 |
| `AuthLayout` | `components/auth/AuthLayout.tsx` | `title`, `subtitle`, `footer`, `onBack`, `centerContent` | Khung màn xác thực: hai hình tròn trang trí (kem, xanh nhạt), nhãn thương hiệu "ĐI CHỢ TIỆN LỢI", KeyboardAvoidingView, maxWidth 560 | 5 màn (4 auth + Đổi mật khẩu) |

## 2. Navigation components

| Thành phần | File | Mô tả |
|---|---|---|
| Root `Stack` (header ẩn) | `app/_layout.tsx` | Chứa nhóm (auth), (tabs) và các màn con; guard chuyển hướng theo `accessToken` |
| Auth `Stack` | `app/(auth)/_layout.tsx` | Hiệu ứng `slide_from_right`, nền `background` |
| Bottom `Tabs` | `app/(tabs)/_layout.tsx` | 5 tab; icon Ionicons/MaterialCommunityIcons dạng outline ↔ filled khi focus; màu active `primaryText`, inactive `textMuted`; nhãn 11 px; ẩn khi bàn phím mở; hiệu ứng fade 180 ms |
| Nút quay lại | `ScreenHeader.onBack`, `AuthLayout.onBack` | Chữ "← Quay lại" (không phải icon hệ thống) |
| Liên kết văn bản | `Link` (expo-router), `LinkText` | Điều hướng trong form xác thực và trong card |

## 3. Form components

`AppInput` (text, email, mật khẩu, số thập phân, đa dòng), `SelectField`, `DateField`, `FilterChip` (cục bộ trong `food.tsx`), `SegmentButton` (cục bộ trong `catalog.tsx`), preset chip 7/30/90 ngày và tab chip (cục bộ trong `reports.tsx`), dải ngày tuần (cục bộ trong `meal.tsx`), hàng nguyên liệu động (cục bộ trong `recipes.tsx`).

## 4. Data display components

`SectionCard`, `StatTile`, `ProgressBar`, `Thumbnail`, `BarChart`, badge hạn sử dụng (cục bộ `FridgeRow`), badge đếm `done/total` (cục bộ `ShoppingCard`), badge "Trưởng nhóm" (cục bộ `group/manage.tsx`), `InfoRow` (khai báo lặp lại ở `profile.tsx` và `group/manage.tsx`), `BreakdownCard` (cục bộ `reports.tsx`), `RenderHTML` (thư viện, chi tiết công thức).

## 5. Feedback components

| Loại | Cách hiện thực | Ghi chú |
|---|---|---|
| Thông báo nội tuyến | `FormMessage` (error/success/info) | Không có toast/snackbar nổi; thông báo nằm đầu màn hình |
| Trạng thái tải | `LoadingState`, `ActivityIndicator` trong `AppButton`, `RefreshControl` | |
| Trạng thái rỗng | `EmptyState` | Có nút hành động phù hợp vai trò |
| Lỗi tải | `ErrorState` + "Thử lại" | Thông điệp lấy từ backend (`getErrorMessage`) |
| Trạng thái thao tác dòng | Chữ "Đang xoá..." thay cho "Xoá" | Ở mọi danh sách có xoá |
| Cập nhật lạc quan | `useToggleShoppingTask` (onMutate/rollback) | Tick món đi chợ phản hồi tức thì |

## 6. Modal và dialog

| Loại | Nơi dùng | Mô tả |
|---|---|---|
| Modal form trung tâm (`Modal transparent, fade`) | Đi chợ (tạo/sửa list), Chi tiết list (thêm/sửa món), Tủ lạnh, Kho thực phẩm, Bữa ăn, Công thức, Danh mục | Lớp phủ `overlay`, thẻ bo góc, nút Lưu + Huỷ, chạm ngoài để đóng (bị chặn khi đang lưu) |
| Bottom sheet (`Modal slide`) | Gợi ý món từ tủ lạnh (`meal.tsx`) | Có tay nắm (handle), tiêu đề + "Đóng" |
| Hộp thoại hệ thống `Alert.alert` | Xác nhận xoá (list, món, thực phẩm, công thức, thành viên, danh mục), rời nhóm, chọn nguồn ảnh, thông báo đổi mật khẩu thành công | Nút huỷ `cancel`, nút xoá `destructive` |

> Style của modal (`modalOverlay`, `modalCard`, `modalTitle`, `modalHint`, `modalCancel`) được khai báo **lặp lại trong từng file màn hình** — chưa được tách thành component dùng chung.

## 7. Component / hook đặc thù nghiệp vụ

| Tên | File | Mô tả |
|---|---|---|
| `ShoppingCard`, `TaskPreview` | `(tabs)/shopping.tsx` | Thẻ danh sách: tên, người được giao, badge `done/total`, progress, 4 món đầu + "Xem thêm n món", ngày, hành động theo quyền |
| `TaskRow` | `shopping/[listId].tsx` | Checkbox tròn 24 px, gạch ngang khi đã mua |
| `FridgeRow` | `(tabs)/fridge.tsx` | Thumbnail 52, tên, badge hạn 3 tông (đỏ ≤ 0 ngày, vàng ≤ 3 ngày, xanh > 3 ngày), số lượng · vị trí, ngày hết hạn |
| `FoodRow`, `FilterChip` | `food.tsx` | Dòng thực phẩm; Sửa/Xoá chỉ hiện với người tạo hoặc trưởng nhóm |
| `MealList`, `MealRow`, `SuggestionRow` | `(tabs)/meal.tsx`, `(tabs)/index.tsx` | Danh sách món theo bữa; dòng gợi ý (lý do, khớp x/y nguyên liệu, thiếu gì) |
| `BreakdownCard` | `reports.tsx` | Bảng phân rã theo danh mục / người / lý do / vị trí |
| `SegmentButton` | `catalog.tsx` | Segmented control 2 lựa chọn |
| `useToggleShoppingTask` | `hooks/useToggleShoppingTask.ts` | Mutation tick món với optimistic update |
| `usePushNotifications` | `hooks/usePushNotifications.ts` | Xin quyền, lấy Expo push token, gửi backend, mở tab Tủ lạnh khi bấm thông báo `EXPIRY_REMINDER` |
| `useAuthStore` | `store/authStore.ts` | Zustand: user, accessToken, hydrate từ SecureStore, logout |

## 8. Nhận xét

- Bộ component đủ để các màn hình có giao diện nhất quán (cùng Card, Button, Input, State view).
- Một số mẫu UI lặp lại nhưng chưa được trừu tượng hoá: khung Modal form, `InfoRow`, chip lọc (FilterChip / preset / tab chip / SegmentButton là 4 cài đặt riêng cho cùng một khái niệm "chip chọn").
- Không có component Toast, Badge, Avatar, IconButton dùng chung; badge được định nghĩa cục bộ tại từng màn.
