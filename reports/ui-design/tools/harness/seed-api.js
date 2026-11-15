// Seed dữ liệu demo qua REST API của chính backend (harness chụp ảnh, không thuộc sản phẩm).
const BASE = 'http://localhost:5050/it4788';
const DAY = 24 * 3600 * 1000;
const iso = (offsetDays) => {
  const d = new Date();
  return new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()) + offsetDays * DAY).toISOString();
};

async function call(token, method, url, body) {
  const res = await fetch(BASE + url, {
    method,
    headers: { 'Content-Type': 'application/json', ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    body: body ? JSON.stringify(body) : undefined,
  });
  const json = await res.json();
  if (!res.ok) console.warn('  !', method, url, json.code, json.message);
  return json.data;
}
const login = async (email, password) => (await call(null, 'POST', '/user/login', { email, password })).accessToken;

(async () => {
  const admin = await login('admin@example.com', 'Admin@123');
  for (const name of ['Rau củ', 'Sữa & trứng', 'Trái cây', 'Đồ khô', 'Gia vị']) await call(admin, 'POST', '/admin/category', { name });
  for (const name of ['gram', 'quả', 'hộp', 'bó', 'lít', 'gói']) await call(admin, 'POST', '/admin/unit', { name });

  const an = await login('an.nguyen@example.com', 'Matkhau@123');
  const foods = [
    ['Cà chua', 'Rau củ', 'kg'], ['Rau muống', 'Rau củ', 'bó'], ['Hành lá', 'Rau củ', 'bó'],
    ['Đậu phụ', 'Rau củ', 'gói'], ['Trứng gà', 'Sữa & trứng', 'quả'], ['Sữa tươi', 'Sữa & trứng', 'hộp'],
    ['Sữa chua', 'Sữa & trứng', 'hộp'], ['Táo', 'Trái cây', 'kg'], ['Chuối', 'Trái cây', 'kg'],
    ['Gạo', 'Đồ khô', 'kg'], ['Nước mắm', 'Gia vị', 'lít'], ['Cải thảo', 'Rau củ', 'kg'],
  ];
  for (const [foodName, categoryName, unitName] of foods) await call(an, 'POST', '/food', { foodName, categoryName, unitName });

  // Sự kiện tủ lạnh cho báo cáo: thêm rồi lấy ra (dùng hết / hết hạn / bỏ đi)
  const tmp = [
    ['Chuối', 1.5, 3, 'consumed'], ['Sữa chua', 4, -2, 'expired'], ['Cải thảo', 1, 1, 'discarded'],
  ];
  for (const [foodName, quantity, d, reason] of tmp) {
    const item = await call(an, 'POST', '/fridge', { foodName, quantity, useWithin: iso(d), location: 'ngăn mát' });
    if (item) await call(an, 'DELETE', '/fridge', { foodName, reason });
  }
  // Ăn hết thịt bò cũ rồi thêm lại để có thêm lượt tiêu thụ
  await call(an, 'DELETE', '/fridge', { foodName: 'Thịt bò', reason: 'consumed' });

  const fridge = [
    ['Thịt bò', 0.5, 1, 'ngăn đá', 'Dùng cho bữa tối mai'], ['Cà chua', 0.8, 4, 'ngăn mát', null],
    ['Rau muống', 2, 1, 'ngăn mát', null], ['Hành lá', 1, 6, 'ngăn mát', null],
    ['Đậu phụ', 2, 2, 'ngăn mát', null], ['Trứng gà', 10, 12, 'cánh tủ', null],
    ['Sữa tươi', 3, 0, 'cánh tủ', null], ['Táo', 1, -2, 'ngăn mát', 'Kiểm tra trước khi ăn'],
  ];
  for (const [foodName, quantity, d, location, note] of fridge) {
    await call(an, 'POST', '/fridge', { foodName, quantity, useWithin: iso(d), location, ...(note ? { note } : {}) });
  }

  const l1 = await call(an, 'POST', '/shopping', { name: 'Đi chợ cuối tuần', assignToUsername: 'binhtran', note: 'Mua ở chợ gần nhà, ưu tiên rau tươi.', date: iso(1) });
  const l2 = await call(an, 'POST', '/shopping', { name: 'Đồ khô tháng 11', assignToUsername: 'annguyen', date: iso(5) });
  const t1 = await call(an, 'POST', '/shopping/task', { listId: l1.id, tasks: [
    { foodName: 'Cà chua', quantity: 1 }, { foodName: 'Rau muống', quantity: 2 }, { foodName: 'Trứng gà', quantity: 10 },
    { foodName: 'Thịt bò', quantity: 0.5 }, { foodName: 'Sữa tươi', quantity: 4 }, { foodName: 'Hành lá', quantity: 1 },
  ] });
  const t2 = await call(an, 'POST', '/shopping/task', { listId: l2.id, tasks: [
    { foodName: 'Gạo', quantity: 5 }, { foodName: 'Nước mắm', quantity: 1 },
  ] });
  const tasks1 = Array.isArray(t1) ? t1 : t1?.tasks ?? [];
  const tasks2 = Array.isArray(t2) ? t2 : t2?.tasks ?? [];
  for (const t of tasks1.slice(0, 2)) await call(an, 'PATCH', `/shopping/task/${t.id}/complete`, { isCompleted: true });
  for (const t of tasks2.slice(0, 1)) await call(an, 'PATCH', `/shopping/task/${t.id}/complete`, { isCompleted: true });

  const meals = [
    ['Rau muống', 'tối', 0], ['Đậu phụ', 'tối', 0], ['Trứng gà', 'sáng', 1], ['Thịt bò', 'tối', 1], ['Cà chua', 'trưa', 2],
  ];
  for (const [foodName, name, d] of meals) await call(an, 'POST', '/meal', { foodName, name, timestamp: iso(d) });

  const recipes = [
    { name: 'Canh cà chua trứng', description: 'Món canh chua ngọt dễ nấu, phù hợp bữa cơm gia đình hằng ngày.',
      ingredients: [{ foodName: 'Cà chua', quantity: 0.3 }, { foodName: 'Trứng gà', quantity: 2 }, { foodName: 'Hành lá', quantity: 1 }],
      htmlContent: '<p>Cà chua rửa sạch, cắt múi cau.</p><p>Phi thơm hành, xào cà chua đến khi mềm.</p><p>Thêm nước, đun sôi rồi đổ trứng đã đánh tan.</p><p>Nêm nếm vừa ăn, rắc hành lá.</p>' },
    { name: 'Rau muống xào tỏi', description: 'Rau muống xanh giòn xào tỏi thơm.',
      ingredients: [{ foodName: 'Rau muống', quantity: 1 }],
      htmlContent: '<p>Nhặt rau, rửa sạch, để ráo.</p><p>Phi tỏi, cho rau vào đảo nhanh tay trên lửa lớn.</p><p>Nêm nước mắm, tắt bếp.</p>' },
    { name: 'Đậu phụ sốt cà chua', description: 'Đậu phụ chiên vàng sốt cà chua đậm đà.',
      ingredients: [{ foodName: 'Đậu phụ', quantity: 1 }, { foodName: 'Cà chua', quantity: 0.2 }, { foodName: 'Hành lá', quantity: 1 }],
      htmlContent: '<p>Đậu phụ cắt miếng, chiên vàng.</p><p>Xào cà chua thành sốt, cho đậu vào rim 5 phút.</p><p>Rắc hành lá và tắt bếp.</p>' },
  ];
  for (const r of recipes) await call(an, 'POST', '/recipe', r);

  // User chưa có nhóm (trạng thái "chưa tham gia nhóm")
  const mongoose = require('mongoose');
  await mongoose.connect('mongodb://127.0.0.1:27099/dichotienloi');
  const { seedUser } = require('./scripts/seed-user');
  await seedUser({ email: 'cuong.le@example.com', password: 'Matkhau@123', name: 'Lê Văn Cường', username: 'cuongle' }).catch((e) => console.warn(e.message));
  await mongoose.disconnect();
  console.log('Seed API xong');
})().catch((e) => { console.error(e); process.exit(1); });
