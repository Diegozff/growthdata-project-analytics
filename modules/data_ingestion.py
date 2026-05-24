"""
Data Ingestion & Validation Module
Handles file upload, column mapping, and data quality checks.
"""

import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO

# ── Column alias map ─────────────────────────────────────────────────────────
# Maps accepted user column names → internal canonical names
COLUMN_ALIASES: dict[str, list[str]] = {
    "task_id":        ["Codigo_EDT", "codigo_edt", "CODIGO_EDT",
                       "Tarea", "tarea", "TAREA", "Task", "task", "ID_Tarea"],
    "PV":             ["Presupuesto_Planificado", "presupuesto_planificado",
                       "PV", "pv", "Planned_Value", "Presupuesto"],
    "AC":             ["Costo_Real", "costo_real", "COSTO_REAL",
                       "AC", "ac", "Actual_Cost", "Costo_Ejecutado"],
    "Avance_Fisico":  ["Avance_Fisico", "avance_fisico", "AVANCE_FISICO",
                       "Progreso", "Progress", "Avance", "pct_avance", "% Avance"],
    "Fecha_Reporte":  ["Fecha_Reporte", "fecha_reporte", "FECHA_REPORTE",
                       "Fecha", "Date", "Periodo", "Reporting_Date"],
    "Subcontratista": ["Subcontratista_Responsable", "subcontratista_responsable",
                       "Subcontratista", "subcontratista", "Contractor",
                       "Responsable", "responsable"],
}

REQUIRED_CANONICAL = list(COLUMN_ALIASES.keys())


def _detect_column(df_cols: list[str], aliases: list[str]) -> str | None:
    """Return the first column name in df_cols that matches an alias."""
    lower_cols = {c.lower().strip(): c for c in df_cols}
    for alias in aliases:
        match = lower_cols.get(alias.lower().strip())
        if match:
            return match
    return None


def upload_and_validate(uploaded_file) -> tuple[pd.DataFrame | None, str | None]:
    """
    Read the uploaded file and validate required columns exist.
    Returns (DataFrame, None) on success or (None, error_message) on failure.
    """
    try:
        if uploaded_file.name.endswith(".csv"):
            # Try UTF-8 first, fall back to latin-1
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding="latin-1")
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            return None, "Formato de archivo no soportado. Use .csv, .xlsx o .xls."
    except Exception as exc:
        return None, f"No se pudo leer el archivo: {exc}"

    if df.empty:
        return None, "El archivo está vacío. Cargue un archivo con datos."

    # Strip whitespace from column names
    df.columns = [str(c).strip() for c in df.columns]

    # Check each required canonical column has at least one alias present
    missing: list[str] = []
    for canonical, aliases in COLUMN_ALIASES.items():
        found = _detect_column(list(df.columns), aliases)
        if not found:
            human_aliases = " / ".join(f"'{a}'" for a in aliases[:4])
            missing.append(f"**{canonical}** — columnas aceptadas: {human_aliases}")

    if missing:
        bullets = "\n".join(f"• {m}" for m in missing)
        return None, (
            "Faltan las siguientes columnas obligatorias en el archivo:\n\n"
            + bullets
            + "\n\nVerifique los nombres de columna o descargue la plantilla de ejemplo."
        )

    return df, None


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename detected aliases to canonical internal names and coerce dtypes.
    """
    rename_map: dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        found = _detect_column(list(df.columns), aliases)
        if found and found != canonical:
            rename_map[found] = canonical

    df = df.rename(columns=rename_map)

    # Coerce numeric columns
    for col in ["PV", "AC", "Avance_Fisico"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    # Clamp Avance_Fisico to [0, 100]
    df["Avance_Fisico"] = df["Avance_Fisico"].clip(0, 100)

    # Coerce date column
    df["Fecha_Reporte"] = pd.to_datetime(df["Fecha_Reporte"], errors="coerce")

    # Fill missing dates with today
    if df["Fecha_Reporte"].isna().any():
        df["Fecha_Reporte"] = df["Fecha_Reporte"].fillna(pd.Timestamp.today())

    # Ensure task_id is string
    df["task_id"] = df["task_id"].astype(str).str.strip()

    # Ensure subcontractor is string
    df["Subcontratista"] = df["Subcontratista"].astype(str).str.strip().replace("nan", "Sin Asignar")

    return df
