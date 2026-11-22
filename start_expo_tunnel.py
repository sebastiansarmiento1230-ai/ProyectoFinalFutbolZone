import subprocess
import time
import re
import os
import sys
import urllib.request
import json

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

print("=========================================================")
print("  ⚽ FUTBOLZONE — INICIANDO SERVICIOS PARA EXPOSICIÓN ⚽")
print("=========================================================")

# 1. Iniciar Backend
print("\n[1/3] Levantando Backend (FastAPI en http://localhost:5000)...")
backend_proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"],
    cwd=BACKEND_DIR,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding="utf-8",
    errors="replace"
)

# 2. Iniciar Frontend
print("[2/3] Levantando Frontend (Vite React en http://localhost:5173)...")
frontend_proc = subprocess.Popen(
    ["npm.cmd", "run", "dev"],
    cwd=FRONTEND_DIR,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding="utf-8",
    errors="replace"
)

# Esperar unos segundos a que ambos servidores estén listos
time.sleep(4)

# 3. Iniciar Cloudflare Tunnel para obtener URL pública HTTPS
print("[3/3] Generando Túnel Público Cloudflare (HTTPS)...")
cf_proc = subprocess.Popen(
    ["npx.cmd", "--yes", "cloudflared", "tunnel", "--url", "http://localhost:5173"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    encoding="utf-8",
    errors="replace"
)

tunnel_url = None
start_time = time.time()
while time.time() - start_time < 30:
    line = cf_proc.stdout.readline()
    if not line:
        continue
    # Buscar patrón de URL trycloudflare.com
    match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
    if match:
        tunnel_url = match.group(0)
        break

if tunnel_url:
    print("\n" + "="*60)
    print(f"🎉 ¡TÚNEL PÚBLICO CLOUDFLARE GENERADO CON ÉXITO!")
    print(f"🌐 ENLACE PÚBLICO HTTPS: {tunnel_url}")
    print(f"🏠 ENLACE LOCALHOST:      http://localhost:5173")
    print(f"📡 ENLACE RED LOCAL WIFI:  http://192.168.137.248:5173")
    print("="*60)

    # Guardar en archivo para consulta rápida
    with open(os.path.join(ROOT_DIR, "URL_EXPOSICION.txt"), "w", encoding="utf-8") as f:
        f.write(f"ENLACE_PUBLICO={tunnel_url}\n")
        f.write("ENLACE_LOCAL=http://localhost:5173\n")
        f.write("ENLACE_RED_LOCAL=http://192.168.137.248:5173\n")
        f.write("CREDENCIALES_ADMIN=admin@futbolzone.com / admin123\n")
        f.write("CREDENCIALES_CLIENTE=cliente@futbolzone.com / cliente123\n")

    # Verificar que el túnel responda
    print("\nVerificando conectividad externa a través del túnel...")
    try:
        req = urllib.request.Request(f"{tunnel_url}/api/canchas/", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            if res.status == 200:
                print("✅ [VERIFICADO] El túnel público responde y el proxy al backend funciona al 100%.")
            else:
                print(f"⚠️ El túnel respondió con código {res.status}")
    except Exception as e:
        print(f"Nota de comprobación: {e}")

else:
    print("⚠️ No se pudo obtener la URL de Cloudflare en 30s. Verifica la conexión.")

# Mantener los procesos vivos para la demostración
try:
    print("\nServidores y túnel activos. Presiona Ctrl+C para detener...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDeteniendo servicios...")
    cf_proc.terminate()
    frontend_proc.terminate()
    backend_proc.terminate()
