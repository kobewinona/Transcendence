import _ from 'lodash';

function isDeepEmpty(obj) {
  if (!_.isObject(obj)) {
    return _.isNil(obj) || obj === '';
  }

  return _.every(obj, (value) => isDeepEmpty(value));
}

export default isDeepEmpty;
