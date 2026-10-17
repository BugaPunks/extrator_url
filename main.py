import os
import sys
import json

# Asegurar codificacion UTF-8 en consola de Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Agregar el directorio del proyecto al path para importar el servicio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extractor.services.youtube import normalizar_url_canal, extraer_urls_canal
from extractor.utils.export import generar_archivo_txt


def main():
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

    incluir_titulos = input("¿Incluir títulos de videos? (s/n, Enter para no): ").strip().lower() == 's'
    
    print(f"\n[+] URL procesada: {normalizar_url_canal(canal)}")
    print("[+] Obteniendo lista de videos (esto puede demorar unos momentos)...")

    # Extraer URLs usando el servicio
    urls, error = extraer_urls_canal(canal, incluir_titulos)
    
    if error:
        print(f"\n[!] Error: {error}")
        sys.exit(1)
    
    if not urls:
        print("\n[!] No se encontraron videos.")
        sys.exit(1)

    # Generar archivo
    archivos = generar_archivo_txt(urls, incluir_titulos, 0)  # 0 = archivo unico
    contenido, nombre_archivo = archivos[0]
    
    ruta_salida = os.path.abspath(archivo)
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write(contenido)

    print(f"\n[OK] ¡Completado con éxito!")
    print(f"[OK] Total de videos extraídos: {len(urls)}")
    print(f"[OK] Archivo guardado en: {ruta_salida}\n")


if __name__ == "__main__":
    main()
