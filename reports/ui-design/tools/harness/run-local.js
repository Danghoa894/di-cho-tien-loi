// Harness chỉ dùng để chụp ảnh giao diện: MongoDB in-memory + seed dữ liệu mẫu.
// KHÔNG thuộc source code sản phẩm.
const path = require('path');
const { execFileSync } = require('child_process');
const { MongoMemoryServer } = require('mongodb-memory-server');

(async () => {
  const mongod = await MongoMemoryServer.create({ instance: { port: 27099, dbName: 'dichotienloi' } });
  const uri = mongod.getUri('dichotienloi');
  const env = {
    ...process.env,
    PORT: '5050',
    NODE_ENV: 'development',
    MONGODB_URI: uri,
    JWT_ACCESS_SECRET: 'local-access-secret-for-screenshots-only-0123456789',
    JWT_REFRESH_SECRET: 'local-refresh-secret-for-screenshots-only-0123456789',
    JWT_ACCESS_EXPIRES_IN: '12h',
    AUTH_RATE_LIMIT_MAX: '0',
    SMTP_USER: '', SMTP_PASS: '',
    CLOUDINARY_CLOUD_NAME: '', CLOUDINARY_API_KEY: '', CLOUDINARY_API_SECRET: '',
    ADMIN_EMAIL: 'admin@example.com', ADMIN_PASSWORD: 'Admin@123', ADMIN_NAME: 'Quản trị viên', ADMIN_USERNAME: 'admin',
    EXPIRY_CRON_SCHEDULE: '0 3 1 1 *',
  };
  Object.assign(process.env, env);
  const opts = { cwd: __dirname, env, stdio: 'inherit' };
  execFileSync(process.execPath, [path.join('scripts', 'seed-sample-data.js')], opts);
  require('./server.js');
  const mongoose = require('mongoose');
  mongoose.connection.once('open', async () => {
    try {
      const { seedAdmin } = require('./scripts/seed-admin');
      // seedAdmin dùng kết nối mongoose hiện có (không gọi connectDB/disconnect ở đây)
      const r = await seedAdmin();
      console.log('Admin seeded:', r.user.email);
    } catch (e) { console.error('seedAdmin lỗi:', e.message); }
  });
})().catch((e) => { console.error(e); process.exit(1); });
