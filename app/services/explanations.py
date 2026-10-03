"""Bilingual labels and explicitly typed AI-style explanations."""
def prediction_note(forecast):
    amount=forecast.get("prediction",0)
    return {"type":"Prediction","en":f"The selected model estimates next-month expenses at about ৳{amount:,.0f}.",
      "bn":f"নির্বাচিত মডেলের হিসাবে পরের মাসের খরচ প্রায় ৳{amount:,.0f} হতে পারে।"}
