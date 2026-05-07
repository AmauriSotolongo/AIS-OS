#!/usr/bin/env python3
"""
Descarga el audio de un Instagram Reel y lo transcribe con Whisper API.
Uso: python3 scripts/transcribe_reel.py <URL>
Output: transcripcion guardada en Amauri Brain/raw/YYYY-MM-DD-<slug>.md

Nota: funciona con Reels públicos. Para cuentas privadas necesitas
pasar cookies con --cookies-from-browser chrome en yt-dlp manualmente.
"""

import sys
import os
import subprocess
import json
import urllib.request
import tempfile
import re
from datetime import date


def get_openai_key():
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    with open(env_path) as f:
        for line in f:
            if line.startswith('OPENAI_API_KEY='):
                return line.split('=', 1)[1].strip()
    raise ValueError("OPENAI_API_KEY no encontrado en .env")


def get_reel_info(url):
    result = subprocess.run(
        ['yt-dlp', '--print', '%(uploader)s — %(title).60s', '--no-playlist', url],
        capture_output=True, text=True
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    # fallback: extraer el reel ID del URL
    match = re.search(r'/reel/([A-Za-z0-9_-]+)', url)
    return f"reel-{match.group(1)}" if match else "reel"


def download_audio(url, output_path):
    print("⬇️  Descargando audio del Reel...")
    result = subprocess.run([
        'yt-dlp',
        '--extract-audio',
        '--audio-format', 'mp3',
        '--audio-quality', '9',
        '--postprocessor-args', 'ffmpeg:-ac 1 -ar 16000 -b:a 32k',
        '--no-playlist',
        '-o', output_path,
        url
    ], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(
            f"Error descargando Reel.\n{result.stderr}\n\n"
            "Si la cuenta es privada, exporta las cookies de Instagram desde Chrome "
            "con la extensión 'Get cookies.txt LOCALLY' y pásalas con:\n"
            "  yt-dlp --cookies cookies.txt ..."
        )
    print("✅ Audio descargado")


def transcribe(audio_path, api_key):
    print("🎙️  Transcribiendo con Whisper API...")
    file_size = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"   Tamaño del archivo: {file_size:.1f} MB")

    with open(audio_path, 'rb') as f:
        audio_data = f.read()

    boundary = 'boundary123456'
    body = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="model"\r\n\r\n'
        f'whisper-1\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="file"; filename="audio.mp3"\r\n'
        f'Content-Type: audio/mpeg\r\n\r\n'
    ).encode() + audio_data + f'\r\n--{boundary}--\r\n'.encode()

    req = urllib.request.Request(
        'https://api.openai.com/v1/audio/transcriptions',
        data=body,
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': f'multipart/form-data; boundary={boundary}'
        }
    )

    with urllib.request.urlopen(req, timeout=300) as r:
        result = json.loads(r.read())

    return result['text']


def slugify(title):
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug.strip())
    return slug[:60]


def save_to_brain(title, url, transcript):
    today = date.today().isoformat()
    slug = slugify(title)
    filename = f"{today}-{slug}.md"

    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'Amauri Brain', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    output_path = os.path.join(raw_dir, filename)

    content = f"""# {title}

**Fuente:** {url}
**Fecha:** {today}
**Tipo:** transcripción de Instagram Reel

---

{transcript}
"""
    with open(output_path, 'w') as f:
        f.write(content)

    return output_path, filename


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 scripts/transcribe_reel.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    api_key = get_openai_key()

    print(f"\n📱 Procesando Reel: {url}\n")

    title = get_reel_info(url)
    print(f"📌 Identificado: {title}")

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, 'audio.%(ext)s')
        download_audio(url, audio_path)

        mp3_path = os.path.join(tmpdir, 'audio.mp3')
        if not os.path.exists(mp3_path):
            for f in os.listdir(tmpdir):
                if f.startswith('audio.'):
                    mp3_path = os.path.join(tmpdir, f)
                    break

        transcript = transcribe(mp3_path, api_key)

    output_path, filename = save_to_brain(title, url, transcript)

    print(f"\n✅ Transcripción guardada en:")
    print(f"   Amauri Brain/raw/{filename}")
    print(f"\n📋 Primeras 300 caracteres:")
    print(f"   {transcript[:300]}...")
    print(f"\n➡️  Ahora corre /ingest para procesar al Brain.")


if __name__ == '__main__':
    main()
