const mapRange = (value, inMin, inMax, outMin, outMax) => {
  return ((value - inMin) / (inMax - inMin)) * (outMax - outMin);
};

export default mapRange;
