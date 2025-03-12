import { cloneDeep } from 'lodash';
import { reactive } from 'vue';

// Utils
function getValueByPath(obj, path) {
  return path
    .replace(/\[(\w+)\]/g, '.$1')
    .split('.')
    .reduce((acc, key) => acc && acc[key], obj);
}

function setByPath(obj, path, value) {
  const keys = path.replace(/\[(\w+)\]/g, '.$1').split('.');
  const lastKey = keys.pop();
  const target = keys.reduce((acc, key) => acc && acc[key], obj);

  if (target && lastKey) {
    target[lastKey] = value;
  }
}

function useForm({ initialValues = {}, mode = 'onChange' } = {}) {
  const values = reactive(cloneDeep(initialValues));
  const errors = reactive({});
  const rulesMap = reactive({});

  // Methods
  const setValue = (field, value) => {
    setByPath(values, field, value);
  };

  const getValues = (path) => {
    if (path) return getValueByPath(values, path);
    return { ...values };
  };

  const setRules = (field, rules) => {
    rulesMap[field] = rules;
  };

  const setError = (field, errorMessage) => {
    setByPath(errors, field, errorMessage);
  };

  const reset = () => {
    Object.assign(values, cloneDeep(initialValues));
    Object.keys(errors).forEach((key) => delete errors[key]);
  };

  // Validation
  const validateField = (field) => {
    const inputValue = getValueByPath(values, field);
    const rules = rulesMap[field];
    if (!rules) return;

    let errorMessage = '';

    if (rules.required && !inputValue) {
      errorMessage = typeof rules.required === 'string' ? rules.required : 'This field is required';
    } else if (rules.minLength && inputValue.length < rules.minLength.value) {
      errorMessage = rules.minLength.message || `Minimum length is ${rules.minLength.value}`;
    } else if (rules.maxLength && inputValue.length > rules.maxLength.value) {
      errorMessage = rules.maxLength.message || `Maximum length is ${rules.maxLength.value}`;
    } else if (rules.pattern && !rules.pattern.value.test(inputValue)) {
      errorMessage = rules.pattern.message || 'Invalid format';
    }

    if (errorMessage) {
      setError(field, errorMessage);
    } else {
      setError(field, '');
    }
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

  // Master controls
  const handleBlur = (field) => {
    if (mode === 'onBlur') {
      validateField(field);
    }
  };

  const handleChange = (field, value) => {
    if (mode === 'onChange') {
      validateField(field);
    }

    setValue(field, value);
  };

  const handleSubmit = (onSubmit, onError) => () => {
    if (validateAll()) {
      onSubmit(values);
    } else if (onError) {
      onError({ ...errors });
    }
  };

  return {
    mode,
    values,
    errors,
    setValue,
    getValues,
    setRules,
    setError,
    reset,
    handleBlur,
    handleChange,
    handleSubmit,
  };
}

export default useForm;
