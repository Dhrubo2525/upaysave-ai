"""Compare two synthetic savings-plan scenarios; not real-world evidence."""
import csv, json, statistics
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; DATA=ROOT/"data"
def main():
    users={r["user_id"]:r for r in csv.DictReader((DATA/"users.csv").open(encoding="utf-8-sig",newline=""))}
    by_user={}
    for r in csv.DictReader((DATA/"monthly_features.csv").open(encoding="utf-8-sig",newline="")):
        by_user.setdefault(r["user_id"],[]).append(r)
    achieved={"control":0,"treatment":0}; projected={"control":0.0,"treatment":0.0}; reductions=[]; feasible={"control":0,"treatment":0}
    count=0
    for uid,rows in by_user.items():
        rows=sorted(rows,key=lambda x:x["month"]); recent=rows[-3:]
        income=statistics.median(float(x["income"]) for x in recent)
        expense=statistics.mean(float(x["total_expense"]) for x in recent)
        shop=statistics.mean(float(x["shopping_expense"]) for x in recent)
        cap=max(0,income-expense-max(1000,round(income*.05)))
        treat_cap=max(0,income-(expense-shop*.08)-max(1000,round(income*.05)))
        # A common synthetic benchmark target: six-month gap equals roughly 18% of average income.
        gap=income*.18; horizon=6
        for key,value in [("control",cap),("treatment",treat_cap)]:
            if value>0: feasible[key]+=1
            projected[key]+=min(gap,value*horizon)
            if value*horizon>=gap: achieved[key]+=1
        reductions.append((treat_cap-cap)); count+=1
    result={"label":"Synthetic simulation — not real customer evidence","method":"Per-user six-month projection. Treatment applies an illustrative 8% reduction to synthetic shopping expenses; it is not observed customer behavior.",
      "sample_users":count,"control":{"goal_feasibility_pct":round(achieved["control"]/max(1,count)*100,1),"goals_achieved":achieved["control"],"projected_savings_per_user":round(projected["control"]/max(1,count),2),"users_with_positive_capacity_pct":round(feasible["control"]/max(1,count)*100,1)},
      "treatment":{"goal_feasibility_pct":round(achieved["treatment"]/max(1,count)*100,1),"goals_achieved":achieved["treatment"],"projected_savings_per_user":round(projected["treatment"]/max(1,count),2),"users_with_positive_capacity_pct":round(feasible["treatment"]/max(1,count)*100,1)},
      "mean_simulated_monthly_capacity_change":round(statistics.mean(reductions),2),"caveat":"This is an illustrative generated-data scenario, not an experiment and not a causal effect."}
    (DATA/"product_metrics.json").write_text(json.dumps(result,indent=2),encoding="utf-8")
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
