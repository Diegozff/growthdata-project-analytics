"""
GrowthData Analytics LLC — Project Controls Platform v2.0
ClickUp-inspired navigation layout
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(
    page_title="GrowthData Analytics | Project Controls",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from modules.ui_components import (
    apply_custom_css, render_kpi_card, render_section_header,
    render_alert, render_page_header, BRAND,
)
from modules.data_ingestion   import upload_and_validate, normalize_columns
from modules.evm_calculator   import (
    calculate_evm_metrics, calculate_project_totals,
    prepare_s_curve_data, get_pareto_data,
)
from modules.visualizations   import (
    plot_s_curve, plot_scatter_quadrant,
    plot_pareto_subcontractors, plot_project_gauge,
)
from modules.export           import export_to_excel, export_to_pdf
from sample_data.generate_sample import generate_sample_csv, generate_sample_excel

apply_custom_css()

LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo GrowthData Project Analytics.png")

# ── Session state ─────────────────────────────────────────────────────────────
if "page"          not in st.session_state: st.session_state.page = "📊  Dashboard"
if "notes"         not in st.session_state: st.session_state.notes = ""
if "df_evm"        not in st.session_state: st.session_state.df_evm = None
if "totals"        not in st.session_state: st.session_state.totals = None
if "uploaded_name" not in st.session_state: st.session_state.uploaded_name = None

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR — ClickUp style
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── Workspace header ──────────────────────────────────────────────────
    logo_col, name_col = st.columns([1, 2.5])
    with logo_col:
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=52)
        else:
            st.markdown('<div style="font-size:2rem;padding:6px 0;">🏗️</div>', unsafe_allow_html=True)
    with name_col:
        st.markdown(f"""
        <div style="padding:8px 0 0 0;">
            <p style="color:{BRAND['text']};font-size:0.88rem;font-weight:700;margin:0;
                      letter-spacing:-0.2px;">GrowthData Analytics</p>
            <p style="color:{BRAND['text_muted']};font-size:0.68rem;margin:2px 0 0 0;">
                Project Controls
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f'<hr class="sidebar-divider">', unsafe_allow_html=True)

    # ── File upload ───────────────────────────────────────────────────────
    st.markdown('<p class="nav-section-label">PROYECTO</p>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Cargar archivo",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed",
        help="CSV o Excel con datos de la obra",
    )

    # Upload status pill
    if uploaded_file:
        st.markdown(f"""
        <div class="upload-status loaded">
            ✅ &nbsp;<strong>{uploaded_file.name}</strong>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="upload-status empty">
            📁 &nbsp; Sin archivo cargado
        </div>""", unsafe_allow_html=True)

    # Sample downloads
    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button("📄 CSV",   generate_sample_csv(),   "muestra.csv",
                           "text/csv", use_container_width=True)
    with dl_col2:
        st.download_button("📊 Excel", generate_sample_excel(), "muestra.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    st.markdown(f'<hr class="sidebar-divider">', unsafe_allow_html=True)

    # ── Navigation ────────────────────────────────────────────────────────
    st.markdown('<p class="nav-section-label">WORKSPACE</p>', unsafe_allow_html=True)

    NAV_PAGES = [
        "📊  Dashboard",
        "📈  Curva S",
        "🎯  Análisis EVM",
        "👷  Subcontratistas",
        "🔮  Proyecciones",
        "📤  Exportar",
    ]

    selected = st.radio("nav", NAV_PAGES, label_visibility="collapsed",
                        index=NAV_PAGES.index(st.session_state.page)
                        if st.session_state.page in NAV_PAGES else 0)
    st.session_state.page = selected

    # ── Filters (shown only when data loaded) ─────────────────────────────
    if st.session_state.df_evm is not None:
        st.markdown(f'<hr class="sidebar-divider">', unsafe_allow_html=True)
        st.markdown('<p class="nav-section-label">FILTROS</p>', unsafe_allow_html=True)

        df_base = st.session_state.df_evm
        dates = sorted(df_base["Fecha_Reporte"].dt.date.unique())

        if len(dates) > 1:
            date_sel = st.select_slider(
                "Período", options=dates,
                value=(dates[0], dates[-1]),
                format_func=lambda d: d.strftime("%d/%m/%y"),
            )
            df_filtered = df_base[
                (df_base["Fecha_Reporte"].dt.date >= date_sel[0]) &
                (df_base["Fecha_Reporte"].dt.date <= date_sel[1])
            ].copy()
        else:
            df_filtered = df_base.copy()

        subs = ["Todos"] + sorted(df_base["Subcontratista"].unique().tolist())
        sel_sub = st.selectbox("Subcontratista", subs, label_visibility="visible")
        if sel_sub != "Todos":
            df_filtered = df_filtered[df_filtered["Subcontratista"] == sel_sub]

        only_crit = st.checkbox("Solo críticas (CPI < 1)")
        if only_crit:
            df_filtered = df_filtered[df_filtered["CPI"] < 1]

        st.markdown(f'<span style="color:{BRAND["text_muted"]};font-size:0.75rem;">'
                    f'**{len(df_filtered)}** tareas en vista</span>', unsafe_allow_html=True)

        st.session_state.df_filtered = df_filtered
        st.session_state.totals_filtered = calculate_project_totals(df_filtered)
    else:
        st.session_state.df_filtered = None
        st.session_state.totals_filtered = None

    # ── Sidebar footer ────────────────────────────────────────────────────
    st.markdown(f'<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="padding:0 16px 8px 16px;">
        <p style="color:{BRAND['text_dim']};font-size:0.65rem;margin:0;line-height:1.8;">
            v2.0 · PMBOK® 7th Ed.<br>
            © 2024 GrowthData Analytics LLC
        </p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DATA PROCESSING (runs whenever a file is uploaded)
# ══════════════════════════════════════════════════════════════════════════════
if uploaded_file and uploaded_file.name != st.session_state.uploaded_name:
    with st.spinner("Procesando datos..."):
        df_raw, err = upload_and_validate(uploaded_file)

    if err:
        st.markdown(f"""
        <div style="padding:28px;margin:20px;">
            <div class="alert-critical">
                <strong>❌ Error de Validación</strong><br>{err}
            </div>
        </div>""", unsafe_allow_html=True)
        st.stop()

    df = normalize_columns(df_raw.copy())
    df = calculate_evm_metrics(df)
    st.session_state.df_evm        = df
    st.session_state.totals        = calculate_project_totals(df)
    st.session_state.df_filtered   = df.copy()
    st.session_state.totals_filtered = st.session_state.totals
    st.session_state.uploaded_name = uploaded_file.name
    st.rerun()


# ── Shortcuts ─────────────────────────────────────────────────────────────────
page     = st.session_state.page
df_evm   = st.session_state.df_evm
totals   = st.session_state.totals_filtered or st.session_state.totals
df_view  = st.session_state.df_filtered if st.session_state.df_filtered is not None else df_evm
has_data = df_evm is not None


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if "Dashboard" in page:
    cpi_badge = ("🟢 CPI OK", "healthy") if (totals and totals["CPI"] >= 1) else ("🔴 Sobrecosto", "critical")
    render_page_header(
        "Dashboard",
        subtitle=f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        icon="📊",
        badge=cpi_badge[0] if has_data else "",
        badge_level=cpi_badge[1] if has_data else "",
    )

    if not has_data:
        # ── Empty state ───────────────────────────────────────────────────
        st.markdown('<div style="padding:20px 28px;">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center;padding:60px 20px;">
            <div style="font-size:4rem;margin-bottom:16px;">📁</div>
            <h2 style="color:{BRAND['text']};font-size:1.3rem;margin:0 0 10px 0;">
                Carga tu archivo de datos para comenzar
            </h2>
            <p style="color:{BRAND['text_muted']};max-width:480px;margin:0 auto;
                      font-size:0.875rem;line-height:1.7;">
                Sube un CSV o Excel con el estado de tu obra desde el panel izquierdo.
                El sistema generará automáticamente todos los indicadores EVM.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Feature grid
        features = [
            ("💹", "CPI & SPI", "Índices de rendimiento de costo y cronograma en tiempo real"),
            ("📈", "Curva S", "Evolución acumulada de PV, AC y EV con zona de desvío"),
            ("🎯", "Cuadrantes", "Mapa visual de tareas por rendimiento SPI vs CPI"),
            ("👷", "Pareto", "Subcontratistas ordenados por impacto en el margen"),
            ("🔮", "EAC", "Proyección del costo final basada en rendimiento actual"),
            ("📄", "Reportes", "Exportación a Excel estilizado y PDF ejecutivo"),
        ]
        cols = st.columns(3)
        for i, (icon, title, desc) in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="content-card" style="text-align:center;padding:20px 16px;min-height:130px;">
                    <div style="font-size:1.8rem;margin-bottom:8px;">{icon}</div>
                    <p style="color:{BRAND['orange']};font-size:0.82rem;font-weight:600;
                              margin:0 0 4px 0;">{title}</p>
                    <p style="color:{BRAND['text_muted']};font-size:0.75rem;margin:0;
                              line-height:1.5;">{desc}</p>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    st.markdown('<div style="padding:20px 28px 0 28px;">', unsafe_allow_html=True)

    # ── Gauges ────────────────────────────────────────────────────────────
    st.plotly_chart(
        plot_project_gauge(totals["avance_ponderado"], totals["CPI"], totals["SPI"]),
        use_container_width=True, config={"displayModeBar": False},
    )

    # ── KPI row 1 ─────────────────────────────────────────────────────────
    render_section_header("INDICADORES EVM PRINCIPALES")
    c = st.columns(6)
    kpis = [
        ("PV — Planificado",   "Presupuesto base",      f"${totals['total_PV']:,.0f}", "📋", "neutral",  None),
        ("AC — Costo Real",    "Ejecutado hasta hoy",   f"${totals['total_AC']:,.0f}", "💰", "neutral",  None),
        ("EV — Valor Ganado",  "Trabajo completado",    f"${totals['total_EV']:,.0f}", "🎯", "neutral",  None),
        ("CPI",                "Rendimiento de costo",  f"{totals['CPI']:.3f}",        "💹",
         "healthy" if totals["CPI"]>=1 else ("critical" if totals["CPI"]<0.85 else "warning"),
         "✅ Bajo presupuesto" if totals["CPI"]>=1 else f"🔴 +{(1-totals['CPI'])*100:.1f}% sobre costo"),
        ("SPI",                "Rendimiento cronograma",f"{totals['SPI']:.3f}",        "⏱️",
         "healthy" if totals["SPI"]>=1 else ("critical" if totals["SPI"]<0.85 else "warning"),
         "✅ Adelantado" if totals["SPI"]>=1 else f"🔴 {(1-totals['SPI'])*100:.1f}% de retraso"),
        ("EAC — Proyección",   "Costo estimado al cierre",f"${totals['EAC']:,.0f}",  "🔮",
         "critical" if totals["EAC"]>totals["total_PV"]*1.05 else "healthy",
         f"Δ ${totals['EAC']-totals['total_PV']:+,.0f} vs BAC"),
    ]
    for col, (lbl, sub, val, icon, status, delta) in zip(c, kpis):
        with col:
            render_kpi_card(lbl, sub, val, icon, status, delta)

    # ── KPI row 2 ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    c2 = st.columns(5)
    kpis2 = [
        ("CV — Var. Costo",     f"${totals['CV']:+,.0f}", "📉",
         "healthy" if totals["CV"]>=0 else "critical", None),
        ("SV — Var. Cronograma",f"${totals['SV']:+,.0f}", "📅",
         "healthy" if totals["SV"]>=0 else "critical", None),
        ("Avance Global",       f"{totals['avance_ponderado']:.1f}%","📐","neutral", "Ponderado por PV"),
        ("TCPI",                f"{totals['TCPI']:.3f}",   "🎲",
         "healthy" if totals["TCPI"]<=1.05 else "critical",
         "Rend. requerido al cierre"),
        ("Tareas Críticas",     str(totals["n_critical"]), "🚨",
         "critical" if totals["n_critical"]>0 else "healthy",
         f"{totals['n_critical']} de {totals['n_tasks']} tareas"),
    ]
    for col, (lbl, val, icon, status, delta) in zip(c2, kpis2):
        with col:
            render_kpi_card(lbl, lbl, val, icon, status, delta)

    # ── Alerts ────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    alerted = False
    if totals["CPI"] < 0.85:
        render_alert(f"COSTO CRÍTICO: CPI={totals['CPI']:.3f} — Proyecto {(1-totals['CPI'])*100:.1f}% sobre presupuesto. Requiere acción inmediata.", "critical")
        alerted = True
    if totals["SPI"] < 0.85:
        render_alert(f"CRONOGRAMA CRÍTICO: SPI={totals['SPI']:.3f} — Retraso acumulado del {(1-totals['SPI'])*100:.1f}%. Revisar ruta crítica.", "critical")
        alerted = True
    if totals["EAC"] > totals["total_PV"] * 1.1:
        render_alert(f"EAC FUERA DE CONTROL: Proyección supera el BAC en ${totals['EAC']-totals['total_PV']:,.0f}. Revisar contingencias.", "warning")
        alerted = True
    if not alerted and totals["CPI"] >= 1 and totals["SPI"] >= 1:
        render_alert("Proyecto dentro de parámetros aceptables — CPI ≥ 1.0 y SPI ≥ 1.0.", "success")

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: CURVA S
# ══════════════════════════════════════════════════════════════════════════════
elif "Curva S" in page:
    render_page_header("Curva S", "Evolución acumulada PV / AC / EV a lo largo del tiempo", "📈")
    st.markdown('<div style="padding:20px 28px;">', unsafe_allow_html=True)

    if not has_data:
        st.info("Carga un archivo de datos para ver la Curva S.", icon="📁")
        st.stop()

    s_data = prepare_s_curve_data(df_view)
    st.plotly_chart(plot_s_curve(s_data), use_container_width=True,
                    config={"displayModeBar": True})

    # Summary table
    render_section_header("RESUMEN POR PERÍODO")
    tbl = s_data.copy()
    tbl["Fecha_Reporte"] = tbl["Fecha_Reporte"].dt.strftime("%d/%m/%Y")
    tbl = tbl.rename(columns={
        "PV":"PV ($)","AC":"AC ($)","EV":"EV ($)",
        "PV_cum":"PV Acum ($)","AC_cum":"AC Acum ($)","EV_cum":"EV Acum ($)",
    })
    st.dataframe(
        tbl.style.format({c: "${:,.0f}" for c in tbl.columns if "$" in c}),
        use_container_width=True, hide_index=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: ANÁLISIS EVM
# ══════════════════════════════════════════════════════════════════════════════
elif "Análisis EVM" in page:
    render_page_header("Análisis EVM", "Mapa de rendimiento SPI vs CPI por tarea", "🎯")
    st.markdown('<div style="padding:20px 28px;">', unsafe_allow_html=True)

    if not has_data:
        st.info("Carga un archivo de datos para ver el análisis.", icon="📁")
        st.stop()

    st.plotly_chart(plot_scatter_quadrant(df_view), use_container_width=True,
                    config={"displayModeBar": True})

    render_section_header("TABLA DE DATOS EVM")
    cols_show = ["task_id","Subcontratista","Fecha_Reporte","PV","AC",
                 "Avance_Fisico","EV","CV","SV","CPI","SPI","status"]
    avail = [c for c in cols_show if c in df_view.columns]
    df_disp = df_view[avail].copy()
    df_disp["Fecha_Reporte"] = df_disp["Fecha_Reporte"].dt.strftime("%d/%m/%Y")
    df_disp.rename(columns={"task_id":"Tarea","Avance_Fisico":"Avance %","status":"Estado"}, inplace=True)

    st.dataframe(
        df_disp.style.format({
            "PV":"${:,.0f}","AC":"${:,.0f}","EV":"${:,.0f}",
            "CV":"${:+,.0f}","SV":"${:+,.0f}",
            "CPI":"{:.3f}","SPI":"{:.3f}","Avance %":"{:.1f}",
        }).map(
            lambda v: "color:#E74C3C;font-weight:bold" if isinstance(v,float) and v<1 else "",
            subset=["CPI","SPI"],
        ).map(
            lambda v: ("color:#E74C3C;font-weight:bold" if isinstance(v,(int,float)) and v<0 else
                       "color:#27AE60;font-weight:bold" if isinstance(v,(int,float)) and v>=0 else ""),
            subset=["CV","SV"],
        ),
        use_container_width=True, height=400,
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: SUBCONTRATISTAS
# ══════════════════════════════════════════════════════════════════════════════
elif "Subcontratistas" in page:
    render_page_header("Subcontratistas", "Pareto de desvíos — quién está licuando el margen", "👷")
    st.markdown('<div style="padding:20px 28px;">', unsafe_allow_html=True)

    if not has_data:
        st.info("Carga un archivo de datos para ver el análisis.", icon="📁")
        st.stop()

    pareto_df = get_pareto_data(df_view)
    st.plotly_chart(plot_pareto_subcontractors(pareto_df), use_container_width=True,
                    config={"displayModeBar": True})

    render_section_header("RANKING DE SUBCONTRATISTAS")
    rank_df = pareto_df[["Subcontratista","PV","AC","EV","CV","CPI","n_tasks"]].copy()
    rank_df.rename(columns={"n_tasks":"Tareas"}, inplace=True)
    st.dataframe(
        rank_df.style.format({
            "PV":"${:,.0f}","AC":"${:,.0f}","EV":"${:,.0f}",
            "CV":"${:+,.0f}","CPI":"{:.3f}",
        }).map(
            lambda v: "color:#E74C3C;font-weight:bold" if isinstance(v,float) and v<1 else
                      "color:#27AE60;font-weight:bold" if isinstance(v,float) and v>=1 else "",
            subset=["CPI"],
        ).map(
            lambda v: "color:#E74C3C;font-weight:bold" if isinstance(v,(int,float)) and v<0 else "",
            subset=["CV"],
        ),
        use_container_width=True, hide_index=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: PROYECCIONES
# ══════════════════════════════════════════════════════════════════════════════
elif "Proyecciones" in page:
    render_page_header("Proyecciones", "Estimación EAC y módulo de notas del Director de Obra", "🔮")
    st.markdown('<div style="padding:20px 28px;">', unsafe_allow_html=True)

    if not has_data:
        st.info("Carga un archivo de datos para ver las proyecciones.", icon="📁")
        st.stop()

    col_l, col_r = st.columns([1, 1], gap="large")

    with col_l:
        st.markdown(f'<div class="content-card-title">📐 Módulo EAC — Estimación al Cierre</div>',
                    unsafe_allow_html=True)
        proj = {
            "Métrica": ["BAC — Presupuesto Original","EV — Valor Ganado",
                        "AC — Costo Real","CPI Actual",
                        "EAC — Costo Estimado al Cierre","ETC — Costo Pendiente",
                        "VAC — Variación al Cierre","TCPI — Rend. Requerido"],
            "Valor":   [f"${totals['total_PV']:,.2f}", f"${totals['total_EV']:,.2f}",
                        f"${totals['total_AC']:,.2f}", f"{totals['CPI']:.4f}",
                        f"${totals['EAC']:,.2f}",
                        f"${totals['EAC']-totals['total_AC']:,.2f}",
                        f"${totals['VAC']:+,.2f}", f"{totals['TCPI']:.4f}"],
            "Estado":  ["📋 Base","🎯 Ganado","💰 Real",
                        "🟢 OK" if totals["CPI"]>=1 else "🔴 Crítico",
                        "🟡 Proyectado",
                        "📌 Pendiente",
                        "🟢 Favorable" if totals["VAC"]>=0 else "🔴 Desfavorable",
                        "🟢 Viable" if totals["TCPI"]<=1.05 else "🔴 Alta exigencia"],
        }
        st.dataframe(pd.DataFrame(proj), hide_index=True,
                     use_container_width=True, height=320)

    with col_r:
        st.markdown(f'<div class="content-card-title">📝 Minuta del Estado de Obra</div>',
                    unsafe_allow_html=True)
        st.session_state.notes = st.text_area(
            "Comentarios",
            value=st.session_state.notes,
            placeholder="Ingrese observaciones, acuerdos y acciones del período...",
            height=270,
            label_visibility="collapsed",
        )

    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  PAGE: EXPORTAR
# ══════════════════════════════════════════════════════════════════════════════
elif "Exportar" in page:
    render_page_header("Exportar", "Descarga el reporte ejecutivo en Excel o PDF", "📤")
    st.markdown('<div style="padding:20px 28px;">', unsafe_allow_html=True)

    if not has_data:
        st.info("Carga un archivo de datos para generar reportes.", icon="📁")
        st.stop()

    ts   = datetime.now().strftime("%Y%m%d_%H%M")
    name = (st.session_state.uploaded_name or "proyecto").replace(".csv","").replace(".xlsx","")

    col_xl, col_pdf, col_info = st.columns([1, 1, 2], gap="large")

    with col_xl:
        st.markdown(f"""
        <div class="content-card" style="text-align:center;padding:28px 20px;">
            <div style="font-size:2.5rem;margin-bottom:12px;">📊</div>
            <p style="color:{BRAND['text']};font-weight:600;font-size:0.9rem;margin:0 0 6px 0;">
                Reporte Excel
            </p>
            <p style="color:{BRAND['text_muted']};font-size:0.75rem;margin:0 0 16px 0;
                      line-height:1.6;">
                3 hojas: Resumen KPIs<br>Tabla EVM · Datos origen
            </p>
        </div>""", unsafe_allow_html=True)
        with st.spinner("Generando..."):
            xl = export_to_excel(df_view, totals, st.session_state.notes)
        st.download_button("📥 Descargar Excel", xl,
                           f"GrowthData_EVM_{name}_{ts}.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                           use_container_width=True)

    with col_pdf:
        st.markdown(f"""
        <div class="content-card" style="text-align:center;padding:28px 20px;">
            <div style="font-size:2.5rem;margin-bottom:12px;">📄</div>
            <p style="color:{BRAND['text']};font-weight:600;font-size:0.9rem;margin:0 0 6px 0;">
                Reporte PDF
            </p>
            <p style="color:{BRAND['text_muted']};font-size:0.75rem;margin:0 0 16px 0;
                      line-height:1.6;">
                KPIs · Alertas · Top 10 críticas<br>Minuta · Firma gerencial
            </p>
        </div>""", unsafe_allow_html=True)
        with st.spinner("Generando..."):
            logo_arg = LOGO_PATH if os.path.exists(LOGO_PATH) else None
            pdf = export_to_pdf(totals, df_view, st.session_state.notes, logo_path=logo_arg)
        st.download_button("📥 Descargar PDF", pdf,
                           f"GrowthData_EVM_{name}_{ts}.pdf",
                           "application/pdf",
                           use_container_width=True)

    with col_info:
        st.markdown(f"""
        <div class="content-card">
            <div class="content-card-title">ℹ️ Contenido del reporte</div>
            <p style="color:{BRAND['text_muted']};font-size:0.8rem;line-height:1.8;margin:0;">
                ✅ &nbsp;KPIs ejecutivos: CPI, SPI, EAC, VAC, TCPI<br>
                ✅ &nbsp;Alertas semafóricas automáticas<br>
                ✅ &nbsp;Top 10 tareas con CPI más bajo<br>
                ✅ &nbsp;Minuta del Director de Obra<br>
                ✅ &nbsp;Bloque de firma gerencial<br>
                ✅ &nbsp;Datos filtrados según vista activa<br>
                ✅ &nbsp;Formato: <strong style="color:{BRAND['text']};">
                {datetime.now().strftime('%d/%m/%Y %H:%M')}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
