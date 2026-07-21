# run_all.ps1
# Script to run the Echo complete project (Backend, Frontend)

Write-Host "Starting Echo MVP Project..." -ForegroundColor Green

# Start Backend
Write-Host "Starting FastAPI Backend..." -ForegroundColor Cyan
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "cd backend; if (Test-Path .venv) { .venv\Scripts\activate }; uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# Start Frontend
Write-Host "Starting Vite Frontend..." -ForegroundColor Cyan
Start-Process -FilePath "powershell.exe" -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host "Both services started in separate windows." -ForegroundColor Green
Write-Host "Backend API: http://localhost:8000"
Write-Host "Frontend App: http://localhost:5173"
