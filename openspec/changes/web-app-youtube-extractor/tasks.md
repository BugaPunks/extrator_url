## 1. Setup — Django + Inertia base

- [x] 1.1 Crear proyecto Django (`extrator_url/extractor_project/`) y app `extractor/`, agregar dependencias Python (`Django>=4.2`, `django-inertia>=0.6`) a `requirements.txt`
- [x] 1.2 Configurar `django-inertia` en `settings.py` (app instalada, middleware, template `app.html` con `<script data-page="app" type="application/json">{{ page|safe }}</script>`)
- [x] 1.3 Configurar Vite + Vue 3 + `@inertiajs/vue3` (`vite.config.js`, `package.json`, `resources/js/app.js` con `createInertiaApp` y CSRF `xsrfCookieName: "csrftoken"` / `xsrfHeaderName: "X-CSRFToken"`)
- [x] 1.4 Configurar rutas raíz en `extractor_project/urls.py` apuntando a la app `extractor`

## 2. Backend — Servicio de extracción

- [x] 2.1 Crear `extractor/services/youtube.py` con la lógica extraída de `main.py`: normalización de handle/URL (agregar `/videos`), `extract_flat: True`, opción de títulos
- [x] 2.2 Implementar tolerancia a videos privados/borrados (omitir ítems, continuar) y errores amigables para canal inválido/sin videos/fallo de red
- [x] 2.3 Adaptar `main.py` para delegar en el servicio (CLI sigue funcionando igual) y verificar manualmente

## 3. Backend — Exportación y vistas

- [x] 3.1 Crear `extractor/utils/export.py`: generación de archivo único y divididos (`urls_videos_parte_N.txt`) con formato `URL` o `Título - URL`
- [x] 3.2 Implementar `extractor/views.py`: `GET /` (render Inertia de `Extractor`), `POST /extraer` (extraer y retornar resultados como props), `GET /exportar` (generar `FileResponse`, ZIP si hay múltiples partes)
- [x] 3.3 Configurar `extractor/urls.py` con las rutas `/`, `/extraer`, `/exportar`

## 4. Frontend — Componentes Vue

- [x] 4.1 Crear `resources/js/Pages/Extractor.vue` con formulario (input canal, checkbox títulos, input máx. URLs por archivo, botón "Extraer URLs") y manejo de estado (loading, results, errors)
- [x] 4.2 Crear componentes `InputChannel.vue`, `ResultsArea.vue` (textarea solo lectura), `ExportButtons.vue` ("Descargar .txt único", "Descargar .txt divididos"), `LoadingSpinner.vue`
- [x] 4.3 Implementar estados de carga: spinner + "Obteniendo lista de videos...", botones deshabilitados durante la extracción
- [x] 4.4 Implementar descarga de archivos desde los botones de exportación (FileResponse del endpoint `/exportar`)
- [x] 4.5 Agregar estilos responsive (`resources/sass/app.scss`) y manejo de errores amigable en la UI

## 5. Integración y Testing

- [x] 5.1 Probar extracción con varios canales (handle, URL completa, canal grande, canal inválido)
- [x] 5.2 Probar exportación: archivo único, divididos (última parte con menos URLs), con y sin títulos
- [x] 5.3 Probar manejo de errores end-to-end: canal inexistente, videos privados/borrados, error de red
- [ ] 5.4 Verificar build de producción de Vite y carga de assets desde Django, y que el CLI original sigue operativo
