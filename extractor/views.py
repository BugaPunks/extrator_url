"""
Vistas de la aplicacion extractor
"""
import json
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from .services.youtube import extraer_urls_canal
from .utils.export import generar_response_descarga


def index(request):
    """Pagina principal - formulario de extraccion"""
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


def extraer(request):
    """Endpoint para extraer URLs de un canal"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)
    
    try:
        data = json.loads(request.body) if request.body else {}
        canal = data.get('canal', '').strip()
        incluir_titulos = data.get('incluir_titulos', False)
    except Exception:
        return JsonResponse({'error': 'Datos invalidos'}, status=400)
    
    if not canal:
        return JsonResponse({'error': 'El canal es obligatorio'}, status=400)
    
    # Extraer URLs
    urls, error = extraer_urls_canal(canal, incluir_titulos)
    
    if error:
        return JsonResponse({'error': error, 'results': []}, status=400)
    
    # Devolver resultados
    return JsonResponse({
        'results': urls,
        'error': None,
        'success_message': f'Se extrajeron {len(urls)} URLs correctamente',
    })


def exportar(request):
    """Endpoint para exportar URLs a archivo"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Metodo no permitido'}, status=405)
    
    try:
        results_str = request.GET.get('results', '')
        incluir_titulos = request.GET.get('incluir_titulos', 'false').lower() == 'true'
        max_urls_por_archivo = int(request.GET.get('max_urls_por_archivo', 0))
        dividido = request.GET.get('dividido', 'false').lower() == 'true'
        
        if not results_str:
            return JsonResponse({'error': 'No hay resultados para exportar'}, status=400)
        
        # Parsear resultados
        urls = json.loads(results_str)
        
        # Generar respuesta de descarga
        response = generar_response_descarga(
            urls, 
            incluir_titulos=incluir_titulos,
            max_urls_por_archivo=max_urls_por_archivo,
            dividido=dividido
        )
        
        return response
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Resultados invalidos'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error al exportar: {str(e)}'}, status=500)
