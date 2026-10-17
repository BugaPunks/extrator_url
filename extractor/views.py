"""
Vistas de la aplicacion extractor
"""
import json
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from .services.youtube import extraer_urls_canal, normalizar_url_canal
from .utils.export import generar_response_descarga


@require_GET
def index(request):
    """
    Pagina principal - formulario de extraccion
    
    GET /
    Renderiza la pagina principal con el componente Extractor de Vue
    """
    return render(request, 'app.html', {
        'page': json.dumps({
            'component': 'Extractor',
            'props': {
                'canal': '',
                'incluir_titulos': False,
                'max_urls_por_archivo': 0,
                'results': [],
                'error': None,
                'success_message': None,
            },
            'url': '/',
            'version': None,
        }),
    })


@require_POST
@csrf_exempt
def extraer(request):
    """
    Endpoint para extraer URLs de un canal
    
    POST /extraer
    
    Body JSON:
    {
        "canal": "@midudev o URL",
        "incluir_titulos": true/false,
        "max_urls_por_archivo": 0
    }
    
    Returns:
        JSON con resultados o error
    """
    try:
        # Parsear body JSON
        data = json.loads(request.body) if request.body else {}
        canal = data.get('canal', '').strip()
        incluir_titulos = bool(data.get('incluir_titulos', False))
        max_urls_por_archivo = int(data.get('max_urls_por_archivo', 0))
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Datos inválidos: se esperaba JSON',
            'results': []
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error al procesar la solicitud: {str(e)}',
            'results': []
        }, status=400)
    
    # Validar canal
    if not canal:
        return JsonResponse({
            'error': 'El canal es obligatorio',
            'results': []
        }, status=400)
    
    # Extraer URLs
    urls, error = extraer_urls_canal(canal, incluir_titulos, max_urls_por_archivo if max_urls_por_archivo > 0 else 0)
    
    if error:
        return JsonResponse({
            'error': error,
            'results': [],
            'canal': canal,
            'incluir_titulos': incluir_titulos,
            'max_urls_por_archivo': max_urls_por_archivo
        }, status=400)
    
    # Devolver resultados
    return JsonResponse({
        'results': urls,
        'error': None,
        'success_message': f'Se extrajeron {len(urls)} URLs correctamente',
        'canal': canal,
        'incluir_titulos': incluir_titulos,
        'max_urls_por_archivo': max_urls_por_archivo
    })


@require_GET
def exportar(request):
    """
    Endpoint para exportar URLs a archivo
    
    GET /exportar
    
    Query params:
        results: JSON string de lista de tuplas (titulo, url)
        incluir_titulos: true/false
        max_urls_por_archivo: numero
        dividido: true/false
        
    Returns:
        FileResponse con el archivo .txt o .zip
    """
    try:
        results_str = request.GET.get('results', '')
        incluir_titulos = request.GET.get('incluir_titulos', 'false').lower() == 'true'
        max_urls_por_archivo = int(request.GET.get('max_urls_por_archivo', 0))
        dividido = request.GET.get('dividido', 'false').lower() == 'true'
        
        if not results_str:
            return JsonResponse({
                'error': 'No hay resultados para exportar'
            }, status=400)
        
        # Parsear resultados
        urls = json.loads(results_str)
        
        if not urls or len(urls) == 0:
            return JsonResponse({
                'error': 'No hay URLs para exportar'
            }, status=400)
        
        # Generar respuesta de descarga
        response = generar_response_descarga(
            urls, 
            incluir_titulos=incluir_titulos,
            max_urls_por_archivo=max_urls_por_archivo,
            dividido=dividido
        )
        
        return response
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Resultados inválidos: formato JSON incorrecto'
        }, status=400)
    except ValueError as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': f'Error al exportar: {str(e)}'
        }, status=500)
