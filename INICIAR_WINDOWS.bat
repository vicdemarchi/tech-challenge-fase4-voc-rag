@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Ambiente Python nao encontrado. Siga docs\COMECE_AQUI.md.
  pause
  exit /b 1
)
if not exist "artifacts\index_manifest.json" (
  echo Indice nao encontrado. Execute as etapas de dados e indice do README.
  pause
  exit /b 1
)
echo Mantenha o Ollama aberto com o modelo qwen2.5:3b instalado.
".venv\Scripts\python.exe" -m streamlit run app.py
pause
