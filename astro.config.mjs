// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://hrialan.github.io',
  base: '/webcam-saint-malo/',
  output: 'static',
  build: {
    assets: 'assets',
  },
});
