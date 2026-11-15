import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

// expo-secure-store không có bản web, nên trên web lưu tạm vào localStorage.
// Khi render phía server (web.output = "server") không có localStorage.
const webStorage = () =>
  typeof localStorage === 'undefined' ? null : localStorage;

export async function getItemAsync(key: string): Promise<string | null> {
  if (Platform.OS === 'web') return webStorage()?.getItem(key) ?? null;
  return SecureStore.getItemAsync(key);
}

export async function setItemAsync(key: string, value: string): Promise<void> {
  if (Platform.OS === 'web') {
    webStorage()?.setItem(key, value);
    return;
  }
  await SecureStore.setItemAsync(key, value);
}

export async function deleteItemAsync(key: string): Promise<void> {
  if (Platform.OS === 'web') {
    webStorage()?.removeItem(key);
    return;
  }
  await SecureStore.deleteItemAsync(key);
}
