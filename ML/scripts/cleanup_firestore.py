import json
import sys
from pathlib import Path

_ML_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ML_DIR))

import firebase_admin
from firebase_admin import credentials, firestore

HOLDOUT_PATH = _ML_DIR / "data/processed/split_holdout.json"
KEY_PATH = _ML_DIR.parent / "fintech-hackathon-2-firebase-adminsdk-fbsvc-5e5a462a40.json"

holdout_ids = set(json.loads(HOLDOUT_PATH.read_text()))
print(f"Holdout set: {len(holdout_ids)} clients")

cred = credentials.Certificate(str(KEY_PATH))
firebase_admin.initialize_app(cred)
db = firestore.client()

docs = list(db.collection("clients").stream())
print(f"Total docs in Firestore: {len(docs)}")

to_delete = [d for d in docs if d.id not in holdout_ids]
print(f"Docs to delete: {len(to_delete)}")

batch = db.batch()
count = 0
for doc in to_delete:
    batch.delete(doc.reference)
    count += 1
    if count % 500 == 0:
        batch.commit()
        batch = db.batch()
        print(f"  Deleted {count}...")

if count % 500 != 0:
    batch.commit()

print(f"Done. Deleted {len(to_delete)} non-holdout clients.")
