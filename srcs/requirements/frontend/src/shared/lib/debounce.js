let debounceTimeoutId = null;

const debounce = (fn, delay = 300) => {
  return (...args) => {
    clearTimeout(debounceTimeoutId);
    debounceTimeoutId = setTimeout(() => {
      fn(...args);
    }, delay);
  };
};

export default debounce;
