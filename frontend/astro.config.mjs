import { defineConfig } from 'astro/config';
import preact from '@astrojs/preact';

export default defineConfig({
  output: 'static',
  devToolbar: { enabled: false },
  vite: {
    server: {
      proxy: {
        '/api': 'http://localhost:8000'
      }
    }
  },
  integrations: [preact()]
});
