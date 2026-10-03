"""Load the trained model and return a transparent next-month expense estimate."""
import json
import joblib
import pandas as pd
from ..config import MODEL_PATH, METRICS_PATH, FEATURES_PATH

_bundle = None
def load_model():
    global _bundle
    if _bundle is None and MODEL_PATH.exists(): _bundle = joblib.load(MODEL_PATH)
    return _bundle

def forecast_for_user(monthly_rows):
    rows = [dict(r) for r in monthly_rows]
    if not rows: return {"available":False,"prediction":0,"model":"unavailable","history_months":0}
    bundle = load_model()
    latest = rows[-1]
    if bundle:
        x = pd.DataFrame([{k: latest[k] for k in bundle["feature_columns"]}])
        value = float(max(0, bundle["model"].predict(x)[0])); selected = bundle["selected_model"]
    else:
        value = float(sum(float(r["total_expense"]) for r in rows[-3:]) / min(3, len(rows))); selected = "Rolling 3-month baseline (model artifact missing)"
    recent = [float(r["total_expense"]) for r in rows[-3:]]
    return {"available":True,"prediction":round(value,2),"model":selected,"history_months":len(rows),
      "last_month_expense":round(float(latest["total_expense"]),2),"rolling_3m_expense":round(sum(recent)/len(recent),2),
      "assumption":"The estimate uses synthetic historical behavior and is not a guarantee.",
      "assumption_bn":"এই অনুমানটি কৃত্রিম আগের খরচের তথ্য থেকে করা; এটি নিশ্চিত ফল নয়।"}

def read_json(path, default):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError): return default
