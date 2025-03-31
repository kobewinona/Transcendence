import { ref, watchEffect } from 'vue';

function useQuery({ fetchFn, params = {}, options = {} }) {
  const {
    enabled = true,
    select = (res) => res,
    onSuccess = () => {},
    onError = () => {},
    onSettled = () => {},
  } = options;

  const data = ref(null);
  const isLoading = ref(false);
  const isError = ref(false);
  const error = ref(null);

  const fetchData = async () => {
    isLoading.value = true;
    isError.value = false;
    error.value = null;

    const startTime = new Date();

    try {
      const result = await fetchFn({ params });
      data.value = select(result);
      onSuccess(result);
    } catch (err) {
      isError.value = true;
      error.value = err;
      onError(err);
    } finally {
      const elapsedTime = new Date() - startTime;
      const remainingTime = Math.max(300 - elapsedTime, 0);

      setTimeout(() => {
        isLoading.value = false;
      }, remainingTime);

      onSettled();
    }
  };

  if (enabled) {
    watchEffect(fetchData);
  }

  const refetch = async () => {
    await fetchData();
  };

  return { data, isLoading, isError, error, refetch };
}

export default useQuery;
