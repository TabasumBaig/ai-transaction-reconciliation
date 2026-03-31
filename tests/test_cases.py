import pandas as pd

# Load final report
df = pd.read_csv("../data/final_report.csv")

# -------------------------------
# TEST 1: Check if file loaded
# -------------------------------
assert not df.empty, "❌ Report is empty"

# -------------------------------
# TEST 2: Missing Settlement exists
# -------------------------------
assert "Missing Settlement" in df["issue"].values, "❌ Missing Settlement case not detected"

# -------------------------------
# TEST 3: Missing Transaction exists
# -------------------------------
assert "Missing Transaction" in df["issue"].values, "❌ Missing Transaction case not detected"

# -------------------------------
# TEST 4: Rounding Difference exists
# -------------------------------
assert "Rounding Difference" in df["issue"].values, "❌ Rounding issue not detected"

# -------------------------------
# TEST 5: Duplicate Entry exists
# -------------------------------
assert "Duplicate Entry" in df["issue"].values, "❌ Duplicate not detected"

# -------------------------------
# TEST 6: Next Month Settlement exists
# -------------------------------
assert "Settled Next Month" in df["issue"].values, "❌ Next month settlement not detected"

# -------------------------------
# TEST 7: No unexpected null IDs
# -------------------------------
assert df["id"].notna().all(), "❌ Null IDs found"

# -------------------------------
# TEST 8: Summary sanity check
# -------------------------------
assert df.shape[0] >= 6, "❌ Data seems incomplete"

print("\n✅ ALL TEST CASES PASSED SUCCESSFULLY 🚀")