# GrowthData Analytics LLC — Project Controls Platform

> **Earned Value Management (EVM) Dashboard for Construction & Industrial Infrastructure**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red)](https://streamlit.io)
[![PMBOK](https://img.shields.io/badge/PMBOK-7th%20Ed.-orange)](https://www.pmi.org)

---

## Overview

A professional Project Controls platform that allows a **Project Manager or Director de Obra** to upload a CSV/Excel file with construction site data and automatically generate:

- **EVM Dashboard** — KPI cards with CPI, SPI, EV, AC, PV, EAC, VAC, TCPI
- **S-Curve** — Cumulative PV / AC / EV over time
- **Quadrant Map** — SPI vs CPI scatter to identify critical tasks
- **Subcontractor Pareto** — Who is eroding project margin
- **Executive Reports** — Styled Excel (3 sheets) + PDF with signatures

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USER/growthdata-project-analytics.git
cd growthdata-project-analytics

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch
streamlit run app.py --server.port 8502
```

Open **http://localhost:8502** in your browser.

Or on Windows, double-click **`iniciar.bat`**.

---

## Required CSV/Excel Columns

| Column | Aliases accepted | Description |
|--------|-----------------|-------------|
| `Codigo_EDT` | `Tarea`, `Task` | Work breakdown structure ID |
| `Presupuesto_Planificado` | `PV`, `Planned_Value` | Planned budget per task |
| `Costo_Real` | `AC`, `Actual_Cost` | Real executed cost |
| `Avance_Fisico` | `Progreso`, `Progress` | Physical progress 0–100 |
| `Fecha_Reporte` | `Date`, `Periodo` | Reporting date |
| `Subcontratista_Responsable` | `Subcontratista`, `Contractor` | Responsible company |

Download the sample template directly from the app sidebar.

---

## EVM Formulas (PMBOK 7th Ed.)

| Metric | Formula | Interpretation |
|--------|---------|---------------|
| **EV** | PV × (Avance / 100) | Earned Value |
| **CV** | EV − AC | Cost Variance (negative = over budget) |
| **SV** | EV − PV | Schedule Variance (negative = delayed) |
| **CPI** | EV / AC | < 1.0 = over budget ⚠️ |
| **SPI** | EV / PV | < 1.0 = behind schedule ⚠️ |
| **EAC** | BAC / CPI | Estimate at Completion |
| **VAC** | BAC − EAC | Variance at Completion |
| **TCPI** | (BAC−EV) / (BAC−AC) | Performance needed to finish on budget |

---

## Project Structure

```
growthdata-project-analytics/
├── app.py                          # Main Streamlit orchestrator
├── iniciar.bat                     # Windows launcher (double-click)
├── requirements.txt
├── modules/
│   ├── data_ingestion.py           # File upload & column validation
│   ├── evm_calculator.py           # EVM engine (PMBOK-compliant)
│   ├── visualizations.py           # Plotly charts (dark theme)
│   ├── export.py                   # Excel + PDF report generation
│   └── ui_components.py            # CSS, KPI cards, alerts
├── sample_data/
│   └── generate_sample.py          # 120-row demo dataset generator
└── .streamlit/
    └── config.toml                 # Dark theme configuration
```

---

## Tech Stack

- **UI:** Streamlit 1.32+
- **Data:** Pandas + NumPy
- **Charts:** Plotly (interactive, dark corporate theme)
- **Excel export:** xlsxwriter (styled, multi-sheet)
- **PDF export:** fpdf2
- **Standard:** PMBOK® 7th Edition EVM

---

*GrowthData Analytics LLC — Project Controls Platform v2.0*
