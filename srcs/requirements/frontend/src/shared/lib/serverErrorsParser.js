export function parseValidationErrors(responseData) {
  if (!responseData || typeof responseData !== 'object') return;

  const flatErrors = {};

  for (const [field, value] of Object.entries(responseData)) {
    if (Array.isArray(value)) {
      value.forEach((item, index) => {
        if (typeof item === 'object') {
          for (const [subField, message] of Object.entries(item)) {
            if (typeof message === 'string') {
              flatErrors[`${field}.${index}.${subField}`] = message;
            }
          }
        }
      });
    } else if (typeof value === 'string') {
      flatErrors[field] = value;
    }
  }

  return Object.keys(flatErrors).length ? flatErrors : undefined;
}

export function tryParseAnyError(error, t) {
  if (!error) return t('unknown_error');

  if (error.response) {
    const { data, statusText, status, headers } = error.response;

    // Check if response contains HTML (Django debug error pages)
    if (
      headers?.['content-type']?.includes('text/html') ||
      (typeof data === 'string' && data.includes('<html'))
    ) {
      console.error('Django returned an HTML error page. Check server logs.');
      return `Server Error ${status}: ${statusText || t('unknown_error')}`;
    }

    if (data) {
      if (typeof data === 'string') {
        return data.length > 500 ? data.slice(0, 500) + '...' : data;
      }
      if (data.detail) {
        return data.detail;
      }
      if (data.message) {
        return data.message;
      }
      if (data.error) {
        return data.error;
      }
      if (Array.isArray(data)) {
        return data.join(', ');
      }
      if (typeof data === 'object') {
        const firstKey = Object.keys(data)[0];
        if (firstKey && typeof data[firstKey] === 'string') {
          return data[firstKey];
        }
        if (firstKey && Array.isArray(data[firstKey])) {
          return data[firstKey].join(', ');
        }
      }
    }

    return statusText || `Error ${status}`;
  }

  if (error.message) {
    return error.message.length > 500 ? error.message.slice(0, 500) + '...' : error.message;
  }

  return t('unknown_error');
}
