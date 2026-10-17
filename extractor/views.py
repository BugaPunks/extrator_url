"""
Vistas de la aplicacion extractor
"""
import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET

from inertia import render as inertia_render

from .services.youtube import extraer_urls_canal
from .utils.export import generar_response_descarga


@require_GET
def index(request):
    """
    Pagina principal - formulario de extraccion

    GET /
    Renderiza el componente Extractor de Vue via Inertia.
    """
    return inertia_render(request, 'Extractor', {
        'canal': '',
        'incluir_titulos': False,
        'max_urls_por_archivo': 0,
    })


def _get_payload(request):
    """Devuelve el payload como dict, aceptando JSON o form-encoded."""
    if 'application/json' in (request.content_type or ''):
        return json.loads(request.body or b'{}')
    return request.POST


def _parse_results(raw):
    """Normaliza la lista de resultados a [ [titulo, url], ... ]."""
    if isinstance(raw, str):
        raw = json.loads(raw or '[]')
    if not isinstance(raw, list):
        raise ValueError('Los resultados deben ser una lista')

    resultados = []
    for item in raw:
        if not item:
            continue
        if isinstance(item, (list, tuple)):
            titulo = item[0] if len(item) > 0 else ''
            url = item[1] if len(item) > 1 else ''
        elif isinstance(item, dict):
            titulo = item.get('titulo', '')
            url = item.get('url', '')
        else:
            raise ValueError('Formato de resultado inválido')
        if url:
            resultados.append((titulo or '', url))
    return resultados


@require_POST
def extraer(request):
    """
    Endpoint para extraer URLs de un canal

    POST /extraer

    Body JSON:
    {
        "canal": "@tucanal o URL",
        "incluir_titulos": true/false
    }

    Returns:
        JSON con resultados o error
    """
    try:
        data = _get_payload(request)
        canal = str(data.get('canal', '')).strip()
        incluir_titulos = str(data.get('incluir_titulos', 'false')).lower() in ('true', '1', 'on', 'si', 's')
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({
            'error': 'Datos inválidos: se esperaba JSON',
            'results': [],
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error al procesar la solicitud: {str(e)}',
            'results': [],
        }, status=400)

    if not canal:
        return JsonResponse({
            'error': 'El canal es obligatorio',
            'results': [],
        }, status=400)

    # Se extraen TODAS las URLs del canal. La division en archivos es una
    # decision de exportacion y no debe limitar la extraccion.
    urls, error = extraer_urls_canal(canal, incluir_titulos)

    if error:
        return JsonResponse({
            'error': error,
            'results': [],
            'canal': canal,
            'incluir_titulos': incluir_titulos,
        }, status=400)

    return JsonResponse({
        'results': urls,
        'error': None,
        'success_message': f'Se extrajeron {len(urls)} URLs correctamente',
        'canal': canal,
        'incluir_titulos': incluir_titulos,
    })


@require_POST
def exportar(request):
    """
    Endpoint para exportar URLs a archivo

    POST /exportar

    Body JSON (o form):
        results: lista [[titulo, url], ...] o JSON string
        incluir_titulos: true/false
        max_urls_por_archivo: numero
        dividido: true/false

    Returns:
        FileResponse con el archivo .txt o .zip
    """
    try:
        payload = _get_payload(request)
        urls = _parse_results(payload.get('results'))
        incluir_titulos = str(payload.get('incluir_titulos', 'false')).lower() in ('true', '1', 'on', 'si', 's')
        max_urls_por_archivo = int(payload.get('max_urls_por_archivo', 0) or 0)
        dividido = str(payload.get('dividido', 'false')).lower() in ('true', '1', 'on', 'si', 's')

        if not urls:
            return JsonResponse({
                'error': 'No hay URLs para exportar',
            }, status=400)

        return generar_response_descarga(
            urls,
            incluir_titulos=incluir_titulos,
            max_urls_por_archivo=max_urls_por_archivo,
            dividido=dividido,
        )

    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Resultados inválidos: formato JSON incorrecto',
        }, status=400)
    except ValueError as e:
        return JsonResponse({
            'error': str(e),
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error al exportar: {str(e)}',
        }, status=500)
