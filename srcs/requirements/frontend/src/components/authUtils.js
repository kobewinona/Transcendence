import { useRouter } from 'vue-router';
import { unsetToken } from '@/components/tokenUtils';
export function logout() {
  try {
    unsetToken();
    router.push('/login');
  } catch (error) {
    handleError(error);
  }

  const router = useRouter();
  router.push({ name: 'Login' });
}