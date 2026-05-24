"""
UI Components — ClickUp-inspired sidebar + brand CSS.
Brand: Navy #1B3566 | Blue #3D7EC5 | Orange #E8921C
"""

import streamlit as st

BRAND = {
    "orange":     "#E8921C",
    "navy":       "#1B3566",
    "blue":       "#3D7EC5",
    "bg":         "#08111E",
    "sidebar":    "#0B0F1E",
    "card":       "#0E1A30",
    "card2":      "#111C35",
    "border":     "#1A2A4A",
    "text":       "#E8EDF5",
    "text_muted": "#7A90B0",
    "text_dim":   "#3D5070",
    "critical":   "#E74C3C",
    "warning":    "#E8921C",
    "healthy":    "#27AE60",
}


def apply_custom_css() -> None:
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── Reset ──────────────────────────────────────────────────────────── */
    html, body, [class*="css"] {{
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    }}
    .stApp {{ background-color: {BRAND['bg']}; }}
    .main .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}

    /* ── Sidebar — ClickUp style ─────────────────────────────────────────── */
    [data-testid="stSidebar"] {{
        background-color: {BRAND['sidebar']} !important;
        border-right: 1px solid {BRAND['border']};
        padding: 0 !important;
    }}
    [data-testid="stSidebar"] > div:first-child {{
        padding: 0 !important;
    }}
    [data-testid="stSidebar"] .block-container {{
        padding: 0 0 20px 0 !important;
    }}

    /* ── Nav radio → ClickUp nav items ──────────────────────────────────── */
    [data-testid="stSidebar"] .stRadio > label {{
        display: none !important;
    }}
    [data-testid="stSidebar"] .stRadio > div {{
        gap: 2px !important;
        display: flex !important;
        flex-direction: column !important;
    }}
    [data-testid="stSidebar"] .stRadio label {{
        display: flex !important;
        align-items: center !important;
        padding: 8px 16px 8px 20px !important;
        border-radius: 0 8px 8px 0 !important;
        margin: 1px 8px 1px 0 !important;
        cursor: pointer !important;
        color: {BRAND['text_muted']} !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        border-left: 3px solid transparent !important;
        transition: all 0.15s ease !important;
        background: transparent !important;
        min-height: 36px !important;
        user-select: none !important;
    }}
    [data-testid="stSidebar"] .stRadio label:hover {{
        background: rgba(255,255,255,0.04) !important;
        color: {BRAND['text']} !important;
        border-left-color: rgba(232,146,28,0.3) !important;
    }}
    /* Active nav item via :has() — modern browsers */
    [data-testid="stSidebar"] .stRadio label:has(input:checked) {{
        background: rgba(232,146,28,0.10) !important;
        border-left-color: {BRAND['orange']} !important;
        color: {BRAND['orange']} !important;
        font-weight: 600 !important;
    }}
    /* Hide radio circles */
    [data-testid="stSidebar"] .stRadio [role="radio"],
    [data-testid="stSidebar"] .stRadio input[type="radio"] {{
        display: none !important;
    }}
    [data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {{
        margin: 0 !important;
        font-size: 0.875rem !important;
    }}

    /* ── Nav section labels ──────────────────────────────────────────────── */
    .nav-section-label {{
        font-size: 0.65rem !important;
        font-weight: 700 !important;
        color: {BRAND['text_dim']} !important;
        text-transform: uppercase !important;
        letter-spacing: 1.5px !important;
        padding: 16px 20px 6px 20px !important;
        margin: 0 !important;
    }}

    /* ── Sidebar divider ─────────────────────────────────────────────────── */
    .sidebar-divider {{
        border: none;
        border-top: 1px solid {BRAND['border']};
        margin: 10px 0;
    }}

    /* ── Workspace header (top of sidebar) ───────────────────────────────── */
    .workspace-header {{
        background: linear-gradient(135deg, {BRAND['navy']}, #0D1830);
        padding: 16px 16px 14px 16px;
        border-bottom: 1px solid {BRAND['border']};
    }}
    .workspace-name {{
        color: {BRAND['text']};
        font-size: 0.95rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.3px;
    }}
    .workspace-sub {{
        color: {BRAND['text_muted']};
        font-size: 0.7rem;
        margin: 2px 0 0 0;
        font-weight: 400;
    }}

    /* ── Upload area (sidebar) ───────────────────────────────────────────── */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {{
        border: 1.5px dashed {BRAND['navy']};
        border-radius: 8px;
        background: rgba(27,53,102,0.12);
        padding: 4px;
    }}
    [data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {{
        border-color: {BRAND['orange']};
        background: rgba(232,146,28,0.05);
    }}

    /* ── Page content wrapper ────────────────────────────────────────────── */
    .page-wrapper {{
        padding: 24px 28px 40px 28px;
    }}

    /* ── Page header (ClickUp-style breadcrumb header) ───────────────────── */
    .page-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 28px 16px 28px;
        border-bottom: 1px solid {BRAND['border']};
        background: {BRAND['bg']};
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    .page-breadcrumb {{
        font-size: 0.72rem;
        color: {BRAND['text_dim']};
        margin: 0 0 4px 0;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }}
    .page-title {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {BRAND['text']};
        margin: 0;
        letter-spacing: -0.4px;
    }}
    .page-subtitle {{
        font-size: 0.78rem;
        color: {BRAND['text_muted']};
        margin: 3px 0 0 0;
    }}

    /* ── Status badge ────────────────────────────────────────────────────── */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.3px;
    }}
    .badge-critical {{
        background: rgba(231,76,60,0.15);
        color: {BRAND['critical']};
        border: 1px solid rgba(231,76,60,0.3);
    }}
    .badge-healthy {{
        background: rgba(39,174,96,0.15);
        color: {BRAND['healthy']};
        border: 1px solid rgba(39,174,96,0.3);
    }}
    .badge-warning {{
        background: rgba(232,146,28,0.15);
        color: {BRAND['orange']};
        border: 1px solid rgba(232,146,28,0.3);
    }}

    /* ── KPI Cards ───────────────────────────────────────────────────────── */
    .kpi-card {{
        background: {BRAND['card']};
        border: 1px solid {BRAND['border']};
        border-top: 2px solid transparent;
        border-radius: 10px;
        padding: 16px 16px 14px 16px;
        text-align: left;
        box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        transition: all 0.2s ease;
        min-height: 120px;
        position: relative;
        overflow: hidden;
    }}
    .kpi-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: {BRAND['blue']};
        border-radius: 10px 10px 0 0;
    }}
    .kpi-card.critical::before {{ background: {BRAND['critical']}; }}
    .kpi-card.healthy::before  {{ background: {BRAND['healthy']}; }}
    .kpi-card.warning::before  {{ background: {BRAND['orange']}; }}
    .kpi-card:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        border-color: #2A3A5A;
    }}
    .kpi-icon-row {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        margin-bottom: 10px;
    }}
    .kpi-icon {{ font-size: 1.1rem; }}
    .kpi-trend {{ font-size: 0.7rem; }}
    .kpi-label {{
        font-size: 0.68rem;
        color: {BRAND['text_muted']};
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin: 0 0 4px 0;
        font-weight: 600;
    }}
    .kpi-value {{
        font-size: 1.55rem;
        font-weight: 700;
        color: {BRAND['text']};
        margin: 0;
        line-height: 1.1;
        letter-spacing: -0.5px;
    }}
    .kpi-value.critical {{ color: {BRAND['critical']}; }}
    .kpi-value.healthy  {{ color: {BRAND['healthy']}; }}
    .kpi-value.warning  {{ color: {BRAND['orange']}; }}
    .kpi-sub {{
        font-size: 0.68rem;
        color: {BRAND['text_dim']};
        margin: 4px 0 0 0;
    }}

    /* ── Section header (ClickUp section title) ──────────────────────────── */
    .section-header {{
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 24px 0 14px 0;
    }}
    .section-header-line {{
        flex: 1;
        height: 1px;
        background: {BRAND['border']};
    }}
    .section-header h3 {{
        color: {BRAND['text_muted']};
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin: 0;
        white-space: nowrap;
    }}

    /* ── Alerts ──────────────────────────────────────────────────────────── */
    .alert-critical {{
        background: rgba(231,76,60,0.08);
        border: 1px solid rgba(231,76,60,0.25);
        border-left: 3px solid {BRAND['critical']};
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 0.85rem;
        color: {BRAND['text']};
    }}
    .alert-warning {{
        background: rgba(232,146,28,0.08);
        border: 1px solid rgba(232,146,28,0.25);
        border-left: 3px solid {BRAND['orange']};
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 0.85rem;
        color: {BRAND['text']};
    }}
    .alert-success {{
        background: rgba(39,174,96,0.08);
        border: 1px solid rgba(39,174,96,0.25);
        border-left: 3px solid {BRAND['healthy']};
        border-radius: 8px;
        padding: 10px 14px;
        margin: 6px 0;
        font-size: 0.85rem;
        color: {BRAND['text']};
    }}

    /* ── Content cards ───────────────────────────────────────────────────── */
    .content-card {{
        background: {BRAND['card']};
        border: 1px solid {BRAND['border']};
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
    }}
    .content-card-title {{
        color: {BRAND['text']};
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 0 14px 0;
        padding-bottom: 10px;
        border-bottom: 1px solid {BRAND['border']};
        display: flex;
        align-items: center;
        gap: 8px;
    }}

    /* ── Buttons ─────────────────────────────────────────────────────────── */
    .stButton > button, .stDownloadButton > button {{
        background: {BRAND['card2']} !important;
        color: {BRAND['text']} !important;
        border: 1px solid {BRAND['border']} !important;
        border-radius: 7px !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        transition: all 0.15s !important;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        background: {BRAND['orange']} !important;
        border-color: {BRAND['orange']} !important;
        color: #fff !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(232,146,28,0.3) !important;
    }}

    /* ── DataFrames ──────────────────────────────────────────────────────── */
    [data-testid="stDataFrame"] {{
        border: 1px solid {BRAND['border']};
        border-radius: 8px;
        overflow: hidden;
    }}

    /* ── Plotly charts ───────────────────────────────────────────────────── */
    .stPlotlyChart {{
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid {BRAND['border']};
    }}

    /* ── Text area ───────────────────────────────────────────────────────── */
    textarea {{
        background-color: {BRAND['card']} !important;
        color: {BRAND['text']} !important;
        border: 1px solid {BRAND['border']} !important;
        border-radius: 8px !important;
        font-size: 0.875rem !important;
    }}

    /* ── Selectbox / Slider ──────────────────────────────────────────────── */
    [data-testid="stSelectbox"] > div, [data-testid="stSlider"] > div {{
        color: {BRAND['text']};
    }}

    /* ── Upload status pill ──────────────────────────────────────────────── */
    .upload-status {{
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.78rem;
        font-weight: 500;
        margin: 8px 0;
    }}
    .upload-status.loaded {{
        background: rgba(39,174,96,0.1);
        border: 1px solid rgba(39,174,96,0.2);
        color: {BRAND['healthy']};
    }}
    .upload-status.empty {{
        background: rgba(26,42,74,0.5);
        border: 1px solid {BRAND['border']};
        color: {BRAND['text_muted']};
    }}

    /* ── Divider ─────────────────────────────────────────────────────────── */
    hr {{ border-color: {BRAND['border']} !important; }}

    /* ── Sidebar scrollbar ───────────────────────────────────────────────── */
    [data-testid="stSidebar"] ::-webkit-scrollbar {{ width: 4px; }}
    [data-testid="stSidebar"] ::-webkit-scrollbar-track {{ background: transparent; }}
    [data-testid="stSidebar"] ::-webkit-scrollbar-thumb {{
        background: {BRAND['border']};
        border-radius: 4px;
    }}

    /* ── Sample download buttons in sidebar ──────────────────────────────── */
    [data-testid="stSidebar"] .stDownloadButton > button {{
        font-size: 0.78rem !important;
        padding: 4px 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "", icon: str = "", badge: str = "", badge_level: str = "") -> None:
    badge_html = ""
    if badge:
        badge_html = f'<span class="status-badge badge-{badge_level}">{badge}</span>'
    st.markdown(f"""
    <div class="page-header">
        <div>
            <p class="page-breadcrumb">GrowthData Analytics &nbsp;/&nbsp; {title}</p>
            <h1 class="page-title">{icon}&nbsp; {title}</h1>
            <p class="page-subtitle">{subtitle}</p>
        </div>
        <div>{badge_html}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = "") -> None:
    st.markdown(f"""
    <div class="section-header">
        <div class="section-header-line"></div>
        <h3>{title}</h3>
        <div class="section-header-line"></div>
    </div>
    """, unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<p style="color:{BRAND["text_muted"]};font-size:0.78rem;margin:-8px 0 12px 0;">{subtitle}</p>',
                    unsafe_allow_html=True)


def render_kpi_card(label, sublabel, value, icon, status="neutral", delta=None) -> None:
    value_class = status if status in ("critical", "healthy", "warning") else ""
    trend = {"critical": "🔴", "healthy": "🟢", "warning": "🟠", "neutral": "⚪"}.get(status, "")
    delta_html = f'<p class="kpi-sub">{delta}</p>' if delta else f'<p class="kpi-sub">{sublabel}</p>'
    st.markdown(f"""
    <div class="kpi-card {status}">
        <div class="kpi-icon-row">
            <span class="kpi-icon">{icon}</span>
            <span class="kpi-trend">{trend}</span>
        </div>
        <p class="kpi-label">{label}</p>
        <p class="kpi-value {value_class}">{value}</p>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_alert(message: str, level: str = "warning") -> None:
    icons = {"critical": "🔴", "warning": "🟠", "success": "✅"}
    st.markdown(f'<div class="alert-{level}">{icons.get(level,"ℹ️")} {message}</div>',
                unsafe_allow_html=True)
