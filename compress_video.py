"""
compress_video.py

Script para comprimir vídeos MP4 usando ffmpeg:
- Usa H.264 con CRF variable (valor por defecto: 23).
- Preset configurable (por defecto: slow).
- Bitrate de audio configurable.
- Procesamiento de un archivo o de todos los mp4 en un directorio.
"""

import os
import sys
import argparse
import subprocess
from tqdm import tqdm

def compress(input_path: str,
             output_path: str,
             crf: int,
             preset: str,
             audio_bitrate: str,
             threads: int):
    """
    Ejecuta ffmpeg para comprimir el vídeo.
    """
    cmd = [
        'ffmpeg',
        '-y',  # sobrescribir sin preguntar
        '-i', input_path,
        '-c:v', 'libx264',
        '-preset', preset,
        '-crf', str(crf),
        '-c:a', 'aac',
        '-b:a', audio_bitrate,
        '-threads', str(threads),
        output_path
    ]
    # Lanza ffmpeg y muestra salida en tiempo real
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        # Opcional: parsear progreso de ffmpeg
        # aquí simplemente lo imprimimos
        sys.stdout.write(line)
    process.wait()
    return process.returncode

def main():
    parser = argparse.ArgumentParser(description="Comprime vídeos MP4 manteniendo calidad.")
    parser.add_argument('input', help="Archivo MP4 de entrada o directorio con MP4s")
    parser.add_argument('-o', '--output', help="Archivo o carpeta de salida (por defecto same location + _compressed)", default=None)
    parser.add_argument('--crf', type=int, default=23, help="Valor CRF (18–28, menor = mejor calidad). Default: 23")
    parser.add_argument('--preset', choices=['ultrafast','superfast','veryfast','faster','fast','medium','slow','slower','veryslow'],
                        default='slow', help="Preset de compresión (más lento = mejor ratio). Default: slow")
    parser.add_argument('--audio-bitrate', default='128k', help="Bitrate de audio (Default: 128k)")
    parser.add_argument('--threads', type=int, default=0, help="Número de hilos para ffmpeg (0 = auto).")
    args = parser.parse_args()

    # Determinar lista de archivos
    inputs = []
    if os.path.isdir(args.input):
        for f in os.listdir(args.input):
            if f.lower().endswith('.mp4'):
                inputs.append(os.path.join(args.input, f))
    else:
        inputs = [args.input]

    if not inputs:
        print("❌ No se encontraron archivos MP4 para procesar.")
        sys.exit(1)

    for in_file in tqdm(inputs, desc="Procesando vídeos"):
        base, ext = os.path.splitext(os.path.basename(in_file))
        # directorio de salida
        if args.output:
            if os.path.isdir(args.output):
                out_file = os.path.join(args.output, base + "_compressed.mp4")
            else:
                # si es archivo único
                out_file = args.output
        else:
            out_file = os.path.join(os.path.dirname(in_file), base + "_compressed.mp4")

        code = compress(in_file, out_file, args.crf, args.preset, args.audio_bitrate, args.threads)
        if code != 0:
            print(f"⚠️ Error al comprimir {in_file} (exit code {code})")
        else:
            in_size = os.path.getsize(in_file) / (1024*1024)
            out_size = os.path.getsize(out_file) / (1024*1024)
            ratio = out_size / in_size * 100
            print(f"✅ {in_file} → {out_file}: {in_size:.1f} MB → {out_size:.1f} MB ({ratio:.0f}% tamaño)")

if __name__ == "__main__":
    main()
