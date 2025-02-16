import { cloneDeep } from 'lodash';
import { reactive } from 'vue';

function useForm({ initialValues = {}, mode = 'onChange' } = {}) {
  const values = reactive(cloneDeep(initialValues));
  const errors = reactive({});

  const getValueByPath = (obj, path) => {
    return path
      .replace(/\[(\w+)\]/g, '.$1')
      .split('.')
      .reduce((acc, key) => acc && acc[key], obj);
  };

  const setValueByPath = (obj, path, value) => {
    const keys = path.replace(/\[(\w+)\]/g, '.$1').split('.');
    const lastKey = keys.pop();
    const target = keys.reduce((acc, key) => acc && acc[key], obj);

    if (target && lastKey) {
      target[lastKey] = value;
    }
  };

  const setValue = (field, value) => {
    setValueByPath(values, field, value);

    if (mode === 'onChange') {
      validateField(field);
    }
  };

  const getValues = (path) => {
    if (path) {
      return getValueByPath(values, path);
    }
    return { ...values };
  };

  const reset = () => {
    Object.assign(values, cloneDeep(initialValues));
    Object.keys(errors).forEach((key) => {
      delete errors[key];
    });
  };

  const validateField = (field) => {
    console.debug('field', field);
    // TODO implement validation logic
  };

  const validateAll = () => {
    let isValid = true;
    Object.keys(values).forEach((field) => {
      validateField(field);
      if (errors[field]) {
        isValid = false;
      }
    });
    return isValid;
  };

  const handleSubmit = (onSubmit, onError) => () => {
    if (validateAll()) {
      onSubmit(values);
    } else if (onError) {
      onError({ ...errors });
    }
  };

  return {
    values,
    errors,
    setValue,
    getValues,
    reset,
    handleSubmit,
  };
}

export default useForm;
