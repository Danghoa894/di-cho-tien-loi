# Khảo sát cấu trúc dự án — Đi chợ tiện lợi (IT4788)

> Nguồn: đọc trực tiếp source code tại commit `335e386` (nhánh `claude/di-cho-uiux-analysis-683bcf`), ngày khảo sát 08/11/2026.
> Mọi nhận định dưới đây đều có căn cứ là file cụ thể trong repo.

## 1. Cấu trúc thư mục cấp cao

| Thư mục / file | Vai trò | Trạng thái |
|---|---|---|
| `mobile/` | Ứng dụng di động React Native + Expo + TypeScript | Đã triển khai |
| `server/` | Backend Node.js + Express 5 + MongoDB (Mongoose 9) | Đã triển khai (543 test theo `docs/test-report.md`) |
| `admin/` (web admin) | Trang quản trị web React + Vite + Ant Design | **Chưa khởi tạo** — không tồn tại thư mục; `docs/README.md` ghi "admin/ … (chưa khởi tạo)" và mục "Chưa làm: Trang admin web" |
| `docs/` | Tài liệu: kế hoạch kiến trúc, góp ý đặc tả API, README tiến độ, báo cáo kiểm thử, 3 file .docx thiết kế | Tài liệu |
| `postman/` | Postman collection + environment | Tài liệu kiểm thử API |
| `docker-compose.yaml`, `render.yaml` | Đóng gói và deploy backend (Render, Docker) | Hạ tầng |

Tổng số file được Git theo dõi: 216.

## 2. Mobile app (`mobile/`)

### 2.1 Entry point và cấu hình

| Hạng mục | Giá trị | File |
|---|---|---|
| Entry | `expo-router/entry` | `mobile/package.json` (`main`) |
| Thư mục route | `src/app` (Expo Router, file-based routing) | `mobile/src/app/` |
| Root layout | `src/app/_layout.tsx` — nạp font, hydrate phiên, điều hướng theo trạng thái đăng nhập, QueryClient, ThemeProvider | |
| Tên ứng dụng | "Đi chợ tiện lợi"; `orientation: portrait`; `userInterfaceStyle: light`; `ios.supportsTablet: false` | `mobile/app.json` |
| Splash / icon nền | `#FFE9A9` (vàng kem) | `mobile/app.json` |
| Plugin | expo-router, expo-splash-screen, expo-secure-store, expo-notifications, expo-image-picker (chuỗi xin quyền tiếng Việt) | `mobile/app.json` |
| Thử nghiệm | `typedRoutes: true`, `reactCompiler: true` | `mobile/app.json` |
| Build | EAS (development / preview / production) | `mobile/eas.json`, `mobile/BUILD.md` |
| API URL | `EXPO_PUBLIC_API_URL`, mặc định `http://10.0.2.2:5000/it4788` (Android) / `http://localhost:5000/it4788` | `src/config/env.ts`, `.env.example` |

### 2.2 Dependency chính (liên quan giao diện)

| Nhóm | Thư viện | Phiên bản khai báo |
|---|---|---|
| Nền tảng | expo / react-native / react | ~58.0.22 / 0.88.1 / 19.3.0 |
| Điều hướng | expo-router, react-native-screens, react-native-safe-area-context | ~58.0.29 / ~4.30.1 / ~5.10.1 |
| Dữ liệu server | @tanstack/react-query | ^5.105.2 |
| State cục bộ | zustand | ^5.0.16 |
| HTTP | axios (interceptor tự refresh token) | ^1.21.0 |
| Font | @expo-google-fonts/be-vietnam-pro (400/500/600/700) | ^0.4.1 |
| Icon | @expo/vector-icons (Ionicons, MaterialCommunityIcons) | ^15.0.2 |
| Ảnh | expo-image, expo-image-picker | ~58.0.18 / ~58.0.10 |
| Hiển thị HTML công thức | react-native-render-html | ^6.3.4 |
| Ngày tháng | dayjs (locale `vi`) | ^1.11.23 |
| Lưu phiên | expo-secure-store | ~58.0.2 |
| Thông báo | expo-notifications, expo-device, expo-constants | ~58.1.7 |

Không dùng thư viện UI kit bên thứ ba (không có NativeBase, React Native Paper, Tamagui…). Toàn bộ component giao diện được tự xây dựng trong `src/components/ui`. `@expo/ui`, `expo-glass-effect`, `expo-symbols` có trong `package.json` nhưng **không được import ở bất kỳ file nào trong `src/`**.

### 2.3 Tổ chức mã nguồn `mobile/src`

```
src/
├── app/                 # 23 file route (Expo Router)
│   ├── _layout.tsx      # root: font, splash, auth guard, QueryClient
│   ├── index.tsx        # file mẫu còn sót của create-expo-app (không được dùng — guard chuyển hướng trước)
│   ├── (auth)/          # _layout, index (redirect), login, register, verify-email, forgot-password
│   ├── (tabs)/          # _layout (5 tab), index, shopping, fridge, meal, profile
│   ├── shopping/[listId].tsx
│   ├── recipes.tsx, recipes/[recipeId].tsx
│   ├── food.tsx, catalog.tsx, reports.tsx, change-password.tsx
│   └── group/setup.tsx, group/manage.tsx
├── components/
│   ├── auth/AuthLayout.tsx
│   └── ui/              # 13 component dùng chung
├── api/                 # 13 file: client.ts (axios), *.api.ts theo module, queryKeys.ts
├── hooks/               # usePushNotifications.ts, useToggleShoppingTask.ts
├── store/authStore.ts   # Zustand + SecureStore
├── theme/               # colors.ts, index.ts (spacing, radius, fonts, typography)
├── types/               # api.ts, models.ts
└── utils/               # date.ts, error.ts, recipe.ts, validation.ts
```

