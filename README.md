# Echo — Industrial Knowledge Intelligence Platform

Echo is an AI-powered industrial knowledge intelligence platform designed to extract insights, manage equipment documentation, query technical SOPs, and provide interactive graphical/semantic visualizer for complex industrial systems.

---

## 🚀 How to Run Locally

### Option 1: Quick Launch (Windows)
Double-click `start.bat` or run:
```cmd
.\start.bat
```
This will launch both the FastAPI backend server and the Vite frontend application in separate windows.

### Option 2: Running Services Separately

#### 1. Start Backend (FastAPI)
```bash
# Using virtualenv python
.venv\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
- **Backend API**: `http://localhost:8000/api/v1`
- **Swagger API Docs**: `http://localhost:8000/docs`

#### 2. Start Frontend (Vite / React)
```bash
cd frontend
npm run dev
```
- **Frontend App**: `http://localhost:5173`

---

## 🛠 Project Structure

- `backend/`: FastAPI application, Supabase database bindings, Gemini/RAG services, and API routes.
- `frontend/`: Modern React (TypeScript) SPA with Tailwind CSS, Lucide icons, and React Query.
- `supabase/`: Database schemas and migrations for PostgreSQL/Supabase.

---

## ⚙️ Environment Variables

- Backend environment variables are configured in `backend/.env`.
- Frontend environment variables are configured in `frontend/.env`.
