# Compress Video GUI

## Descripción

**Compress Video GUI** es una herramienta de escritorio con interfaz gráfica desarrollada en **Tkinter** para comprimir vídeos MP4 usando **ffmpeg**. Permite ajustar parámetros clave como:

- **CRF** (Constant Rate Factor, rango 18–28)  
- **Preset** de codificación H.264 (`ultrafast`, `slow`, `veryslow`, etc.)  
- **Bitrate** de audio (por ejemplo, `128k`)  
- **Hilos** de CPU (0 = auto)

Muestra en tiempo real la salida de `ffmpeg` en un área de texto desplazable y ejecuta la tarea de compresión en un hilo separado para mantener la interfaz responsiva.

## Requisitos

- **Python 3.6+**  
- **ffmpeg** instalado y accesible en tu `PATH`  
- Paquetes Python:
  - `tqdm>=4.0.0`

*(Tkinter forma parte de la biblioteca estándar de Python y no requiere instalación adicional.)*

## Instalación

```bash
# Clona el repositorio
git clone https://github.com/tu-usuario/tu-repo.git
cd tu-repo

# (Opcional) Crea y activa un entorno virtual
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate

# Instala las dependencias
pip install -r requirements.txt
```

## Uso
```
python compress_video_gui.py
```

1. En la ventana, selecciona el archivo o carpeta de entrada con vídeos MP4.

2. Elige la carpeta o ruta de archivo de salida.

3. Ajusta CRF, preset, bitrate de audio y número de hilos.

4. Haz clic en Iniciar Compresión y observa los logs de ffmpeg en tiempo real.

## Contribuciones

1. Haz un _fork_ de este repositorio.  
2. Crea una rama (`git checkout -b mejora-feature`).  
3. Realiza tus cambios y haz _commit_ (`git commit -am "Agrega nueva función"`).  
4. Empuja la rama (`git push origin mejora-feature`).  
5. Abre un _Pull Request_.

## Licencia

MIT License – consulta el archivo [LICENSE](LICENSE) para más detalles.