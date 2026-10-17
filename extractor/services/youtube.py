"""
Servicio de extraccion de URLs de YouTube
"""
import yt_dlp
from typing import List, Tuple, Optional


class ErrorExtraccion(Exception):
    """Error personalizado para problemas de extraccion"""
    pass


def normalizar_url_canal(canal_input: str) -> str:
    """
    Normaliza la entrada del usuario para asegurar un formato valido de YouTube
    apuntando a la seccion de videos.
    
    Args:
        canal_input: URL, handle o identificador del canal
        
    Returns:
        URL normalizada del canal con la pestana /videos
        
    Examples:
        >>> normalizar_url_canal("@tucanal")
        'https://www.youtube.com/@tucanal/videos'
        >>> normalizar_url_canal("tucanal")
        'https://www.youtube.com/@tucanal/videos'
        >>> normalizar_url_canal("https://www.youtube.com/@tucanal")
        'https://www.youtube.com/@tucanal/videos'
    """
    url = canal_input.strip().rstrip('/')
    
    # Si ingresaron solo el handle (ej: @tucanal o tucanal)
    if url.startswith('@'):
        url = f"https://www.youtube.com/{url}"
    elif not url.startswith('http://') and not url.startswith('https://'):
        if 'youtube.com' in url:
            url = f"https://{url}"
        else:
            url = f"https://www.youtube.com/@{url}"

    # Si no especifica una pestana (/videos, /shorts, /streams, etc.), agregamos /videos
    pestanas = ('/videos', '/shorts', '/streams', '/playlists', '/featured')
    if not any(url.endswith(p) for p in pestanas):
        url = f"{url}/videos"
        
    return url


def extraer_urls_canal(channel_url: str, incluir_titulos: bool = False, max_urls: int = 0) -> Tuple[Optional[List[Tuple[str, str]]], Optional[str]]:
    """
    Extrae URLs de videos de un canal de YouTube.
    
    Args:
        channel_url: URL o handle del canal
        incluir_titulos: Si True, devuelve tuplas (titulo, url), sino solo urls
        max_urls: Maximo de URLs a extraer (0 = todos)
        
    Returns:
        Tupla de (lista_de_resultados, error)
        - lista_de_resultados: Lista de tuplas (titulo, url) o None si hay error
        - error: Mensaje de error o None si tuvo exito
        
    Raises:
        ErrorExtraccion: Si hay un error critico de configuracion
        
    Notes:
        - Maneja videos privados/borrados omitiendolos silenciosamente
        - Tolera errores de red y canales invalidos
        - Usa extract_flat: True para extraccion rapida
    """
    canal_url_procesada = normalizar_url_canal(channel_url)
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': False,  # Queremos ver warnings para depuracion
        'ignoreerrors': True,  # Continuar si hay errores en videos individuales
    }

    urls_encontradas = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(canal_url_procesada, download=False)
            
            if not info:
                return None, "No se pudo obtener informacion del canal. Verifica que la URL sea valida."

            # Verificar si es un canal o una lista de reproduccion
            if info.get('_type') == 'playlist':
                entries = info.get('entries', [])
            elif info.get('_type') == 'url':
                # Si es una URL directa a un video
                video_id = info.get('id')
                video_url = info.get('url') or f"https://www.youtube.com/watch?v={video_id}"
                titulo = info.get('title') or 'Sin titulo'
                urls_encontradas.append((titulo, video_url))
                return urls_encontradas, None
            else:
                # Es un canal
                entries = info.get('entries', [])
            
            if not entries:
                return None, "No se encontraron videos. Asegurate de que el canal tenga videos publicos."

            # Procesar cada entrada
            for entry in entries:
                # Saltar entradas nulas (videos borrados o privados)
                if not entry:
                    continue
                
                # Verificar si la entrada es un video valido
                if entry.get('is_unlisted') or entry.get('is_private'):
                    continue
                
                # Obtener informacion del video
                video_id = entry.get('id')
                video_url = entry.get('url')
                titulo = entry.get('title') or 'Sin titulo'
                
                # Si no hay URL, construirla
                if not video_url and video_id:
                    video_url = f"https://www.youtube.com/watch?v={video_id}"
                
                # Si la URL no es completa, completarla
                if video_url and not video_url.startswith('http'):
                    video_url = f"https://www.youtube.com/watch?v={video_url}"
                
                # Solo agregar si tenemos una URL valida
                if video_url:
                    urls_encontradas.append((titulo, video_url))
                    
                    # Limitar si se especifico max_urls
                    if max_urls > 0 and len(urls_encontradas) >= max_urls:
                        break
            
            if not urls_encontradas:
                return None, "No se encontraron videos publicos en este canal."
            
            return urls_encontradas, None
            
    except yt_dlp.utils.DownloadError as e:
        # Error de descarga (video privado, canal invalido, etc.)
        error_msg = str(e)
        if 'private' in error_msg.lower():
            return None, "El canal o algunos videos son privados y no se pueden acceder."
        elif 'not found' in error_msg.lower() or '404' in error_msg:
            return None, f"Canal no encontrado: {channel_url}"
        else:
            return None, f"Error al acceder al canal: {error_msg}"
    except yt_dlp.utils.ExtractorError as e:
        # Error del extractor
        return None, f"Error al procesar el canal: {str(e)}"
    except Exception as e:
        # Cualquier otro error
        return None, f"Error inesperado: {str(e)}"
