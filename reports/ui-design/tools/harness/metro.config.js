// Cấu hình Metro CHỈ cho harness chụp ảnh web (đặt vào BẢN SAO của mobile/, không phải repo sản phẩm).
const path = require('path');
const { getDefaultConfig } = require('expo/metro-config');
const config = getDefaultConfig(__dirname);
const shims = {
  'expo-secure-store': path.resolve(__dirname, 'harness-shims/secure-store.web.js'),
  'expo-notifications': path.resolve(__dirname, 'harness-shims/notifications.web.js'),
};
const orig = config.resolver.resolveRequest;
config.resolver.resolveRequest = (context, moduleName, platform) => {
  if (platform === 'web' && shims[moduleName]) return { type: 'sourceFile', filePath: shims[moduleName] };
  return orig ? orig(context, moduleName, platform) : context.resolveRequest(context, moduleName, platform);
};
module.exports = config;
