# HPB Retention Platform

A full-stack AI platform built for a bank hackathon. It identifies which clients are at risk of churning, scores their value to the bank, and surfaces personalized cashback offers — so relationship managers can focus retention budgets where they matter most.

---

## What it does

### Priority scoring
Every client gets a **churn risk score** (LightGBM classifier) and a **value score** (weighted segmentation across balance, revenue, product depth, tenure, and credit rating). These are combined into a priority action:

| Action | Criteria |
|---|---|
| **Retain** | Risk ≥ 40 and Value ≥ 40 — act now |
| **Monitor** | Risk ≥ 20 and Value ≥ 40 — watch closely |
| **Nurture** | Risk < 20 and Value ≥ 40 — low risk, high value |
| **Low Priority** | All others |

### Personalized cashback offers
For every client, the recommendation engine (ALS/NMF candidate generation + LightGBM ranker) produces up to 3 cashback offers ranked by predicted spending affinity. Cashback percentages are dynamically calculated per client using a weighted formula: `B + (CBOmax − B) × (0.6 × value + 0.4 × risk)`.

### Contract partnership recommendations
An aggregated view of which merchant categories offer the best partnership potential across the entire client portfolio, rated A–E by confidence.

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | SvelteKit, Tailwind CSS |
| Database | Firebase Firestore |
| ML pipeline | Python, LightGBM, SHAP, NMF (implicit) |
| API | FastAPI (port 8000) |

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- Firebase service account key at repo root: `fintech-hackathon-2-firebase-adminsdk-fbsvc-5e5a462a40.json`

---

## Setup

**Install Python dependencies:**
```bash
cd ML
pip install -r requirements.txt
```

**Install frontend dependencies:**
```bash
npm install
```

**Score holdout clients** (one-time — writes ML scores to Firestore):
```bash
cd ML
python scripts/score_holdout.py
```

---

## Running the app

Open two terminals:

```bash
# Terminal 1 — API
cd ML
uvicorn api.main:app --reload --port 8000

# Terminal 2 — Frontend
npm run dev
```

Open [http://localhost:5173](http://localhost:5173) and log in with:
- Email: `vili.cenko@gmail.com`
- Password: `123456`

---

## How to use it

### Dashboard (home page)
- The **client list** shows all 462 holdout clients with their priority action badge, risk score, and value score.
- Use the **sidebar filters** to narrow by priority action (Retain / Monitor / Nurture / Low Priority), risk range, value range, or name search.
- Click the **Risk** or **Value** column headers to sort ascending or descending.
- The **stats bar** at the top shows portfolio-level counts: total clients, high-risk count, high-value count, and priority retention count.

### Client detail page
Click any client to open their detail view:
- **Priority banner** — shows the computed action (Retain / Monitor / Nurture / Low Priority) at the top.
- **Churn risk section** — risk score, top SHAP drivers explaining why the model flagged this client, and an explanation string.
- **Value assessment section** — value score, value tier (Bronze / Silver / Gold / Platinum), and component breakdown (balance, revenue, product depth, tenure, primary bank status, credit rating).
- **Personalized offers section** — up to 3 cashback offers ranked by model score, showing cashback %, expected EUR/month, duration, and minimum spend.

### Contract Partnerships page
- Navigate via the top navbar.
- Ranks all merchant categories by partnership attractiveness (A–E rating).
- Filter by client risk or value score range to see which categories are most relevant for a given client segment.
- The **Confidence** score reflects partnership attractiveness based on client spending volume, penetration rate, and segment affinity across the holdout portfolio.

---

## Project structure

```
Fintech-hackathon/
├── src/                          # SvelteKit frontend
│   ├── routes/
│   │   ├── +page.svelte          # Dashboard (client list)
│   │   ├── client/[id]/          # Client detail page
│   │   ├── recommendations/      # Contract partnerships page
│   │   └── login/                # Login page
│   └── lib/
│       ├── components/           # ClientCard, RetentionCard, FilterPanel, ...
│       ├── stores/               # clientStore (filtering + sorting)
│       ├── priority.ts           # computePriority logic
│       ├── api/retention.ts      # FastAPI client
│       └── firebase/             # Firestore read helpers
├── ML/
│   ├── api/                      # FastAPI app + recommend service
│   ├── scripts/
│   │   └── score_holdout.py      # One-time pipeline: score + write to Firestore
│   ├── data/
│   │   ├── models/               # Trained LightGBM, NMF models
│   │   └── processed/            # Feature parquets, holdout split
│   ├── config.py                 # Offer catalog, thresholds, weights
│   ├── ModelToConfig.py          # Dynamic cashback formula
│   └── requirements.txt
└── CLAUDE.md                     # Full architecture and data model reference
```
