import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { resolve } from 'path';

export default defineConfig({
    plugins: [vue()],
    base: '/static/',
    root: resolve(import.meta.dirname, 'resources'),
    build: {
        outDir: resolve(import.meta.dirname, 'static'),
        emptyOutDir: true,
        manifest: true,
        rollupOptions: {
            input: {
                app: resolve(import.meta.dirname, 'resources/js/app.js'),
            },
        },
    },
    server: {
        port: 5173,
        strictPort: true,
    },
});
