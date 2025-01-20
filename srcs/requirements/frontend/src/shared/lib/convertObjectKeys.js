const convertObjectKeys = (obj, convertFn) => {
  if (Array.isArray(obj)) {
    return obj.map((item) => convertObjectKeys(item, convertFn));
  } else if (obj !== null && typeof obj === 'object') {
    return Object.entries(obj).reduce((acc, [key, value]) => {
      const convertedKey = convertFn(key);
      acc[convertedKey] = convertObjectKeys(value, convertFn);
      return acc;
    }, {});
  }
  return obj;
};

export default convertObjectKeys;
