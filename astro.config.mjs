import sitemap from '@astrojs/sitemap';
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://www.globalairoperations.com',
  trailingSlash: 'never',
  integrations: [sitemap()],
});
