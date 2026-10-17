"""
Utilidades para exportacion de URLs a archivos .txt
"""
import os
import zipfile
import tempfile
from io import BytesIO
from django.http import FileResponse


def generar_archivo_txt(urls, incluir_titulos=False, max_urls_por_archivo=0):
    """
    Genera archivo(s) .txt con las URLs.
    
    Args:
        urls: Lista de tuplas (titulo, url)
        incluir_titulos: Si True, formato "Titulo - URL"
        max_urls_por_archivo: Maximo de URLs por archivo (0 = archivo unico)
        
    Returns:
        Si max_urls_por_archivo == 0: (contenido, nombre_archivo)
        Si max_urls_por_archivo > 0: lista de (contenido, nombre_archivo)
    """
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
        
        # Ultima parte
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


def crear_zip_con_archivos(archivos):
    """
    Crea un archivo ZIP con los archivos dados.
    
    Args:
        archivos: Lista de tuplas (contenido, nombre_archivo)
        
    Returns:
        BytesIO con el contenido del ZIP
    """
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for contenido, nombre_archivo in archivos:
            zipf.writestr(nombre_archivo, contenido)
    
    zip_buffer.seek(0)
    return zip_buffer


def generar_response_descarga(urls, incluir_titulos=False, max_urls_por_archivo=0, dividido=False):
    """
    Genera una FileResponse para descargar los archivos.
    
    Args:
        urls: Lista de tuplas (titulo, url)
        incluir_titulos: Si True, formato "Titulo - URL"
        max_urls_por_archivo: Maximo de URLs por archivo
        dividido: Si True, fuerza division (si max_urls_por_archivo > 0)
        
    Returns:
        FileResponse con el archivo o ZIP
    """
    if dividido and max_urls_por_archivo > 0:
        archivos = generar_archivo_txt(urls, incluir_titulos, max_urls_por_archivo)
        
        if len(archivos) > 1:
            zip_buffer = crear_zip_con_archivos(archivos)
            return FileResponse(
                zip_buffer,
                as_attachment=True,
                filename="urls_videos_divididos.zip"
            )
        else:
            # Solo un archivo, devolver .txt
            contenido, nombre = archivos[0]
            return FileResponse(
                BytesIO(contenido.encode('utf-8')),
                as_attachment=True,
                filename=nombre
            )
    else:
        # Archivo unico
        archivos = generar_archivo_txt(urls, incluir_titulos, 0)
        contenido, nombre = archivos[0]
        return FileResponse(
            BytesIO(contenido.encode('utf-8')),
            as_attachment=True,
            filename=nombre
        )
