"""
Earned Value Management (EVM) Engine
Calculates all PMBOK-compliant EVM metrics per task and at project level.
"""

import pandas as pd
import numpy as np


def calculate_evm_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute EVM metrics for every row. Adds columns:
    EV, CV, SV, CPI, SPI, CV_pct, SV_pct, status
    """
    df = df.copy()

    # Core EVM formulas
    df["EV"] = df["PV"] * (df["Avance_Fisico"] / 100.0)
    df["CV"] = df["EV"] - df["AC"]                          # Cost Variance
    df["SV"] = df["EV"] - df["PV"]                          # Schedule Variance

    # Performance indices (guard against division by zero)
    df["CPI"] = np.where(df["AC"] > 0, df["EV"] / df["AC"], 1.0)
    df["SPI"] = np.where(df["PV"] > 0, df["EV"] / df["PV"], 1.0)

    # Percentage variances
    df["CV_pct"] = np.where(df["AC"] > 0, (df["CV"] / df["AC"]) * 100, 0.0)
    df["SV_pct"] = np.where(df["PV"] > 0, (df["SV"] / df["PV"]) * 100, 0.0)

    # Traffic-light status per task
    def _task_status(row) -> str:
        cpi, spi = row["CPI"], row["SPI"]
        if cpi >= 1.0 and spi >= 1.0:
            return "✅ En Control"
        elif cpi < 0.85 or spi < 0.85:
            return "🔴 Crítico"
        else:
            return "🟡 Atención"

    df["status"] = df.apply(_task_status, axis=1)

    # Round display columns
    for col in ["EV", "CV", "SV", "CPI", "SPI", "CV_pct", "SV_pct"]:
        df[col] = df[col].round(4)

    return df


def calculate_project_totals(df: pd.DataFrame) -> dict:
    """
    Aggregate project-level EVM metrics from the task-level DataFrame.
    """
    total_PV = df["PV"].sum()
    total_AC = df["AC"].sum()
    total_EV = df["EV"].sum()

    CPI = total_EV / total_AC if total_AC > 0 else 1.0
    SPI = total_EV / total_PV if total_PV > 0 else 1.0

    CV  = total_EV - total_AC
    SV  = total_EV - total_PV

    # EAC: Estimate at Completion based on current CPI performance
    EAC = total_PV / CPI if CPI > 0 else total_PV

    # TCPI: To-Complete Performance Index (effort needed to finish on budget)
    ETC = total_PV - total_EV          # Remaining planned work
    TCPI = ETC / (total_PV - total_AC) if (total_PV - total_AC) != 0 else 1.0

    # VAC: Variance at Completion
    VAC = total_PV - EAC

    # Overall physical progress
    avance_ponderado = (total_EV / total_PV * 100) if total_PV > 0 else 0.0

    return {
        "total_PV":          round(total_PV, 2),
        "total_AC":          round(total_AC, 2),
        "total_EV":          round(total_EV, 2),
        "CV":                round(CV, 2),
        "SV":                round(SV, 2),
        "CPI":               round(CPI, 4),
        "SPI":               round(SPI, 4),
        "EAC":               round(EAC, 2),
        "TCPI":              round(TCPI, 4),
        "VAC":               round(VAC, 2),
        "avance_ponderado":  round(avance_ponderado, 2),
        "n_tasks":           len(df),
        "n_critical":        int((df["CPI"] < 1).sum()),
        "n_delayed":         int((df["SPI"] < 1).sum()),
    }


def prepare_s_curve_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate PV, AC, EV by reporting date for the S-Curve.
    If a single date exists, returns a simple snapshot row.
    """
    agg = (
        df.groupby("Fecha_Reporte")[["PV", "AC", "EV"]]
        .sum()
        .reset_index()
        .sort_values("Fecha_Reporte")
    )
    # Cumulative sums
    agg["PV_cum"] = agg["PV"].cumsum()
    agg["AC_cum"] = agg["AC"].cumsum()
    agg["EV_cum"] = agg["EV"].cumsum()
    return agg


def get_pareto_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate CV by subcontractor, sorted by most negative (worst) first.
    Adds cumulative % for Pareto line.
    """
    grp = (
        df.groupby("Subcontratista")
        .agg(
            CV=("CV", "sum"),
            AC=("AC", "sum"),
            PV=("PV", "sum"),
            EV=("EV", "sum"),
            n_tasks=("task_id", "count"),
        )
        .reset_index()
    )
    grp["CPI"] = np.where(grp["AC"] > 0, grp["EV"] / grp["AC"], 1.0)
    # Sort: most negative CV first (biggest risk)
    grp = grp.sort_values("CV", ascending=True).reset_index(drop=True)
    # Pareto % cumulative of absolute negative deviation
    negative = grp[grp["CV"] < 0].copy()
    if not negative.empty:
        total_neg = negative["CV"].abs().sum()
        negative["cum_pct"] = (negative["CV"].abs().cumsum() / total_neg * 100).round(1)
        grp = grp.merge(negative[["Subcontratista", "cum_pct"]], on="Subcontratista", how="left")
    else:
        grp["cum_pct"] = 0.0
    return grp
