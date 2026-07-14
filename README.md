# Brent Oil Price Analysis

## Project Overview

This project analyzes how major political and economic events affect Brent oil prices using **change point detection** and **Bayesian statistical modeling**. The analysis covers daily Brent oil prices from **May 20, 1987, to September 30, 2022**.

### Business Problem

The oil market is highly volatile, making it difficult for investors, policymakers, and energy companies to make informed decisions. This project provides data-driven insights to:
- Identify key events impacting oil prices
- Quantify the magnitude of price changes
- Guide investment strategies and policy development

### Key Objectives

1. Identify significant events affecting Brent oil prices
2. Quantify event impacts using statistical methods
3. Provide actionable insights for stakeholders

---

## Project Structure

brent-oil-price-analysis/
├── data/
│   ├── brent_oil_prices.csv         # Raw data
│   ├── cleaned_brent_oil_prices.csv # Processed data
│   ├── key_events.csv               # Events dataset
│   └── event_impacts.csv            # Impact analysis
├── notebooks/
│   ├── 01_data_exploration.ipynb    # Task 1: EDA
│   ├── 02_change_point_modeling.ipynb # Task 2: Change Point
│   └── 03_advanced_analysis.ipynb   # Task 3: Advanced
├── src/
│   ├── data_loader.py               # Data loading utilities
│   ├── change_point_model.py        # Bayesian modeling
│   └── visualization.py             # Plotting functions
├── backend/                         # Flask API
│   ├── app.py
│   ├── api.py
│   └── data_loader.py
├── frontend/                        # React Dashboard
│   └── src/
│       ├── App.js
│       ├── components/
│       └── services/
├── figures/                         # Generated visualizations
├── docs/
│   └── interim_report.md            # Task 1 Report
├── requirements.txt
└── README.md

---

## Dataset

### Brent Oil Prices
- **Source**: Historical daily oil prices
- **Period**: May 20, 1987 – September 30, 2022
- **Records**: 9,011 daily observations
- **Fields**: Date, Price (USD/barrel)

### Events Dataset
20+ major events compiled including:
- Geopolitical conflicts (Gulf Wars, Russia-Ukraine)
- OPEC policy decisions
- Economic crises (2008 Financial Crisis, COVID-19)
- International sanctions

---

## 🔬 Methodology

### 1. Exploratory Data Analysis
- Trend analysis and visualization
- Stationarity testing (ADF, KPSS)
- Volatility analysis
- Event impact assessment

### 2. Change Point Detection
- **Bayesian approach** using PyMC
- Identification of structural breaks
- 95% credible intervals
- Event association

### 3. Interactive Dashboard
- **Backend**: Flask REST API
- **Frontend**: React with Recharts
- Features: Price chart, event filtering, impact analysis

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### Installation

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python app.py
```

#### Frontend Setup
```bash
cd frontend
npm install
npm start
```

#### Run Notebooks
```bash
jupyter notebook notebooks/
```

---

## Key Findings

| Metric | Value |
|---|---|
| Average Price | $48.42 |
| Min Price | $9.10 |
| Max Price | $143.95 |
| Total Records | 9,011 |

### Top Event Impacts

| Event | Price Change | % Change |
|---|---|---|
| Russia-Ukraine War | +$17.10 | +17.45% |
| Iraq Invades Kuwait | +$7.01 | +37.16% |
| Global Financial Crisis | -$6.33 | -6.24% |

---

## Technologies

- **Python**: Pandas, NumPy, PyMC, Matplotlib, Seaborn
- **Statistics**: SciPy, Statsmodels
- **Backend**: Flask, Flask-CORS
- **Frontend**: React, Recharts, Axios
- **Notebooks**: Jupyter
- **Version Control**: Git, GitHub

---

## Team

- **Tutors**: Kerod, Feven, Mahbubah
- **Student**: Nardos Tsige

---

## Key Dates

| Milestone | Date |
|---|---|
| Challenge Introduction | July 8, 2026 |
| Interim Submission | July 12, 2026 |
| Final Submission | July 14, 2026 |

---

## License

MIT License

---

## Links

- [GitHub Repository](#)
- [Live Dashboard](#)
- [API Documentation](#)

---

## Acknowledgments

- Data source for Brent oil prices
- PyMC and ArviZ for Bayesian modeling
- Open-source community for tools and libraries
