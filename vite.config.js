import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
    plugins: [vue()],
    root: resolve(__dirname, 'resources'),
    build: {
        outDir: resolve(__dirname, 'staticfiles'),
        emptyOutDir: true,
        rollupOptions: {
            input: {
                app: resolve(__dirname, 'resources/js/app.js'),
            },
        },
    },
    server: {
        port: 5173,
        strictPort: true,
    },
});
