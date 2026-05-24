"""
GrowthData Analytics LLC
Project Controls & Earned Value Management Platform
Construction & Industrial Infrastructure

Entry point: streamlit run app.py
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ── Page config MUST be first Streamlit call ─────────────────────────────────
st.set_page_config(
    page_title="GrowthData Analytics | Project Controls",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Internal modules ──────────────────────────────────────────────────────────
from modules.ui_components    import apply_custom_css, render_kpi_card, render_section_header, render_alert
from modules.data_ingestion   import upload_and_validate, normalize_columns
from modules.evm_calculator   import calculate_evm_metrics, calculate_project_totals, prepare_s_curve_data, get_pareto_data
from modules.visualizations   import plot_s_curve, plot_scatter_quadrant, plot_pareto_subcontractors, plot_project_gauge
from modules.export           import export_to_excel, export_to_pdf
from sample_data.generate_sample import generate_sample_csv, generate_sample_excel

apply_custom_css()

# ── Logo path ─────────────────────────────────────────────────────────────────
LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo GrowthData Project Analytics.png")

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
col_logo, col_title, col_date = st.columns([1.2, 5, 2])

with col_logo:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, width=110)
    else:
        st.markdown('<div style="font-size:3.5rem;text-align:center;padding-top:4px;">🏗️</div>',
                    unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div style="padding: 6px 0 0 0;">
        <h1 style="color:#E8921C;margin:0;font-size:1.9rem;font-weight:700;letter-spacing:-0.5px;">
            GrowthData Analytics LLC
        </h1>
        <p style="color:#8FA8C8;margin:4px 0 0 0;font-size:0.88rem;font-weight:400;">
            Project Controls &amp; Earned Value Management &nbsp;|&nbsp;
            Construction &amp; Industrial Infrastructure
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_date:
    st.markdown(f"""
    <div style="text-align:right;padding:10px 4px 0 0;">
        <p style="color:#E8921C;margin:0;font-size:0.75rem;font-weight:600;text-transform:uppercase;
                  letter-spacing:1px;">Sistema de Control de Proyectos</p>
        <p style="color:#8FA8C8;margin:4px 0 0 0;font-size:0.78rem;">
            {datetime.now().strftime('%d/%m/%Y  %H:%M')}
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:8px 0 16px 0;border-bottom:1px solid #1A3060;">
        <h2 style="color:#E8921C;font-size:1rem;font-weight:600;margin:0;">⚙️ Panel de Control</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**📂 Carga de Datos**")

    uploaded_file = st.file_uploader(
        "Archivo de reporte de obra",
        type=["csv", "xlsx", "xls"],
        help="Formatos: CSV (.csv) o Excel (.xlsx / .xls). Tamaño máximo: 200 MB.",
    )

    st.markdown("---")
    st.markdown("**📋 Plantilla de Ejemplo**")

    col_csv, col_xl = st.columns(2)
    with col_csv:
        st.download_button(
            "📄 CSV",
            data=generate_sample_csv(),
            file_name="muestra_proyecto.csv",
            mime="text/csv",
            use_container_width=True,
            help="Descarga un CSV de ejemplo con 120 filas y 6 períodos",
        )
    with col_xl:
        st.download_button(
            "📊 Excel",
            data=generate_sample_excel(),
            file_name="muestra_proyecto.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    st.markdown("---")

    # Filters — populated only after data load (see below)
    filter_placeholder = st.empty()

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.7rem;color:#2A4470;text-align:center;line-height:1.7;">
        <strong style="color:#E8921C;font-weight:700;">GrowthData Analytics LLC</strong><br>
        Project Controls Platform v2.0<br>
        PMBOK® 7th Ed. Compliant<br>
        © 2024 Todos los derechos reservados
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LANDING PAGE (no file uploaded)
# ══════════════════════════════════════════════════════════════════════════════
if uploaded_file is None:
    st.markdown("""
    <div style="text-align:center;padding:50px 20px 30px 20px;">
        <div style="font-size:5rem;margin-bottom:16px;">📊</div>
        <h2 style="color:#E8921C;font-size:1.6rem;margin:0 0 12px 0;">
            Plataforma de Control de Proyectos de Construcción
        </h2>
        <p style="color:#8FA8C8;max-width:640px;margin:0 auto;line-height:1.8;font-size:0.95rem;">
            Cargue su archivo de reporte en el panel lateral para generar automáticamente
            el dashboard ejecutivo con análisis EVM completo, Curva S, análisis de
            subcontratistas y proyecciones de cierre del proyecto.
        </p>
    </div>
    """, unsafe_allow_html=True)

    features = [
        ("🔢", "Motor EVM Completo",
         "CPI, SPI, CV, SV, EAC, VAC, TCPI calculados automáticamente conforme a PMBOK® 7ª Ed."),
        ("📈", "Curva S en Tiempo Real",
         "Evolución temporal acumulada de PV, AC y EV para análisis de tendencias de proyecto."),
        ("⚠️", "Alertas Semafóricas",
         "Identificación automática por cuadrantes de tareas y subcontratistas en zona crítica."),
        ("📊", "Análisis de Subcontratistas",
         "Pareto de desvíos para identificar quién está licuando el margen de la obra."),
        ("🔮", "Proyección Ejecutiva",
         "Estimación del costo final (EAC) basada en el rendimiento real del proyecto."),
        ("📄", "Exportación Profesional",
         "Reportes ejecutivos en Excel estilizado y PDF con firmas para presentaciones gerenciales."),
    ]

    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div style="background:linear-gradient(145deg,#0F2144,#0A1628);
                        border:1px solid #1B3566;border-top:2px solid #E8921C;border-radius:14px;
                        padding:22px 18px;text-align:center;
                        margin-bottom:16px;min-height:170px;">
                <div style="font-size:2.2rem;margin-bottom:10px;">{icon}</div>
                <h4 style="color:#E8921C;margin:0 0 8px 0;font-size:0.95rem;">{title}</h4>
                <p style="color:#8FA8C8;font-size:0.8rem;margin:0;line-height:1.6;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:linear-gradient(135deg,rgba(26,58,110,0.5),rgba(13,31,53,0.5));
                border:1px solid #1B3566;border-radius:12px;border-top:2px solid #E8921C;padding:18px 24px;margin-top:10px;">
        <h4 style="color:#E8921C;margin:0 0 12px 0;">📋 Columnas Requeridas en el Archivo</h4>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;">
            <div style="color:#E8EDF5;font-size:0.82rem;">
                <code style="color:#E8921C;">Codigo_EDT</code> o <code style="color:#E8921C;">Tarea</code>
                <br><span style="color:#8FA8C8;font-size:0.75rem;">ID del componente de obra</span>
            </div>
            <div style="color:#E8EDF5;font-size:0.82rem;">
                <code style="color:#E8921C;">Presupuesto_Planificado</code> o <code style="color:#E8921C;">PV</code>
                <br><span style="color:#8FA8C8;font-size:0.75rem;">Costo teórico planificado</span>
            </div>
            <div style="color:#E8EDF5;font-size:0.82rem;">
                <code style="color:#E8921C;">Costo_Real</code> o <code style="color:#E8921C;">AC</code>
                <br><span style="color:#8FA8C8;font-size:0.75rem;">Gasto ejecutado real</span>
            </div>
            <div style="color:#E8EDF5;font-size:0.82rem;">
                <code style="color:#E8921C;">Avance_Fisico</code>
                <br><span style="color:#8FA8C8;font-size:0.75rem;">Progreso 0–100%</span>
            </div>
            <div style="color:#E8EDF5;font-size:0.82rem;">
                <code style="color:#E8921C;">Fecha_Reporte</code>
                <br><span style="color:#8FA8C8;font-size:0.75rem;">Dimensión temporal</span>
            </div>
            <div style="color:#E8EDF5;font-size:0.82rem;">
                <code style="color:#E8921C;">Subcontratista_Responsable</code>
                <br><span style="color:#8FA8C8;font-size:0.75rem;">Empresa ejecutora</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — DATA INGESTION & VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
with st.spinner("Validando y procesando datos del proyecto..."):
    df_raw, error_msg = upload_and_validate(uploaded_file)

if error_msg:
    st.markdown(f"""
    <div style="background:rgba(231,76,60,0.12);border:1px solid #E74C3C;
                border-left:5px solid #E74C3C;border-radius:10px;
                padding:20px 24px;margin:20px 0;">
        <h3 style="color:#E74C3C;margin:0 0 10px 0;">❌ Error de Validación de Datos</h3>
        <p style="color:#E8EDF5;margin:0;white-space:pre-line;">{error_msg}</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("💡 Descargue la **plantilla de ejemplo** desde el panel lateral para ver el formato correcto.")
    st.stop()

# ── Normalize & EVM calculation ───────────────────────────────────────────────
df = normalize_columns(df_raw.copy())

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR FILTERS (now that df is loaded)
# ══════════════════════════════════════════════════════════════════════════════
with filter_placeholder.container():
    st.markdown("**🔍 Filtros de Análisis**")

    dates      = sorted(df["Fecha_Reporte"].dt.date.unique())
    has_multi  = len(dates) > 1

    if has_multi:
        date_range = st.select_slider(
            "Período",
            options=dates,
            value=(dates[0], dates[-1]),
            format_func=lambda d: d.strftime("%d/%m/%Y"),
        )
        df_filtered = df[
            (df["Fecha_Reporte"].dt.date >= date_range[0]) &
            (df["Fecha_Reporte"].dt.date <= date_range[1])
        ].copy()
    else:
        st.caption(f"Período único: {dates[0].strftime('%d/%m/%Y')}")
        df_filtered = df.copy()

    subcontractors = ["Todos"] + sorted(df["Subcontratista"].unique().tolist())
    selected_sub   = st.selectbox("Subcontratista", subcontractors)
    if selected_sub != "Todos":
        df_filtered = df_filtered[df_filtered["Subcontratista"] == selected_sub]

    show_critical = st.checkbox("Solo Tareas Críticas (CPI < 1)", value=False)
    if show_critical:
        df_filtered_view = df_filtered[calculate_evm_metrics(df_filtered)["CPI"] < 1].copy()
    else:
        df_filtered_view = df_filtered.copy()

    st.markdown(f"<span style='color:#8FA8C8;font-size:0.78rem;'>**{len(df_filtered_view)}** tareas en vista</span>",
                unsafe_allow_html=True)

# ── EVM on full filtered data ─────────────────────────────────────────────────
df_evm    = calculate_evm_metrics(df_filtered)
totals    = calculate_project_totals(df_evm)

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — KPI CARDS
# ══════════════════════════════════════════════════════════════════════════════
render_section_header(
    "📊 Indicadores Clave de Rendimiento — EVM",
    f"Métricas consolidadas · {totals['n_tasks']} tareas analizadas · "
    f"Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
)

kpi_col = st.columns(6)
with kpi_col[0]:
    render_kpi_card(
        "Presupuesto Planificado", "PV — Budget at Completion",
        f"${totals['total_PV']:,.0f}", "📋", "neutral",
    )
with kpi_col[1]:
    render_kpi_card(
        "Costo Real Ejecutado", "AC — Actual Cost",
        f"${totals['total_AC']:,.0f}", "💰", "neutral",
    )
with kpi_col[2]:
    render_kpi_card(
        "Valor Ganado", "EV — Earned Value",
        f"${totals['total_EV']:,.0f}", "🎯", "neutral",
    )
with kpi_col[3]:
    status_cpi = "healthy" if totals["CPI"] >= 1 else ("critical" if totals["CPI"] < 0.85 else "warning")
    render_kpi_card(
        "Índ. Rendimiento Costo", "CPI — Cost Performance Index",
        f"{totals['CPI']:.3f}", "💹", status_cpi,
        "✅ Bajo Presupuesto" if totals["CPI"] >= 1 else f"🔴 Sobrecosto {(1-totals['CPI'])*100:.1f}%",
    )
with kpi_col[4]:
    status_spi = "healthy" if totals["SPI"] >= 1 else ("critical" if totals["SPI"] < 0.85 else "warning")
    render_kpi_card(
        "Índ. Rendimiento Cronograma", "SPI — Schedule Performance Index",
        f"{totals['SPI']:.3f}", "⏱️", status_spi,
        "✅ Adelantado" if totals["SPI"] >= 1 else f"🔴 Retrasado {(1-totals['SPI'])*100:.1f}%",
    )
with kpi_col[5]:
    eac_status = "critical" if totals["EAC"] > totals["total_PV"] * 1.05 else "healthy"
    delta_eac  = totals["EAC"] - totals["total_PV"]
    render_kpi_card(
        "Costo Estimado al Cierre", "EAC — Estimate at Completion",
        f"${totals['EAC']:,.0f}", "🔮", eac_status,
        f"Δ ${delta_eac:+,.0f} vs BAC",
    )

st.markdown("<br>", unsafe_allow_html=True)

# Secondary KPIs row
kpi_col2 = st.columns(5)
with kpi_col2[0]:
    render_kpi_card(
        "Variación de Costo", "CV = EV − AC",
        f"${totals['CV']:+,.0f}", "📉",
        "healthy" if totals["CV"] >= 0 else "critical",
    )
with kpi_col2[1]:
    render_kpi_card(
        "Variación de Cronograma", "SV = EV − PV",
        f"${totals['SV']:+,.0f}", "📅",
        "healthy" if totals["SV"] >= 0 else "critical",
    )
with kpi_col2[2]:
    render_kpi_card(
        "Avance Físico Global", "Ponderado por PV",
        f"{totals['avance_ponderado']:.1f}%", "📐", "neutral",
    )
with kpi_col2[3]:
    render_kpi_card(
        "TCPI — Rend. Requerido", "Para cerrar en presupuesto",
        f"{totals['TCPI']:.3f}", "🎲",
        "healthy" if totals["TCPI"] <= 1.05 else "critical",
        "⚡ Alta exigencia" if totals["TCPI"] > 1.1 else None,
    )
with kpi_col2[4]:
    render_kpi_card(
        "Tareas en Zona Crítica", "CPI < 1.0",
        str(totals["n_critical"]), "🚨",
        "critical" if totals["n_critical"] > 0 else "healthy",
        f"{totals['n_critical']}/{totals['n_tasks']} tareas",
    )

# ── Automatic alerts ──────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
has_alert = False
if totals["CPI"] < 0.85:
    render_alert(
        f"ALERTA CRÍTICA DE COSTO: CPI = {totals['CPI']:.3f} — El proyecto ejecuta un "
        f"{(1-totals['CPI'])*100:.1f}% sobre el presupuesto. Requiere intervención inmediata en el control de costos.",
        "critical",
    )
    has_alert = True

if totals["SPI"] < 0.85:
    render_alert(
        f"ALERTA CRÍTICA DE CRONOGRAMA: SPI = {totals['SPI']:.3f} — El proyecto acumula un "
        f"{(1-totals['SPI'])*100:.1f}% de retraso respecto al plan. Revisar ruta crítica.",
        "critical",
    )
    has_alert = True

if totals["EAC"] > totals["total_PV"] * 1.1:
    overrun = totals["EAC"] - totals["total_PV"]
    render_alert(
        f"PROYECCIÓN FUERA DE CONTROL: El EAC (${totals['EAC']:,.0f}) supera el presupuesto "
        f"original en ${overrun:,.0f}. Se recomienda revisión del alcance y contingencias.",
        "critical",
    )
    has_alert = True

if not has_alert and totals["CPI"] >= 1 and totals["SPI"] >= 1:
    render_alert("Proyecto dentro de parámetros aceptables: CPI ≥ 1.0 y SPI ≥ 1.0. Continuar monitoreo.", "success")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — DASHBOARD VISUAL
# ══════════════════════════════════════════════════════════════════════════════
render_section_header("📈 Dashboard Visual e Interactivo", "Análisis gráfico del Triángulo de Hierro: Alcance · Tiempo · Costo")

# ── Gauge row ─────────────────────────────────────────────────────────────────
st.plotly_chart(
    plot_project_gauge(totals["avance_ponderado"], totals["CPI"], totals["SPI"]),
    use_container_width=True,
    config={"displayModeBar": False},
)

# ── S-Curve ───────────────────────────────────────────────────────────────────
s_data = prepare_s_curve_data(df_evm)
st.plotly_chart(
    plot_s_curve(s_data),
    use_container_width=True,
    config={"displayModeBar": True, "modeBarButtonsToRemove": ["select2d", "lasso2d"]},
)

# ── Quadrant scatter + Pareto (side by side) ──────────────────────────────────
col_scatter, col_pareto = st.columns([1, 1])

with col_scatter:
    st.plotly_chart(
        plot_scatter_quadrant(df_evm),
        use_container_width=True,
        config={"displayModeBar": True},
    )

with col_pareto:
    pareto_df = get_pareto_data(df_evm)
    st.plotly_chart(
        plot_pareto_subcontractors(pareto_df),
        use_container_width=True,
        config={"displayModeBar": True},
    )

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# PHASE 4 — PROJECTIONS & DATA TABLE
# ══════════════════════════════════════════════════════════════════════════════
render_section_header("🔮 Proyección Ejecutiva y Análisis de Datos")

col_proj, col_notes = st.columns([1, 1])

with col_proj:
    st.markdown("""
    <div style="background:linear-gradient(145deg,#0F2144,#0A1628);
                border:1px solid #1B3566;border-radius:12px;border-top:2px solid #E8921C;padding:20px;">
        <h4 style="color:#E8921C;margin:0 0 16px 0;font-weight:700;">📐 Módulo de Estimación (EAC)</h4>
    """, unsafe_allow_html=True)

    proj_data = {
        "Métrica": [
            "BAC — Presupuesto Original",
            "EV — Valor Ganado Acumulado",
            "AC — Costo Real Acumulado",
            "CPI Actual del Proyecto",
            "EAC — Costo Estimado al Cierre",
            "ETC — Costo Pendiente Estimado",
            "VAC — Variación al Cierre",
            "TCPI — Rendimiento Requerido",
        ],
        "Valor": [
            f"${totals['total_PV']:,.2f}",
            f"${totals['total_EV']:,.2f}",
            f"${totals['total_AC']:,.2f}",
            f"{totals['CPI']:.4f}",
            f"${totals['EAC']:,.2f}",
            f"${totals['EAC'] - totals['total_AC']:,.2f}",
            f"${totals['VAC']:+,.2f}",
            f"{totals['TCPI']:.4f}",
        ],
        "Estado": [
            "📋 Base",
            "🎯 Ejecutado",
            "💰 Real",
            "🟢 OK" if totals["CPI"] >= 1 else "🔴 Crítico",
            "🟡 Proyección",
            "📌 Pendiente",
            "🟢 Favorable" if totals["VAC"] >= 0 else "🔴 Desfavorable",
            "🟢 Viable" if totals["TCPI"] <= 1.05 else "🔴 Alta exigencia",
        ],
    }
    st.dataframe(
        pd.DataFrame(proj_data),
        hide_index=True,
        use_container_width=True,
        height=310,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with col_notes:
    st.markdown("""
    <div style="background:linear-gradient(145deg,#0F2144,#0A1628);
                border:1px solid #1B3566;border-radius:12px;border-top:2px solid #E8921C;padding:20px;">
        <h4 style="color:#E8921C;margin:0 0 12px 0;font-weight:700;">📝 Minuta del Estado de Obra</h4>
    """, unsafe_allow_html=True)

    project_notes = st.text_area(
        "Comentarios del Director de Obra / Project Manager",
        placeholder=(
            "Ej: Semana 24 — Estructura metálica con retraso de 2 semanas por "
            "demoras en provisión de acero. Se gestionó proveedor alternativo. "
            "Instalaciones eléctricas HV presentan sobrecosto del 18%, se solicitó "
            "revisión de alcance al subcontratista..."
        ),
        height=220,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── EVM Data Table ────────────────────────────────────────────────────────────
render_section_header("📋 Tabla de Datos EVM por Tarea")

display_cols = ["task_id", "Subcontratista", "Fecha_Reporte",
                "PV", "AC", "Avance_Fisico", "EV", "CV", "SV", "CPI", "SPI", "status"]
available    = [c for c in display_cols if c in df_evm.columns]

df_display = df_evm[available].copy()
df_display["Fecha_Reporte"] = df_display["Fecha_Reporte"].dt.strftime("%d/%m/%Y")
df_display.rename(columns={
    "task_id": "Tarea / EDT",
    "Subcontratista": "Subcontratista",
    "Avance_Fisico": "Avance %",
    "status": "Estado",
}, inplace=True)

st.dataframe(
    df_display.style.format({
        "PV": "${:,.0f}", "AC": "${:,.0f}", "EV": "${:,.0f}",
        "CV": "${:+,.0f}", "SV": "${:+,.0f}",
        "CPI": "{:.3f}", "SPI": "{:.3f}", "Avance %": "{:.1f}",
    }).map(
        lambda v: "color: #E74C3C; font-weight: bold" if isinstance(v, float) and v < 1 else "",
        subset=["CPI", "SPI"],
    ).map(
        lambda v: "color: #E74C3C; font-weight: bold" if isinstance(v, (int, float)) and v < 0 else
                  "color: #27AE60; font-weight: bold" if isinstance(v, (int, float)) and v >= 0 else "",
        subset=["CV", "SV"],
    ),
    use_container_width=True,
    height=380,
)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# EXPORT SECTION
# ══════════════════════════════════════════════════════════════════════════════
render_section_header("📤 Exportación de Reportes Ejecutivos")

col_dl1, col_dl2, col_spacer = st.columns([1.5, 1.5, 3])

project_name = uploaded_file.name.replace(".csv", "").replace(".xlsx", "").replace(".xls", "")
ts           = datetime.now().strftime("%Y%m%d_%H%M")

with col_dl1:
    with st.spinner("Preparando Excel..."):
        excel_bytes = export_to_excel(df_evm, totals, project_notes)
    st.download_button(
        label="📊 Descargar Reporte Excel",
        data=excel_bytes,
        file_name=f"GrowthData_EVM_{project_name}_{ts}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
    st.caption("Incluye: KPIs ejecutivos · Tabla EVM · Datos origen")

with col_dl2:
    with st.spinner("Preparando PDF..."):
        logo_path_arg = LOGO_PATH if os.path.exists(LOGO_PATH) else None
        pdf_bytes     = export_to_pdf(totals, df_evm, project_notes, logo_path=logo_path_arg)
    st.download_button(
        label="📄 Descargar Reporte PDF",
        data=pdf_bytes,
        file_name=f"GrowthData_EVM_{project_name}_{ts}.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
    st.caption("Incluye: KPIs · Alertas · Top 10 críticas · Minuta")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;padding:16px;border-top:2px solid #1B3566;margin-top:20px;">
    <p style="color:#E8921C;font-size:0.73rem;margin:0;font-weight:500;letter-spacing:0.5px;">
        GrowthData Analytics LLC &nbsp;·&nbsp; Project Controls Platform v2.0 &nbsp;·&nbsp; PMBOK® 7ª Edición &nbsp;·&nbsp;
        Earned Value Management (EVM) &nbsp;·&nbsp; © 2024 Todos los derechos reservados
    </p>
</div>
""", unsafe_allow_html=True)
