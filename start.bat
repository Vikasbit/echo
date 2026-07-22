@echo off
echo Starting Echo Industrial Knowledge Intelligence Platform...

SET PYTHON_CMD=python
IF EXIST ".venv\Scripts\python.exe" (
    SET PYTHON_CMD=.venv\Scripts\python.exe
)

start "Echo Backend (FastAPI)" cmd /k "%PYTHON_CMD% -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"
start "Echo Frontend (Vite)" cmd /k "cd frontend && npm run dev"

echo.
echo ===================================================
echo  Echo Platform Started!
echo  - Frontend App:  http://localhost:5173
echo  - Backend API:   http://localhost:8000/api/v1
echo  - API Docs:      http://localhost:8000/docs
echo ===================================================
