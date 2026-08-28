#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$PROJECT_DIR/.venv"

if [ ! -d "$VENV" ]; then
  echo "Error: .venv no encontrado en $PROJECT_DIR"
  exit 1
fi

cleanup() {
  echo ""
  echo "Deteniendo servidores..."
  [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null
  [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null
  wait
  echo "Servidores detenidos."
  exit 0
}

trap cleanup SIGINT SIGTERM

echo "Script de inicio para OxigenScript"
echo ""

echo "[1/2] Iniciando backend (FastAPI en puerto 8000)..."
"$VENV/bin/uvicorn" api.main:app --host 0.0.0.0 --port 8000 --reload >/tmp/fastapi.log 2>&1 &
BACKEND_PID=$!
echo "      Backend PID: $BACKEND_PID"

sleep 2

if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
  echo "      Error: Backend no pudo iniciarse. Revisa /tmp/fastapi.log"
  exit 1
fi

echo "[2/2] Iniciando frontend (Astro en puerto 4321)..."
cd "$PROJECT_DIR/frontend"
npx astro dev --host 0.0.0.0 >/tmp/astro.log 2>&1 &
FRONTEND_PID=$!
echo "      Frontend PID: $FRONTEND_PID"

sleep 3

if ! kill -0 "$FRONTEND_PID" 2>/dev/null; then
  echo "      Error: Frontend no pudo iniciarse. Revisa /tmp/astro.log"
  kill "$BACKEND_PID" 2>/dev/null
  exit 1
fi

echo ""
echo "Servidores listos"
echo "  Frontend: http://localhost:4321"
echo "  Backend:  http://localhost:8000"
echo ""
echo "Presiona Ctrl+Alt+C para detener ambos servidores."
echo ""

wait
