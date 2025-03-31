export const modes = {
  passive: () => [],

  // Validate on blur only
  lazy: () => ['blur'],

  // Validate on input and blur
  aggressive: () => ['input', 'blur'],

  // Validate on blur always, and on input if there's already an error
  eager: ({ errorMessage }) => {
    return errorMessage.value ? ['input', 'blur'] : ['blur'];
  },
};
