"""
Sample data generator for GrowthData Analytics demo.
Produces a realistic construction project EVM dataset.
"""

import pandas as pd
import numpy as np
import io


def generate_sample_dataframe() -> pd.DataFrame:
    np.random.seed(42)

    subcontractors = [
        "Constructora Vial S.A.",
        "Ingeniería Estructural XYZ",
        "Hidráulica & Sanitaria Ltda.",
        "Electromecánica Industrial Corp.",
        "Montajes Metálicos del Norte",
        "Terraforming Solutions",
        "Concretos & Prefabricados SA",
    ]

    tasks = [
        # (code, name, PV, subcontractor_idx, scenario)
        ("EDT-1.1", "Replanteo y Topografía",         45_000,  5, "healthy"),
        ("EDT-1.2", "Movimiento de Tierras",          320_000,  5, "slight_over"),
        ("EDT-1.3", "Relleno y Compactación",         180_000,  5, "healthy"),
        ("EDT-2.1", "Pilotes y Fundaciones",          850_000,  1, "critical"),
        ("EDT-2.2", "Vigas de Cimentación",           420_000,  1, "slight_over"),
        ("EDT-2.3", "Muros de Contención",            210_000,  6, "healthy"),
        ("EDT-3.1", "Estructura Metálica Principal",  980_000,  4, "critical"),
        ("EDT-3.2", "Cubierta y Cerramiento",         540_000,  4, "slight_over"),
        ("EDT-3.3", "Losas y Entrepisos",             460_000,  6, "healthy"),
        ("EDT-4.1", "Instalaciones Eléctricas HV",   620_000,  3, "critical"),
        ("EDT-4.2", "Instalaciones Eléctricas LV",   340_000,  3, "slight_over"),
        ("EDT-4.3", "Sistemas de Control",            290_000,  3, "healthy"),
        ("EDT-5.1", "Tuberías Proceso Industrial",   410_000,  2, "critical"),
        ("EDT-5.2", "Instrumentación y Medición",    380_000,  2, "slight_over"),
        ("EDT-5.3", "Red de Incendios",              160_000,  2, "healthy"),
        ("EDT-6.1", "Acabados y Revestimientos",     220_000,  0, "healthy"),
        ("EDT-6.2", "Pintura Industrial",            145_000,  0, "slight_over"),
        ("EDT-7.1", "Vialidad Interna",              280_000,  5, "healthy"),
        ("EDT-7.2", "Señalización y Demarcación",     75_000,  5, "healthy"),
        ("EDT-8.1", "Pruebas y Comisionamiento",     350_000,  3, "delayed"),
    ]

    # ── Multi-period dataset: 6 monthly snapshots ─────────────────────────
    periods = pd.date_range("2024-01-31", periods=6, freq="ME")
    records = []

    for task_code, task_name, pv_total, sub_idx, scenario in tasks:
        for period_idx, period_date in enumerate(periods):
            progress_factor = (period_idx + 1) / len(periods)

            if scenario == "healthy":
                avance   = min(100, round(progress_factor * 100 * np.random.uniform(0.95, 1.05), 1))
                ac_ratio = np.random.uniform(0.92, 0.98)

            elif scenario == "slight_over":
                avance   = min(100, round(progress_factor * 100 * np.random.uniform(0.88, 0.97), 1))
                ac_ratio = np.random.uniform(1.04, 1.12)

            elif scenario == "critical":
                avance   = min(100, round(progress_factor * 100 * np.random.uniform(0.70, 0.85), 1))
                ac_ratio = np.random.uniform(1.15, 1.35)

            elif scenario == "delayed":
                avance   = min(100, round(progress_factor * 100 * np.random.uniform(0.60, 0.75), 1))
                ac_ratio = np.random.uniform(0.96, 1.02)

            # PV for this period (proportional)
            pv_period = pv_total * progress_factor
            ev_period = pv_period * (avance / 100)
            ac_period = ev_period * ac_ratio

            records.append({
                "Codigo_EDT":                task_code,
                "Tarea":                     task_name,
                "Presupuesto_Planificado":   round(pv_period, 2),
                "Costo_Real":                round(ac_period, 2),
                "Avance_Fisico":             avance,
                "Fecha_Reporte":             period_date.strftime("%Y-%m-%d"),
                "Subcontratista_Responsable": subcontractors[sub_idx],
                "Unidad":                    "Global",
                "Fase":                      task_code.split("-")[0] + "-" + task_code.split(".")[0][-1],
            })

    return pd.DataFrame(records)


def generate_sample_csv() -> bytes:
    df  = generate_sample_dataframe()
    buf = io.BytesIO()
    df.to_csv(buf, index=False, encoding="utf-8")
    return buf.getvalue()


def generate_sample_excel() -> bytes:
    df  = generate_sample_dataframe()
    buf = io.BytesIO()
    df.to_excel(buf, index=False, engine="openpyxl")
    return buf.getvalue()


if __name__ == "__main__":
    df = generate_sample_dataframe()
    df.to_csv("sample_project_data.csv", index=False)
    print(f"Generated {len(df)} rows across {df['Fecha_Reporte'].nunique()} periods.")
    print(df.head())
