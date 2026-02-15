# 🧠 RetentionAI: Employee Churn Prediction System

## 💼 Business Problem
Employee turnover is one of the highest costs for HR departments. Replacing a key employee can cost up to **200% of their annual salary** due to recruitment fees, onboarding time, and lost productivity.

**The Challenge:** HR Managers react *after* an employee resigns. They lack a proactive tool to identify "at-risk" talent before it's too late.

## 🎯 The Solution
**RetentionAI** is a Full-Stack Machine Learning application that:
1.  **Predicts** the probability of an employee leaving (Churn Risk).
2.  **Identifies** key drivers of dissatisfaction (e.g., Low Salary, Lack of Promotion, Overtime).
3.  **Simulates** retention strategies (e.g., "If we increase salary by 10%, does the risk drop?").

## 🏗️ Architecture & Tech Stack
This project follows MLOps best practices, decoupling the model training from the inference API.

* **Data Processing:** Pandas & Scikit-Learn Pipelines (Custom Transformers).
* **Model:** Random Forest / XGBoost (Supervised Classification).
* **Backend/API:** FastAPI (Future implementation).
* **Frontend:** Streamlit (Interactive Dashboard).
* **Containerization:** Docker.

## 📊 Project Structure
```text
retention-ai/
├── data/          # Raw and processed data (Git ignored)
├── notebooks/     # Experimental Analysis (EDA)
├── src/           # Production Source Code
│   ├── data/      # Data loading logic
│   ├── features/  # Feature Engineering pipelines
│   └── models/    # Training and Evaluation scripts
├── models/        # Serialized models (.pkl)
└── app/           # Streamlit Frontend application