import { useRouter } from 'vue-router';

import { unsetToken } from '@/components/tokenUtils';
import { useAuth} from '@/pages/LoginPage/components/composables/useAuth'
export function logout() {
  const { handleError} = useAuth()
  try {
    unsetToken();
    router.push('/login');
  } catch (error) {
    handleError(error);
  }

  const router = useRouter();
  router.push({ name: 'Login' });
}