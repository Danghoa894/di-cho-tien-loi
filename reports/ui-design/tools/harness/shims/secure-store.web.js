// Shim CHỈ dùng cho harness chụp ảnh trên web: expo-secure-store không có bản web.
const ls = () => (typeof localStorage === 'undefined' ? null : localStorage);
export async function getItemAsync(k) { return ls()?.getItem(k) ?? null; }
export async function setItemAsync(k, v) { ls()?.setItem(k, v); }
export async function deleteItemAsync(k) { ls()?.removeItem(k); }
export function getItem(k) { return ls()?.getItem(k) ?? null; }
export function setItem(k, v) { ls()?.setItem(k, v); }
export async function isAvailableAsync() { return true; }
