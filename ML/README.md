# Fintech Hackathon — Bank Retention Platform

AI-powered client retention platform: churn prediction, value scoring, and personalized cashback recommendations.

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- Firebase service account key at repo root (`fintech-hackathon-2-firebase-adminsdk-fbsvc-5e5a462a40.json`)

---

## 1. Install dependencies

**Python (API + pipeline):**
```bash
cd ML
pip install -r requirements.txt
```

**Frontend:**
```bash
# from repo root
npm install
```

---

## 2. Score holdout clients (one-time)

Runs the churn + value models on the 462 holdout clients and writes scores to Firestore.

```bash
cd ML
python scripts/score_holdout.py
```

---

## 3. Start the API

```bash
cd ML
uvicorn api.main:app --reload --port 8000
```

Verify it's running:
```bash
curl http://localhost:8000/health
```

---

## 4. Start the frontend

```bash
# from repo root
npm run dev
```

Open [http://localhost:5173](http://localhost:5173)

Login with: `vili.cenko@gmail.com` / `123456`

---

## Full startup (steps 3 + 4 together)

```bash
# Terminal 1
cd ML && uvicorn api.main:app --reload --port 8000

# Terminal 2
npm run dev
```

---

## Project structure

```
Fintech-hackathon/
├── src/                  # SvelteKit frontend
├── ML/
│   ├── api/              # FastAPI recommendation endpoint
│   ├── scripts/          # score_holdout.py, cleanup_firestore.py
│   ├── data/
│   │   ├── models/       # Trained LightGBM + NMF models
│   │   └── processed/    # Feature parquets, split files
│   └── requirements.txt
└── CLAUDE.md             # Full architecture reference
```
