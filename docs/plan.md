# Plan de Implementación: Extractor de URLs de YouTube - Web App

## Resumen
Convertir el script CLI actual (`main.py`) en una aplicación web usando Django + Inertia.js + Vue 3 que permita extraer URLs de videos de un canal de YouTube y exportarlas a archivos .txt con opciones de división.

## Requisitos Funcionales

### 1. Interfaz de Usuario
- **Pantalla principal**: Formulario con:
  - Textbox/Input para URL o handle del canal de YouTube (ej: `@tucanal`, `https://www.youtube.com/@tucanal`)
  - Checkbox: "Incluir títulos de videos" (desmarcado por defecto)
  - Input numérico: "Máx. URLs por archivo" (opcional, para dividir en múltiples .txt)
  - Botón: "Extraer URLs"
- **Área de resultados**: Textarea de solo lectura que muestra las URLs extraídas (y títulos si se marcó la opción)
- **Botones de exportación**:
  - "Descargar .txt único"
  - "Descargar .txt divididos" (si se configuró máximo por archivo)

### 2. Funcionalidad de Extracción
- Usar `yt-dlp` (igual que el script actual)
- Procesar la URL del canal (normalizar handles, agregar `/videos` si falta)
- Extraer lista plana de videos (`extract_flat: True`)
- Manejar errores: videos privados/borrados continuar sin detener
- Retornar lista de tuplas `(titulo, url)` o solo `url` según opción

### 3. Exportación a .txt
- **Archivo único**: Todas las URLs en un archivo
- **Archivos divididos**: Si se especifica "Máx. URLs por archivo" > 0, crear múltiples archivos:
  - `urls_videos_parte_1.txt`, `urls_videos_parte_2.txt`, etc.
  - Cada archivo con el número configurado de URLs (excepto el último)
- Formato por línea: `URL` o `Título - URL` según opción de títulos

### 4. Estados de Carga
- Loading spinner/message mientras `yt-dlp` procesa
- Mensaje de progreso: "Obteniendo lista de videos..."
- Deshabilitar botones durante extracción

## Requisitos No Funcionales
- Sin base de datos (resultados solo en memoria/transitorios)
- Sin autenticación
- Responsive design
- Manejo de errores amigable (UI)

## Arquitectura Técnica

### Backend (Django)
```
extractor/
├── views.py          # Vista principal que maneja POST de extracción
├── urls.py           # Rutas Django
├── services/
│   └── youtube.py    # Lógica de extracción (refactor de main.py)
├── utils/
│   └── export.py     # Utilidades para generar .txt (único y divididos)
```

### Frontend (Vue 3 + Inertia)
```
resources/js/
├── Pages/
│   └── Extractor.vue     # Componente principal
├── Components/
│   ├── InputChannel.vue  # Input para URL del canal
│   ├── ResultsArea.vue   # Textarea de resultados
│   ├── ExportButtons.vue # Botones de descarga
│   └── LoadingSpinner.vue
├── app.js                # Entry point Inertia
└── sass/app.scss         # Estilos
```

### Flujo de Datos
1. Usuario llena formulario → POST a `/extraer`
2. Django View llama `youtube_service.extraer_urls_canal()`
3. Servicio retorna lista de videos
4. View retorna JSON con datos a Inertia (props)
5. Vue actualiza UI con resultados
6. Usuario click "Descargar" → POST a `/exportar` con datos + opciones
7. Django genera .txt(s) y retorna `FileResponse` para descarga

## Endpoints API

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Página principal (Inertia render) |
| POST | `/extraer` | Extraer URLs del canal, retorna JSON con resultados |
| POST | `/exportar` | Generar y descargar archivo(s) .txt |

## Pasos de Implementación

### Fase 1: Configuración Base Django + Inertia
1. Crear proyecto Django (`django-admin startproject`)
2. Configurar `django-inertia` en `settings.py`
3. Crear app `extractor`
4. Configurar template base `inertia.html` (formato v3)
5. Configurar `createInertiaApp` con CSRF de Django

### Fase 2: Backend - Lógica de Extracción
1. Mover lógica de `main.py` a `services/youtube.py`
2. Crear `utils/export.py` para generación de .txt
3. Implementar vistas en `views.py`
4. Configurar URLs

### Fase 3: Frontend - Vue Components
1. Configurar Vite + Vue 3 + `@inertiajs/vue3`
2. Crear componentes UI
3. Manejar estado: loading, results, errors
4. Implementar descarga de archivos (blob)

### Fase 4: Integración y Testing
1. Probar extracción con varios canales
2. Probar exportación único y dividido
3. Manejo de errores (canal inválido, sin videos, red)
4. Estilos y UX pulido

## Dependencias

### Python (requirements.txt)
```
Django>=4.2
django-inertia>=0.6
yt-dlp>=2026.1.1
```

### Node.js (package.json)
```json
{
  "dependencies": {
    "@inertiajs/vue3": "^3.9.1",
    "vue": "^3.4.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0",
    "sass": "^1.70.0"
  }
}
```

## Configuración Inertia v3 (Importante)
Según la documentación proporcionada:
- Usar template `inertia.html` con `<script data-page="app" type="application/json">{{ page|safe }}</script>`
- Configurar CSRF: `xsrfCookieName: "csrftoken"`, `xsrfHeaderName: "X-CSRFToken"`
- Flash messages via Django messages framework

## Estructura de Archivos Final
```
extrator_url/
├── manage.py
├── requirements.txt
├── package.json
├── vite.config.js
├── extractor_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── extractor/
│   ├── __init__.py
│   ├── views.py
│   ├── urls.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── youtube.py
│   └── utils/
│       ├── __init__.py
│       └── export.py
├── templates/
│   └── inertia.html
├── resources/
│   ├── js/
│   │   ├── app.js
│   │   ├── Pages/Extractor.vue
│   │   └── Components/
│   └── sass/app.scss
└── static/ (generado por Vite)
```

## Consideraciones de Rendimiento
- `yt-dlp` con `extract_flat: True` es rápido (no descarga videos)
- Para canales muy grandes (>5000 videos), considerar timeout y paginación
- La división en archivos se hace en memoria, eficiente para <10k URLs

## Próximos Pasos
Una vez aprobado este plan, procederé a implementar cada fase secuencialmente.