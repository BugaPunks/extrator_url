"""
Servicio de extraccion de URLs de YouTube
"""
import yt_dlp


def normalizar_url_canal(canal_input: str) -> str:
    """
    Normaliza la entrada del usuario para asegurar un formato valido de YouTube
    apuntando a la seccion de videos.
    """
    url = canal_input.strip().rstrip('/')
    
    # Si ingresaron solo el handle (ej: @midudev o midudev)
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


def extraer_urls_canal(channel_url: str, incluir_titulos: bool = False):
    """
    Extrae URLs de videos de un canal de YouTube.
    
    Args:
        channel_url: URL o handle del canal
        incluir_titulos: Si True, devuelve tuplas (titulo, url), sino solo urls
        
    Returns:
        Lista de tuplas (titulo, url) o solo urls, o lista vacia en caso de error
    """
    canal_url_procesada = normalizar_url_canal(channel_url)
    
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
    }

    urls_encontradas = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(canal_url_procesada, download=False)
        except Exception as e:
            return None, f"Error al acceder al canal: {str(e)}"

        if not info:
            return None, "No se pudo obtener informacion del canal."

        nombre_canal = info.get('channel') or info.get('uploader') or info.get('title') or "Canal"

        entries = info.get('entries', [])
        for entry in entries:
            if not entry:
                continue
            
            video_id = entry.get('id')
            video_url = entry.get('url') or (f"https://www.youtube.com/watch?v={video_id}" if video_id else None)
            titulo = entry.get('title') or 'Sin titulo'

            if video_url:
                if not video_url.startswith('http'):
                    video_url = f"https://www.youtube.com/watch?v={video_url}"
                urls_encontradas.append((titulo, video_url))

    if not urls_encontradas:
        return None, "No se encontraron videos. Asegurate de que el canal tenga videos publicos."

    return urls_encontradas, None
