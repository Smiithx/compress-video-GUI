#!/usr/bin/env python3
"""
compress_video_gui.py

Aplicación con interfaz gráfica en Tkinter para comprimir vídeos MP4 usando ffmpeg:
- Usa H.264 con CRF configurable.
- Preset configurable.
- Bitrate de audio configurable.
- Selección de archivo/carpeta de entrada y carpeta de salida.
- Muestra salida de ffmpeg en un área de texto.
"""
import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext, messagebox

# Configuración de presets disponibles
default_presets = ['ultrafast','superfast','veryfast','faster','fast','medium','slow','slower','veryslow']


def compress(input_path: str,
             output_path: str,
             crf: int,
             preset: str,
             audio_bitrate: str,
             threads: int,
             log_widget: scrolledtext.ScrolledText):
    """
    Ejecuta ffmpeg para comprimir el vídeo dado y escribe logs en el widget.
    """
    cmd = [
        'ffmpeg',
        '-y',
        '-i', input_path,
        '-c:v', 'libx264',
        '-preset', preset,
        '-crf', str(crf),
        '-c:a', 'aac',
        '-b:a', audio_bitrate,
        '-threads', str(threads),
        output_path
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        log_widget.insert(tk.END, line)
        log_widget.see(tk.END)
    process.wait()
    return process.returncode


def start_compression(params, log_widget, btn_start):
    """
    Lanza la compresión en un hilo para no bloquear la GUI.
    """
    btn_start.config(state=tk.DISABLED)
    inputs = []
    inp = params['input_path'].get()
    if os.path.isdir(inp):
        for f in os.listdir(inp):
            if f.lower().endswith('.mp4'):
                inputs.append(os.path.join(inp, f))
    else:
        inputs = [inp]

    if not inputs:
        messagebox.showerror("Error", "No se encontraron archivos MP4.")
        btn_start.config(state=tk.NORMAL)
        return

    out_base = params['output_path'].get()
    crf = int(params['crf'].get())
    preset = params['preset'].get()
    audio_bitrate = params['audio_bitrate'].get()
    threads = int(params['threads'].get())

    for in_file in inputs:
        base, _ = os.path.splitext(os.path.basename(in_file))
        if out_base:
            if os.path.isdir(out_base):
                out_file = os.path.join(out_base, f"{base}_compressed.mp4")
            else:
                out_file = out_base
        else:
            out_file = os.path.join(os.path.dirname(in_file), f"{base}_compressed.mp4")

        log_widget.insert(tk.END, f"\nComprimir: {in_file}\n")
        code = compress(in_file, out_file, crf, preset, audio_bitrate, threads, log_widget)
        if code != 0:
            log_widget.insert(tk.END, f"⚠️ Error al comprimir {in_file} (codigo {code})\n")
        else:
            in_size = os.path.getsize(in_file)/(1024*1024)
            out_size = os.path.getsize(out_file)/(1024*1024)
            ratio = out_size/in_size*100
            log_widget.insert(tk.END, f"✅ {in_file} → {out_file}: {in_size:.1f}MB → {out_size:.1f}MB ({ratio:.0f}%)\n")
        log_widget.see(tk.END)

    btn_start.config(state=tk.NORMAL)


def create_gui():
    root = tk.Tk()
    root.title("Compress Video - Tkinter GUI")
    root.geometry('700x600')

    frame = ttk.Frame(root, padding=10)
    frame.pack(fill=tk.BOTH, expand=True)

    # Parámetros de entrada
    params = {
        'input_path': tk.StringVar(),
        'output_path': tk.StringVar(),
        'crf': tk.StringVar(value='23'),
        'preset': tk.StringVar(value='slow'),
        'audio_bitrate': tk.StringVar(value='128k'),
        'threads': tk.StringVar(value='0')
    }

    # Input file/folder
    ttk.Label(frame, text="Entrada (archivo o carpeta MP4):").grid(column=0, row=0, sticky=tk.W)
    inp_entry = ttk.Entry(frame, textvariable=params['input_path'], width=50)
    inp_entry.grid(column=1, row=0, sticky=tk.W)
    ttk.Button(frame, text="Browse...", command=lambda: params['input_path'].set(filedialog.askopenfilename(filetypes=[('MP4 Files','*.mp4')]))).grid(column=2, row=0)
    ttk.Button(frame, text="Folder", command=lambda: params['input_path'].set(filedialog.askdirectory())).grid(column=3, row=0)

    # Output folder
    ttk.Label(frame, text="Salida (carpeta o archivo):").grid(column=0, row=1, sticky=tk.W)
    out_entry = ttk.Entry(frame, textvariable=params['output_path'], width=50)
    out_entry.grid(column=1, row=1, sticky=tk.W)
    ttk.Button(frame, text="Browse...", command=lambda: params['output_path'].set(filedialog.askdirectory())).grid(column=2, row=1)

    # CRF
    ttk.Label(frame, text="CRF (18-28):").grid(column=0, row=2, sticky=tk.W)
    crf_spin = ttk.Spinbox(frame, from_=18, to=28, textvariable=params['crf'], width=5)
    crf_spin.grid(column=1, row=2, sticky=tk.W)

    # Preset
    ttk.Label(frame, text="Preset:").grid(column=0, row=3, sticky=tk.W)
    preset_combo = ttk.Combobox(frame, values=default_presets, textvariable=params['preset'], state='readonly')
    preset_combo.grid(column=1, row=3, sticky=tk.W)

    # Audio bitrate
    ttk.Label(frame, text="Audio Bitrate:").grid(column=0, row=4, sticky=tk.W)
    ttk.Entry(frame, textvariable=params['audio_bitrate'], width=10).grid(column=1, row=4, sticky=tk.W)

    # Threads
    ttk.Label(frame, text="Hilos (0=auto):").grid(column=0, row=5, sticky=tk.W)
    ttk.Entry(frame, textvariable=params['threads'], width=5).grid(column=1, row=5, sticky=tk.W)

    # Botón iniciar
    btn_start = ttk.Button(frame, text="Iniciar Compresión", command=lambda: threading.Thread(target=start_compression, args=(params, log, btn_start), daemon=True).start())
    btn_start.grid(column=1, row=6, pady=10)

    # Área de logs
    log = scrolledtext.ScrolledText(frame, width=80, height=20)
    log.grid(column=0, row=7, columnspan=4, pady=10)

    root.mainloop()


if __name__ == '__main__':
    create_gui()