### 2.4 Tài nguyên giao diện

| Tài nguyên | File |
|---|---|
| Icon ứng dụng | `assets/images/icon.png`, `assets/expo.icon/` (iOS) |
| Adaptive icon Android | `android-icon-foreground.png`, `android-icon-background.png`, `android-icon-monochrome.png` |
| Splash | `assets/images/splash-icon.png` |
| Favicon web | `assets/images/favicon.png` |
| Font | Be Vietnam Pro (tải qua package `@expo-google-fonts`, không có file font trong repo) |
| Icon trong UI | Ionicons, MaterialCommunityIcons (`@expo/vector-icons`) |
| Ảnh minh hoạ / illustration | **Không có** trong repo |

## 3. Backend (`server/`)

| Hạng mục | Nội dung |
|---|---|
| Entry | `server/server.js` → `src/app.js`; base path `/it4788`; health `GET /it4788/health` |
| Kiến trúc | routes → middlewares (auth, validate Joi, upload multer, rateLimit, audit, groupAdmin, admin) → controllers → services → models |
| Model (12) | User, Group, Category, Unit, Food, FridgeItem, FridgeEvent, ShoppingList, Task, MealPlan, Recipe, Log |
| Nhóm route | `/user`, `/user/group`, `/food`, `/fridge`, `/shopping`, `/meal`, `/recipe`, `/report`, `/admin` |
| Response | Khuôn thống nhất `{ code, message, data }` với mã 5 chữ số (`constants/responseCode.js`) — mobile hiển thị trực tiếp `message` tiếng Việt |
| Job | `jobs/expiryChecker.job.js` — cron 08:00 hằng ngày, gửi Expo Push cho món sắp hết hạn trong 3 ngày |
| Dịch vụ ngoài | MongoDB Atlas, Cloudinary (ảnh), Gmail SMTP (mã xác minh), Expo Push |

### 3.1 Phân quyền thực tế (đối chiếu service)

| Thao tác | Ai được phép | Căn cứ |
|---|---|---|
| CRUD danh mục, đơn vị | `role = admin` (admin hệ thống); mọi user đăng nhập được xem | `routes/admin.route.js` (`admin()`) |
| Quản trị user, xem logs | `role = admin` | `routes/admin.route.js` |
| Thêm / xoá thành viên nhóm | Trưởng nhóm | `routes/group.route.js` (`groupAdmin`) |
| Tạo / sửa / xoá danh sách và món đi chợ | Trưởng nhóm | `services/shopping.service.js:63` |
| Đánh dấu đã mua | Mọi thành viên trong nhóm | `services/shopping.service.js` (completeTask chỉ kiểm tra cùng nhóm) |
| Tạo / sửa / xoá kế hoạch bữa ăn | Trưởng nhóm | `services/meal.service.js:75` |
| Sửa / xoá thực phẩm trong kho | Người tạo hoặc trưởng nhóm | `services/food.service.js:51` |
| CRUD tủ lạnh, công thức | Mọi thành viên trong nhóm | `services/fridge.service.js`, `services/recipe.service.js` |

## 4. Web Admin

| Hạng mục | Trạng thái | Căn cứ |
|---|---|---|
| Mã nguồn web admin | **Chưa triển khai** (không có thư mục `admin/`, không có package React/Vite/AntD nào trong repo) | cây thư mục; `docs/README.md` |
| API phục vụ admin | **Đã có ở backend**: category, unit, logs, quản trị user (list/detail/update/lock/delete) | `server/src/routes/admin.route.js` |
| Giao diện admin trong mobile | **Một phần**: màn `catalog.tsx` cho phép user `role=admin` thêm/sửa/xoá danh mục & đơn vị; user thường chỉ xem. Không có màn quản trị user hay xem logs | `mobile/src/app/catalog.tsx` |
| Thiết kế web admin | Chỉ là định hướng trong `docs/01-KE-HOACH-KIEN-TRUC.md` (React + Vite + Ant Design) | |

## 5. Tài liệu dự án tìm thấy

| File | Nội dung |
|---|---|
| `docs/README.md` | Tiến độ chi tiết backend, mobile, việc chưa làm |
| `docs/01-KE-HOACH-KIEN-TRUC.md` | Công nghệ, kiến trúc, CSDL, danh sách 16 màn hình dự kiến, phân quyền 3 cấp, luồng nhắc hết hạn |
| `docs/02-GOP-Y-DAC-TA-API.md` | Góp ý / bổ sung đặc tả API |
| `docs/test-report.md` | Báo cáo kiểm thử backend |
| `docs/Đi chợ tiện lợi — *.docx` (3 file) | Mô hình yêu cầu, thiết kế backend, thiết kế ứng dụng (định dạng Word) |
| `mobile/BUILD.md` | Hướng dẫn build EAS |
