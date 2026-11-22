@echo off
title FutbolZone Stopper
color 0C
echo =========================================================
echo    🛑 DETENIENDO SERVIDORES DE FUTBOLZONE...
echo =========================================================
echo.

echo Liberando puerto 5000 (Backend FastAPI)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5000 "') do taskkill /f /pid %%a 2>nul

echo Liberando puerto 5173 (Frontend Vite)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":5173 "') do taskkill /f /pid %%a 2>nul

echo.
echo ✅ Los servidores de FutbolZone (puertos 5000 y 5173) han sido detenidos.
echo.
pause
