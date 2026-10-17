"""
Utilidades para exportacion de URLs a archivos .txt
"""
import os
import zipfile
from io import BytesIO, StringIO
from typing import List, Tuple
from django.http import FileResponse


def generar_archivo_txt(
    urls: List[Tuple[str, str]], 
    incluir_titulos: bool = False, 
    max_urls_por_archivo: int = 0
) -> List[Tuple[str, str]]:
    """
    Genera archivo(s) .txt con las URLs.
    
    Args:
        urls: Lista de tuplas (titulo, url)
        incluir_titulos: Si True, formato "Titulo - URL"
        max_urls_por_archivo: Maximo de URLs por archivo (0 = archivo unico)
        
    Returns:
        Lista de tuplas (contenido, nombre_archivo)
        
    Examples:
        >>> urls = [('Video 1', 'https://youtube.com/watch?v=abc'), ('Video 2', 'https://youtube.com/watch?v=def')]
        >>> generar_archivo_txt(urls, False, 0)
        [('https://youtube.com/watch?v=abc\\nhttps://youtube.com/watch?v=def', 'urls_videos.txt')]
        >>> generar_archivo_txt(urls, True, 1)
        [('Video 1 - https://youtube.com/watch?v=abc', 'urls_videos_parte_1.txt'), 
         ('Video 2 - https://youtube.com/watch?v=def', 'urls_videos_parte_2.txt')]
    """
    if not urls:
        return []
    
    if max_urls_por_archivo <= 0:
        # Archivo unico
        contenido = []
        for titulo, url in urls:
            if incluir_titulos:
                contenido.append(f"{titulo} - {url}")
            else:
                contenido.append(url)
        
        texto = "\n".join(contenido)
        return [(texto, "urls_videos.txt")]
    else:
        # Archivos divididos
        archivos = []
        parte = 1
        urls_actuales = []
        
        for titulo, url in urls:
            urls_actuales.append((titulo, url))
            
            if len(urls_actuales) >= max_urls_por_archivo:
                contenido = []
                for t, u in urls_actuales:
                    if incluir_titulos:
                        contenido.append(f"{t} - {u}")
                    else:
                        contenido.append(u)
                
                texto = "\n".join(contenido)
                nombre_archivo = f"urls_videos_parte_{parte}.txt"
                archivos.append((texto, nombre_archivo))
                urls_actuales = []
                parte += 1
        
        # Ultima parte (puede tener menos URLs)
        if urls_actuales:
            contenido = []
            for t, u in urls_actuales:
                if incluir_titulos:
                    contenido.append(f"{t} - {u}")
                else:
                    contenido.append(u)
            
            texto = "\n".join(contenido)
            nombre_archivo = f"urls_videos_parte_{parte}.txt"
            archivos.append((texto, nombre_archivo))
        
        return archivos


def crear_zip_con_archivos(archivos: List[Tuple[str, str]]) -> BytesIO:
    """
    Crea un archivo ZIP con los archivos dados.
    
    Args:
        archivos: Lista de tuplas (contenido, nombre_archivo)
        
    Returns:
        BytesIO con el contenido del ZIP
        
    Raises:
        ValueError: Si la lista de archivos esta vacia
    """
    if not archivos:
        raise ValueError("No hay archivos para comprimir")
    
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for contenido, nombre_archivo in archivos:
            # Asegurar que el contenido sea string
            if isinstance(contenido, str):
                zipf.writestr(nombre_archivo, contenido)
            else:
                zipf.writestr(nombre_archivo, str(contenido))
    
    zip_buffer.seek(0)
    return zip_buffer


def generar_response_descarga(
    urls: List[Tuple[str, str]], 
    incluir_titulos: bool = False,
    max_urls_por_archivo: int = 0,
    dividido: bool = False
) -> FileResponse:
    """
    Genera una FileResponse para descargar los archivos.
    
    Args:
        urls: Lista de tuplas (titulo, url)
        incluir_titulos: Si True, formato "Titulo - URL"
        max_urls_por_archivo: Maximo de URLs por archivo
        dividido: Si True, fuerza division (si max_urls_por_archivo > 0)
        
    Returns:
        FileResponse con el archivo o ZIP
        
    Raises:
        ValueError: Si no hay URLs para exportar
    """
    if not urls:
        raise ValueError("No hay URLs para exportar")
    
    if dividido and max_urls_por_archivo > 0:
        archivos = generar_archivo_txt(urls, incluir_titulos, max_urls_por_archivo)
        
        if len(archivos) > 1:
            zip_buffer = crear_zip_con_archivos(archivos)
            return FileResponse(
                zip_buffer,
                as_attachment=True,
                filename="urls_videos_divididos.zip",
                content_type="application/zip"
            )
        else:
            # Solo un archivo, devolver .txt
            contenido, nombre = archivos[0]
            return FileResponse(
                BytesIO(contenido.encode('utf-8')),
                as_attachment=True,
                filename=nombre,
                content_type="text/plain; charset=utf-8"
            )
    else:
        # Archivo unico
        archivos = generar_archivo_txt(urls, incluir_titulos, 0)
        contenido, nombre = archivos[0]
        return FileResponse(
            BytesIO(contenido.encode('utf-8')),
            as_attachment=True,
            filename=nombre,
            content_type="text/plain; charset=utf-8"
        )
