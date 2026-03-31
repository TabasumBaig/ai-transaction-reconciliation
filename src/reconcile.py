import pandas as pd

# -------------------------------
# 1. Load Data
# -------------------------------
transactions = pd.read_csv("../data/transactions.csv")
settlements = pd.read_csv("../data/settlements.csv")

# Convert dates
transactions['date'] = pd.to_datetime(transactions['date'])
settlements['date'] = pd.to_datetime(settlements['date'])

# -------------------------------
# 2. Detect Duplicate Entries
# -------------------------------
duplicate_ids = settlements[settlements.duplicated(subset=['id'], keep=False)].copy()
duplicate_ids['issue'] = "Duplicate Entry"

# -------------------------------
# 3. Merge Data
# -------------------------------
df = transactions.merge(
    settlements,
    on="id",
    how="outer",
    suffixes=("_txn", "_bank")
)

# -------------------------------
# 4. Identify Issues
# -------------------------------
df["issue"] = "Matched"

# Missing cases
df.loc[df["amount_txn"].isna(), "issue"] = "Missing Transaction"
df.loc[df["amount_bank"].isna(), "issue"] = "Missing Settlement"

# Rounding difference (VERY IMPORTANT FIX)
df.loc[
    (df["amount_txn"].notna()) &
    (df["amount_bank"].notna()) &
    (abs(df["amount_txn"] - df["amount_bank"]) > 0) &
    (abs(df["amount_txn"] - df["amount_bank"]) < 0.01),
    "issue"
] = "Rounding Difference"

# Next month settlement
df.loc[
    (df["date_txn"].notna()) &
    (df["date_bank"].notna()) &
    (
        (df["date_bank"].dt.month != df["date_txn"].dt.month) |
        (df["date_bank"].dt.year != df["date_txn"].dt.year)
    ),
    "issue"
] = "Settled Next Month"

# Exact mismatch (important addition 🔥)
df.loc[
    (df["amount_txn"].notna()) &
    (df["amount_bank"].notna()) &
    (abs(df["amount_txn"] - df["amount_bank"]) >= 0.01),
    "issue"
] = "Amount Mismatch"

# -------------------------------
# 5. Clean Report
# -------------------------------
report = df[['id', 'amount_txn', 'amount_bank', 'date_txn', 'date_bank', 'issue']].copy()

# -------------------------------
# 6. Add Explanation Column
# -------------------------------
def explain(issue):
    explanations = {
        "Matched": "Transaction and settlement match correctly",
        "Missing Settlement": "Transaction exists but not settled in bank",
        "Missing Transaction": "Settlement exists without original transaction",
        "Rounding Difference": "Minor difference due to rounding",
        "Duplicate Entry": "Same transaction recorded multiple times",
        "Settled Next Month": "Settlement recorded in next month (timing delay)",
        "Amount Mismatch": "Amounts differ significantly"
    }
    return explanations.get(issue, "Unknown issue")

report["explanation"] = report["issue"].apply(explain)

# -------------------------------
# 7. Add Duplicate Rows
# -------------------------------
if not duplicate_ids.empty:
    duplicate_ids = duplicate_ids.rename(columns={"amount": "amount_bank", "date": "date_bank"})
    duplicate_ids["amount_txn"] = None
    duplicate_ids["date_txn"] = None

    duplicate_ids = duplicate_ids[['id', 'amount_txn', 'amount_bank', 'date_txn', 'date_bank', 'issue']]
    duplicate_ids["explanation"] = duplicate_ids["issue"].apply(explain)

    report = pd.concat([report, duplicate_ids], ignore_index=True)

# -------------------------------
# 8. Sort Report (clean view)
# -------------------------------
report = report.sort_values(by="issue")

# -------------------------------
# 9. Print Output
# -------------------------------
print("\n==== FINAL RECONCILIATION REPORT ====\n")
print(report)

# -------------------------------
# 10. Summary (VERY IMPORTANT)
# -------------------------------
print("\n==== SUMMARY ====\n")
print(report['issue'].value_counts())

# -------------------------------
# 11. Save Output
# -------------------------------
report.to_csv("../data/final_report.csv", index=False)

print("\n✅ Final report saved as final_report.csv")