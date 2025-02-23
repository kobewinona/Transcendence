const isVueComponent = (value) => {
  return typeof value === 'function' || (typeof value === 'object' && value !== null);
};

export default isVueComponent;
