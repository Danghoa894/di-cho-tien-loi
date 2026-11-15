// Shim CHỈ dùng cho harness chụp ảnh trên web: expo-notifications không chạy trên web.
export const AndroidImportance = { HIGH: 4, DEFAULT: 3 };
export function setNotificationHandler() {}
export function useLastNotificationResponse() { return null; }
export function clearLastNotificationResponse() {}
export async function setNotificationChannelAsync() { return null; }
export async function getPermissionsAsync() { return { status: 'undetermined', granted: false }; }
export async function requestPermissionsAsync() { return { status: 'denied', granted: false }; }
export async function getExpoPushTokenAsync() { throw new Error('unsupported on web'); }
