# Extractor de URLs de Canales de YouTube

Programa en Python para extraer todas las URLs de los videos de un canal de YouTube y guardarlas en un archivo de texto (`.txt`), una URL por línea.

## Requisitos
- Python 3.8 o superior
- Librería `yt-dlp`

Instalación de dependencias:
```bash
pip install -r requirements.txt
```

## Formas de uso

### 1. Modo Interactivo
Simplemente ejecuta el script:
```bash
python main.py
```
Te pedirá:
1. La URL o identificador del canal (por ejemplo: `@midudev`, `midudev`, o `https://www.youtube.com/@midudev`).
2. El nombre del archivo `.txt` donde se guardarán (por defecto: `urls_videos.txt`).

---

### 2. Modo por argumentos (Línea de comandos)
Puedes pasarle el canal y el archivo directamente:

```bash
# Formato: python main.py "<canal>" [nombre_archivo.txt]
python main.py "https://www.youtube.com/@NombreCanal" urls.txt
```
*(Nota: En PowerShell/Windows, pon el nombre del canal entre comillas si usas `@`, por ejemplo: `"@NombreCanal"`).*

## Características
- **Rápido y ligero**: Usa extracción *flat* (no descarga los videos ni el audio, solo obtiene la lista de enlaces).
- **Formatos flexibles**: Acepta URLs completas (`https://www.youtube.com/@canal/videos`), enlaces cortos o solo el `@handle`.
- **Manejo de errores**: Si algún video fue borrado o es privado, continúa con los demás sin detenerse.
- **Formato limpio**: Guarda una URL por cada línea en el archivo `.txt`.
