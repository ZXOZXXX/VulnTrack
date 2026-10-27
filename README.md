# 🛡️ VulnTrack — Vulnerability Management System

<p align="center">
  <strong>A Python-Based Cybersecurity Project Powered by Design and Analysis of Algorithms</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-Web%20Application-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-Data%20Visualization-3F4F75?logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Testing-pytest-0A9EDC?logo=pytest&logoColor=white" alt="pytest">
  <img src="https://img.shields.io/badge/Domain-Cybersecurity-darkgreen" alt="Cybersecurity">
</p>

---

## 🔍 About the Project

**VulnTrack** is a Python-based vulnerability management application designed to record, analyze, and prioritize security vulnerabilities using risk-based assessment and fundamental **Design and Analysis of Algorithms (DAA)** techniques.

The application combines cybersecurity concepts with algorithmic problem-solving to help users identify higher-priority vulnerabilities and organize remediation efforts.

## 🎯 Project Objectives

- Develop an organized vulnerability management application.
- Calculate risk scores using vulnerability-related assessment factors.
- Classify vulnerabilities into priority categories.
- Implement Linear Search for efficient record lookup.
- Implement Merge Sort for risk-score-based sorting.
- Present vulnerability information through an interactive Streamlit interface.
- Validate application functionality using automated tests.

## ✨ Key Features

| Feature | Description |
|---|---|
| 🛡️ Vulnerability Management | Maintain and manage vulnerability records. |
| 📊 Risk Score Calculation | Evaluate vulnerabilities using defined risk factors. |
| 🚦 Priority Classification | Categorize findings according to risk score thresholds. |
| 🔎 Linear Search | Search for vulnerabilities using their IDs. |
| ⚙️ Merge Sort | Sort vulnerabilities by risk score. |
| 📈 Interactive Dashboard | Display vulnerability information and visualizations. |
| 🧪 Automated Testing | Verify functionality using pytest. |

## 🧠 Design and Analysis of Algorithms (DAA)

### 1. Linear Search

Linear Search checks records one by one until the target vulnerability ID is found or the list ends.

- **Best case:** O(1)
- **Average case:** O(n)
- **Worst case:** O(n)

### 2. Merge Sort

Merge Sort divides a list into smaller sublists, sorts them recursively, and merges the results into sorted order.

- **Best case:** O(n log n)
- **Average case:** O(n log n)
- **Worst case:** O(n log n)
- **Auxiliary space:** O(n) for a typical array-based implementation

### 3. Risk-Based Prioritization

VulnTrack uses a risk-scoring model to help determine which vulnerability records require greater attention. Priority classification is based on the thresholds implemented in the project.

## 🧰 Technology Stack

- **Programming Language:** Python
- **Web Interface:** Streamlit
- **Visualization:** Plotly
- **Testing Framework:** pytest
- **Development Environment:** Visual Studio Code
- **Version Control:** Git and GitHub

## 📁 Project Structure

```text
VulnTrack/
│
├── algorithms/
│   ├── linear_search.py
│   └── merge_sort.py
│
├── data/
│   └── database.py
│
├── models/
│   └── vulnerability.py
│
├── services/
│   └── vulnerability_service.py
│
├── tests/
│   └── test_vulnerability.py
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

*Note: Update the tree if your actual filenames differ.*

## 🚀 Installation and Setup

### Prerequisites

- Python 3.12 or another compatible Python version
- pip package manager
- Git (optional)

### Step 1: Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/VulnTrack.git
cd VulnTrack
```

Replace `YOUR-USERNAME` with your GitHub username.

### Step 2: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
streamlit run app.py
```

The application will provide a local URL in the terminal. Open it in your browser.

### Step 5: Run Automated Tests

```bash
python -m pytest -v
```

## 📸 Application Screenshots

Add screenshots of your actual running application in the `screenshots/` directory.

### Dashboard
<!-- Add your dashboard screenshot here -->
<!-- Example: ![VulnTrack Dashboard](screenshots/dashboard.png) -->

### Vulnerability Management
<!-- Add your vulnerability management screenshot here -->
<!-- Example: ![Vulnerability Management](screenshots/vulnerability-management.png) -->

### Search and Sorting
<!-- Add your Linear Search and Merge Sort screenshots here -->

### Automated Testing
<!-- Add a screenshot of the actual passing pytest output here -->

## 🧪 Testing and Validation

The project uses pytest to validate key functionality, including:

- Risk score calculation.
- Priority classification.
- Vulnerability record operations.
- Search and sorting behavior, where covered by the test suite.

Only report test results that have actually been run and verified.

## 🔮 Future Enhancements

- Advanced vulnerability analytics.
- Exportable vulnerability assessment reports.
- Enhanced filtering and search.
- Improved dashboard visualizations.
- Additional security assessment and reporting features.

## 👨‍💻 Author

**Arpit Paliwal**

Master of Computer Applications (MCA)

**Project:** VulnTrack — Vulnerability Management System

---

<p align="center">
  <strong>Built to connect Cybersecurity, Python, and Algorithmic Problem-Solving.</strong>
</p>
