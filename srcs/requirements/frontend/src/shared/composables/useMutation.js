import { ref } from 'vue';

function useMutation(fetchFn, options = {}) {
  const { enabled = true, onSuccess = () => {}, onError = () => {} } = options;

  const isLoading = ref(false);
  const isError = ref(false);

  const mutate = async (...args) => {
    if (!enabled) return;

    isLoading.value = true;
    isError.value = false;

    const startTime = new Date();

    try {
      const result = await fetchFn(...args);
      onSuccess(result);
    } catch (error) {
      isError.value = true;
      onError(error);
    } finally {
      const elapsedTime = new Date() - startTime;
      const remainingTime = Math.max(300 - elapsedTime, 0);

      setTimeout(() => {
        isLoading.value = false;
      }, remainingTime);
    }
  };

  return { isLoading, isError, mutate };
}

export default useMutation;
