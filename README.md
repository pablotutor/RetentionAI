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
* **Model:** Logistic Regression / Random Forest / XGBoost (Supervised Classification).
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
```

## 🚀 How to Run (Docker)

The easiest way to run the application is using Docker to avoid environment issues.

1. **Build the image:**
```bash
docker build -t retention-ai .

```


2. **Run the container:**
```bash
docker run -p 8501:8501 retention-ai

```


3. **Access the App:**
Open your browser at `http://localhost:8501`



## 🔮 Roadmap & Future Improvements

This project is currently a functional prototype. The following features are planned for the next release (v2.0):

### 1. Enhanced UI/UX

* **Dark Mode Fixes:** Optimize CSS styles to ensure full compatibility with Streamlit's dark theme (currently optimized for light mode).
* **Nuanced Risk Levels:** Move beyond binary (High/Low) classification. Implement a tiered system: *Low Risk* (Green), *Moderate Watchlist* (Yellow), *High Risk* (Red).

### 2. Advanced Batch Capabilities

* **Drill-Down Analysis:** Make the Batch table interactive. Clicking on a high-risk employee should redirect to the "Individual Analysis" page with their data pre-loaded to simulate specific retention scenarios.
* **Bulk Actions:** Select multiple employees to generate a PDF report for department heads.

### 3. Enterprise Integration

* **SQL Database:** Migrate from CSV uploads to a persistent SQL database (PostgreSQL) to store employee history and track risk evolution over time.
* **Direct Action (Microsoft Teams/Slack):** Add a "Schedule Meeting" button next to high-risk profiles that integrates with the company calendar API to set up 1-on-1 retention interviews immediately.

### 4. API Decoupling

* Migrate the inference logic from the Streamlit app to a standalone **FastAPI** microservice to allow other internal tools to consume the churn predictions.

---

*Built with ❤️ by Pablo*