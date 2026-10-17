import { createApp, h } from 'vue';
import { createInertiaApp } from '@inertiajs/vue3';
import '../css/app.css';

const pages = {
    Extractor: () => import('./Pages/Extractor.vue'),
};

createInertiaApp({
    resolve: name => pages[name](),
    setup({ el, App, props, plugin }) {
        createApp({ render: () => h(App, props) })
            .use(plugin)
            .mount(el);
    },
    progress: {
        color: '#4B5563',
    },
    title: title => `${title} - Extractor de URLs de YouTube`,
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
});
