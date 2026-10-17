## Context

El proyecto es hoy un script CLI (`main.py`) que usa `yt-dlp` para extraer URLs de videos de un canal de YouTube y guardarlas en .txt. El objetivo es convertirlo en una web app (Django + Inertia.js + Vue 3) sin base de datos ni autenticación, manteniendo el CLI funcional refactorizando la lógica de extracción en un servicio compartido.

Stakeholders: usuarios finales sin conocimientos técnicos que quieren extraer URLs de canales de YouTube desde el navegador.

## Goals / Non-Goals

**Goals:**
- Interfaz web con formulario (URL/handle del canal, opción de títulos, máximo de URLs por archivo).
- Extracción de videos con `yt-dlp` (`extract_flat: True`), tolerante a videos privados/borrados.
- Descarga de .txt único o divididos (`urls_videos_parte_N.txt`).
- Estados de carga y manejo de errores amigable en la UI.
- Refactorizar la lógica de `main.py` en `extractor/services/youtube.py` reutilizable por CLI y web.

**Non-Goals:**
- Autenticación de usuarios.
- Persistencia en base de datos (resultados solo en memoria).
- Descarga o procesamiento de contenido de video.
- Paginación de resultados para canales gigantes (se deja como mejora futura; solo timeout).
- Cambiar el comportamiento del CLI existente.

## Decisions

1. **Stack: Django + Inertia.js + Vue 3** — Inertia permite escribir páginas como componentes Vue sin API REST dedicada ni estado de sesión del lado del servidor. Alternativa descartada: SPA + DRF (más complejidad: serialización, CORS, doble routing) y Flask + HTMX (menos integración con Vue 3 que ya se desea).
2. **Extracción en memoria, sin BD** — Los resultados viajan como props de Inertia en el POST `/extraer` y se reenvían al POST `/exportar`. Alternativa descartada: sesión/cache de servidor (complejidad innecesaria para uso single-shot).
3. **Exportación server-side con `FileResponse`** — `/exportar` recibe los datos + opciones y responde con el archivo (o ZIP si hay múltiples partes). Alternativa descartada: generación pura en cliente con Blob (perdemos los nombres `parte_N.txt` consistentes y la lógica queda en dos lugares).
4. **Normalización de URL/handle en el servicio** — `@handle` → `https://www.youtube.com/@handle/videos`; URLs sin `/videos` se les agrega. Centralizado en `youtube.py` para que CLI y web compartan la lógica.
5. **Inertia v3 con template `inertia.html`** — `<script data-page="app" type="application/json">{{ page|safe }}</script>`, CSRF con `xsrfCookieName: "csrftoken"` / `xsrfHeaderName: "X-CSRFToken"`, flash messages vía Django messages framework.
6. **Vite como bundler** — `@vitejs/plugin-vue`, sass, entry `resources/js/app.js`, manifest para `django-vite`-style loading (o script tags condicionales en dev/prod).

## Risks / Trade-offs

- [Resultados en memoria se pierden al recargar la página] → Aceptado: UX single-shot; la UI indica que se deben descargar antes de salir.
- [Canales muy grandes (>5000 videos) pueden tardar o agotar memoria] → Timeout configurado en `yt-dlp` y mensaje de progreso; paginación queda fuera de alcance.
- [Cambio en `main.py` puede romper el CLI] → Refactor mínimo: mover lógica al servicio y dejar `main.py` como wrapper; prueba manual del CLI.
- [Respuesta síncrona de `/extraer` bloquea el worker durante la extracción] → Aceptado para v1 (extracción flat es rápida); si escala, migrar a tarea asíncrona.
- [Videos privados/borrados] → `extract_flat` con manejo de errores por ítem: se omiten y se reporta el conteo, sin abortar.

## Migration Plan

1. Crear estructura Django/Inertia/Vite en paralelo al CLI existente.
2. Extraer lógica a `services/youtube.py` y adaptar `main.py` para usarla (CLI sigue funcionando).
3. Desplegar web app con `manage.py runserver` + `npm run dev` (dev) o build estático (prod).
4. Rollback: revertir cambios; el CLI original sigue disponible en git history.

## Open Questions

- ¿Incluir ZIP automático cuando hay múltiples archivos divididos, o enlaces de descarga individuales? (Se propone ZIP.)
- ¿Nombre del archivo único: `urls_videos.txt` (consistente con el CLI) o con timestamp?
