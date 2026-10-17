"""
Template tags para cargar los assets generados por Vite.

Usa el manifest que genera `npm run build` (build.manifest: true), de modo que
la plantilla no necesita conocer los nombres con hash de los archivos.

Uso:
    {% load vite %}
    {% vite_asset 'resources/js/app.js' %}
"""
import json
from pathlib import Path

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()

_manifest_cache = None
_MANIFEST_CANDIDATES = (
    Path('.vite') / 'manifest.json',
    Path('manifest.json'),
)


def _get_manifest():
    global _manifest_cache
    if _manifest_cache is not None:
        return _manifest_cache

    static_dir = Path(settings.BASE_DIR) / 'static'
    for relative in _MANIFEST_CANDIDATES:
        candidate = static_dir / relative
        if candidate.exists():
            with candidate.open(encoding='utf-8') as fh:
                _manifest_cache = json.load(fh)
            return _manifest_cache

    _manifest_cache = {}
    return _manifest_cache


def _manifest_key(entry):
    """Normaliza la ruta de entrada al key usado por Vite (relativo al root)."""
    key = str(entry).replace('\\', '/')
    if key.startswith('resources/'):
        key = key[len('resources/'):]
    return key


@register.simple_tag
def vite_asset(entry):
    """Renderiza los <link>/<script> del entry indicado usando el manifest."""
    chunk = _get_manifest().get(_manifest_key(entry))

    if not chunk:
        return format_html(
            '<!-- vite: no se encontró "{}" en el manifest. Ejecuta `npm run build`. -->',
            entry,
        )

    html = []
    for css_href in chunk.get('css', []):
        html.append(f'<link rel="stylesheet" href="{static(css_href)}">')

    file_href = chunk.get('file')
    if file_href:
        if file_href.endswith('.css'):
            html.append(f'<link rel="stylesheet" href="{static(file_href)}">')
        else:
            html.append(f'<script type="module" src="{static(file_href)}"></script>')

    return mark_safe('\n'.join(html))
