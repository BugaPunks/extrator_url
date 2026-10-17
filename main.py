import os
import sys
import yt_dlp

# Asegurar codificación UTF-8 en consola de Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def normalizar_url_canal(canal_input: str) -> str:
    """
    Normaliza la entrada del usuario para asegurar un formato válido de YouTube
    apuntando a la sección de videos.
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

    # Si no especifica una pestaña (/videos, /shorts, /streams, etc.), agregamos /videos
    pestanas = ('/videos', '/shorts', '/streams', '/playlists', '/featured')
    if not any(url.endswith(p) for p in pestanas):
        url = f"{url}/videos"
        
    return url

def extraer_urls_canal(channel_url: str, archivo_salida: str = "urls_videos.txt", incluir_titulos: bool = False):
    canal_url_procesada = normalizar_url_canal(channel_url)
    
    print(f"\n[+] URL procesada: {canal_url_procesada}")
    print("[+] Obteniendo lista de videos (esto puede demorar unos momentos)...")

    ydl_opts = {
        'extract_flat': True,       # Extrae la lista rápidamente sin descargar contenido
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,       # Si algún video fue borrado o es privado, continúa
    }

    urls_encontradas = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(canal_url_procesada, download=False)
        except Exception as e:
            print(f"\n[!] Error al acceder al canal: {e}")
            return []

        if not info:
            print("\n[!] No se pudo obtener información del canal.")
            return []

        nombre_canal = info.get('channel') or info.get('uploader') or info.get('title') or "Canal"
        print(f"[OK] Canal detectado: {nombre_canal}")

        entries = info.get('entries', [])
        for entry in entries:
            if not entry:
                continue
            
            video_id = entry.get('id')
            video_url = entry.get('url') or (f"https://www.youtube.com/watch?v={video_id}" if video_id else None)
            titulo = entry.get('title') or 'Sin título'

            if video_url:
                if not video_url.startswith('http'):
                    video_url = f"https://www.youtube.com/watch?v={video_url}"
                urls_encontradas.append((titulo, video_url))

    if not urls_encontradas:
        print("\n[!] No se encontraron videos. Asegúrate de que el canal tenga videos públicos.")
        return []

    ruta_salida = os.path.abspath(archivo_salida)
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        for titulo, url in urls_encontradas:
            if incluir_titulos:
                f.write(f"{titulo} - {url}\n")
            else:
                f.write(f"{url}\n")

    print(f"\n[OK] ¡Completado con éxito!")
    print(f"[OK] Total de videos extraídos: {len(urls_encontradas)}")
    print(f"[OK] Archivo guardado en: {ruta_salida}\n")
    return urls_encontradas

if __name__ == "__main__":
    print("=" * 45)
    print("   EXTRACTOR DE URLs DE VIDEOS DE YOUTUBE   ")
    print("=" * 45)

    if len(sys.argv) > 1:
        canal = sys.argv[1]
        archivo = sys.argv[2] if len(sys.argv) > 2 else "urls_videos.txt"
    else:
        canal = input("\nIngresa la URL o handle del canal (ej: @midudev o URL completa): ").strip()
        if not canal:
            print("[!] No se ingresó ningún canal.")
            sys.exit(1)
        archivo = input("Nombre del archivo .txt (Enter para 'urls_videos.txt'): ").strip()
        if not archivo:
            archivo = "urls_videos.txt"

    if not archivo.endswith(".txt"):
        archivo += ".txt"

    extraer_urls_canal(canal, archivo)
