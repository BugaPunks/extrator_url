## Why

El extractor de URLs de YouTube funciona hoy solo como script CLI (`main.py`), lo que limita su uso a personas con terminal y conocimientos técnicos. Convertirlo en una aplicación web accesible desde el navegador amplía su utilidad a cualquier usuario, manteniendo la misma lógica de extracción con `yt-dlp`.

## What Changes

- Se agrega una aplicación web (Django + Inertia.js + Vue 3) con formulario para ingresar URL/handle de un canal de YouTube.
- Nueva funcionalidad de exportación: generación de archivos .txt (único o divididos por máximo de URLs por archivo) descargables desde el navegador.
- La lógica de extracción de `main.py` se refactoriza en un servicio backend reutilizable (`services/youtube.py`).
- El CLI existente **no se elimina**; la web es una capa adicional sobre el mismo servicio.
- Sin base de datos, sin autenticación: resultados transitorios en memoria.

## Capabilities

### New Capabilities
- `channel-url-extraction`: Extraer la lista plana de videos (URLs y opcionalmente títulos) de un canal de YouTube dado su URL o handle, con manejo de errores (videos privados/borrados no detienen el proceso).
- `txt-export`: Generar y descargar archivos .txt con las URLs extraídas, en archivo único o divididos en múltiples partes según el máximo configurado, con o sin títulos.
- `web-extractor-ui`: Interfaz web con formulario de entrada, estados de carga, visualización de resultados en textarea de solo lectura y manejo amigable de errores.

### Modified Capabilities

(ninguna — no existen specs previos en `openspec/specs/`)

## Impact

- **Código nuevo**: proyecto Django (`extractor_project/`, app `extractor/`), frontend Vue 3 + Inertia (`resources/js/`), template `inertia.html`, configuración Vite.
- **Código modificado**: `main.py` se refactoriza para delegar en `extractor/services/youtube.py` (comportamiento CLI se mantiene).
- **Dependencias Python**: se agregan `Django>=4.2`, `django-inertia>=0.6` a `requirements.txt` (ya existe `yt-dlp`).
- **Dependencias Node.js**: `vue`, `@inertiajs/vue3`, `vite`, `@vitejs/plugin-vue`, `sass` en `package.json`.
- **Endpoints nuevos**: `GET /`, `POST /extraer`, `POST /exportar`.
- **Rendimiento**: extracción con `extract_flat: True` (rápido); para canales muy grandes (>5000 videos) se consideran timeout/paginación.
