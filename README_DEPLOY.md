# Deploy-ready instructions (Frontend + Backend)

This project is split into:
- `api/` (FastAPI backend)
- `web/` (Next.js frontend)

## Local run (quick test)

**Backend**
```bash
cd api
python -m venv .venv
# mac/linux:
source .venv/bin/activate
# windows:
# .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

**Frontend**
```bash
cd web
npm install
npm run dev
```

Open: http://localhost:3000

> Note: if you haven't added `api/models/wheel.pt` yet, the backend will return 0 detections (but won't crash).

## Deploy (recommended): Render (API) + Vercel (Web)

### 1) Put code on GitHub
Create a repo with this structure:
```
wheel-tryon/
  api/
  web/
```

### 2) Deploy API to Render
- New > Web Service
- Root Directory: `api`
- Build Command: `pip install -r requirements.txt`
- Start Command:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port $PORT
  ```
After deploy, test:
- `https://YOUR-RENDER-URL/health` -> `{"ok": true}`

### 3) Deploy Web to Vercel
- New Project > Import repo
- Root Directory: `web`
- Environment Variable:
  - `NEXT_PUBLIC_API_BASE` = `https://YOUR-RENDER-URL`
Deploy, then open your Vercel URL.

## Adding the AI weights
Place your YOLO weights at:
- `api/models/wheel.pt`

Then redeploy the Render service (or push to GitHub if included in repo).
