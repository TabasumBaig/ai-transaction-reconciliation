# 💳 AI Transaction Reconciliation System

## 📌 Overview
This project is a Python-based system that reconciles platform transactions with bank settlement records.

It identifies mismatches and provides clear explanations for each issue.

---

## 🚀 Features
- Detects Missing Settlements  
- Detects Missing Transactions  
- Identifies Duplicate Entries  
- Handles Rounding Differences  
- Detects Next-Month Settlements  
- Generates clean reconciliation report  

---

## ⚙️ Tech Stack
- Python
- Pandas
- Streamlit (for dashboard)

---

## 📂 Project Structure


---

## ▶️ How to Run

### Run reconciliation script:
```bash
cd src
python reconcile.py

cd tests
python test_cases.py

cd app
python -m streamlit run app.py

📊 Output
Generates final_report.csv
Displays categorized issues with explanations

🧪 Test Cases

The project includes automated test cases to validate:

Missing data detection
Duplicate handling
Rounding issues
Next-month settlement cases

💡 Assumptions
Transactions and settlements are linked by ID
Small differences (<0.01) are treated as rounding errors
Settlements may occur in the next month