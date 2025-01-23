const svgFiles = import.meta.glob('/src/assets/icons/**/*.svg', { eager: true });

const svgComponents = {};

const nameCounts = {};

Object.entries(svgFiles).forEach(([filePath, component]) => {
  const rawName = filePath
    .split('/')
    .pop()
    .replace(/\.svg$/, '');

  const nameWithoutPrefix = rawName.replace(/^\d+-/, '').replace(/\s+/g, '-');

  let componentName =
    nameWithoutPrefix
      .split('-')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join('') + 'Icon';

  if (nameCounts[componentName]) {
    nameCounts[componentName] += 1;
    componentName += nameCounts[componentName];
  } else {
    nameCounts[componentName] = 1;
  }

  svgComponents[componentName] = component.default || component;
});

export default svgComponents;
