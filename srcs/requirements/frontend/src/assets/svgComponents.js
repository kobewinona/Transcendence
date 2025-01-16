const svgFiles = import.meta.glob('./icons/**/*.svg', { eager: true });

export const svgComponents = {};

const nameCounts = {}; // Keep track of how many times a name has been used

Object.entries(svgFiles).forEach(([filePath, component]) => {
  // Extract the file name (e.g., `Game console.svg`)
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
