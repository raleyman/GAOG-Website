import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://www.globalairoperations.com',
  trailingSlash: 'never',
  integrations: [sitemap()],
});
