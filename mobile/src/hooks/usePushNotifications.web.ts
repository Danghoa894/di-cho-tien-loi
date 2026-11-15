import { useCallback } from 'react';
import type { PushStatus } from './usePushNotifications';

// Metro ưu tiên file .web.ts khi build web, nên bản web không nạp expo-notifications
// (module này không hỗ trợ web). API giữ giống bản native.
type PushState = {
  status: PushStatus;
  message: string;
  token: string | null;
};

const unsupported: PushState = {
  status: 'unsupported',
  message: 'Thông báo đẩy không hỗ trợ trên web.',
  token: null,
};

export async function registerPushNotifications(): Promise<PushState> {
  return unsupported;
}

export function usePushNotifications(_options: {
  enabled: boolean;
  autoRequest?: boolean;
}) {
  const register = useCallback(
    async (_requestPermission = true) => unsupported,
    []
  );

  return { ...unsupported, register };
}
