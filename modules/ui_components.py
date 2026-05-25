"""
UI Components — ClickUp-inspired sidebar + GrowthData brand CSS.
Palette: Navy #1B3566 | Blue #3D7EC5 | Orange #E8921C | BG #0F1C35
"""
from __future__ import annotations
import streamlit as st

BRAND = {
    "orange":       "#E8921C",
    "orange_light": "#F5A73A",
    "navy":         "#1B3566",
    "navy_light":   "#244280",
    "blue":         "#3D7EC5",
    "blue_light":   "#5A95D5",
    "bg":           "#0F1C35",   # page background — dark navy (not black)
    "sidebar":      "#0C1628",   # sidebar — slightly darker
    "card":         "#162236",   # card background
    "card_hover":   "#1C2C46",
    "border":       "#1E3454",   # visible but subtle border
    "border_light": "#2A4570",   # accent border
    "text":         "#E8EDF5",
    "text_muted":   "#8AAAC8",
    "text_dim":     "#4A6688",
    "critical":     "#E74C3C",
    "warning":      "#E8921C",
    "healthy":      "#27AE60",
    "white":        "#FFFFFF",
}


def apply_custom_css() -> None:
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif !important;
    }}

    /* ── Page background ─────────────────────────────────────────────────── */
    .stApp {{ background-color: {BRAND['bg']}; }}
    .main .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}

    /* ── Sidebar ─────────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {{
        background-color: {BRAND['sidebar']} !important;
        border-right: 1px solid {BRAND['border']};
    }}
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebar"] .block-container {{
        padding: 0 0 20px 0 !important;
    }}

    /* Logo: white pill so it's visible on dark sidebar */
    [data-testid="stSidebar"] img {{
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 4px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4) !important;
    }}

    /* ── Nav radio → ClickUp nav items ──────────────────────────────────── */
    [data-testid="stSidebar"] .stRadio > label {{ display: none !important; }}
    [data-testid="stSidebar"] .stRadio > div {{
        gap: 2px !important;
        display: flex !important;
        flex-direction: column !important;
    }}
    [data-testid="stSidebar"] .stRadio label {{
        display: flex !important;
        align-items: center !important;
        padding: 9px 16px 9px 20px !important;
        border-radius: 0 8px 8px 0 !important;
        margin: 1px 10px 1px 0 !important;
        cursor: pointer !important;
        color: {BRAND['text_muted']} !important;
        font-size: 0.875rem !important;
        font-weight: 500 !important;
        border-left: 3px solid transparent !important;
        transition: all 0.15s ease !important;
        background: transparent !important;
        min-height: 38px !important;
    }}
    [data-testid="stSidebar"] .stRadio label:hover {{
        background: rgba(61,126,197,0.08) !important;
        color: {BRAND['text']} !important;
        border-left-color: rgba(232,146,28,0.4) !important;
    }}
    [data-testid="stSidebar"] .stRadio label:has(input:checked) {{
        background: rgba(232,146,28,0.12) !important;
        border-left-color: {BRAND['orange']} !important;
        color: {BRAND['orange']} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] .stRadio [role="radio"],
    [data-testid="stSidebar"] .stRadio input[type="radio"] {{ display: none !important; }}
    [data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {{
        margin: 0 !important;
        font-size: 0.875rem !important;
    }}

    /* ── Nav section labels ──────────────────────────────────────────────── */
    .nav-section-label {{
        font-size: 0.63rem !important;
        font-weight: 700 !important;
        color: {BRAND['text_dim']} !important;
        text-transform: uppercase !important;
        letter-spacing: 1.6px !important;
        padding: 14px 20px 5px 20px !important;
        margin: 0 !important;
    }}

    /* ── Sidebar divider ─────────────────────────────────────────────────── */
    hr {{ border-color: {BRAND['border']} !important; margin: 8px 0 !important; }}

    /* ── Upload pill ─────────────────────────────────────────────────────── */
    .upload-status {{
        display: flex; align-items: center; gap: 8px;
        padding: 7px 14px; border-radius: 7px;
        font-size: 0.78rem; font-weight: 500; margin: 6px 0;
    }}
    .upload-status.loaded {{
        background: rgba(39,174,96,0.12);
        border: 1px solid rgba(39,174,96,0.25);
        color: {BRAND['healthy']};
    }}
    .upload-status.empty {{
        background: rgba(30,52,84,0.5);
        border: 1px solid {BRAND['border']};
        color: {BRAND['text_muted']};
    }}

    /* ── File uploader ───────────────────────────────────────────────────── */
    [data-testid="stSidebar"] [data-testid="stFileUploader"] {{
        border: 1.5px dashed {BRAND['navy_light']};
        border-radius: 8px;
        background: rgba(27,53,102,0.15);
        padding: 4px;
        transition: all 0.2s;
    }}
    [data-testid="stSidebar"] [data-testid="stFileUploader"]:hover {{
        border-color: {BRAND['orange']};
        background: rgba(232,146,28,0.06);
    }}

    /* ── Page header ─────────────────────────────────────────────────────── */
    .page-header {{
        padding: 20px 28px 16px 28px;
        border-bottom: 1px solid {BRAND['border']};
        background: linear-gradient(180deg, #132040 0%, {BRAND['bg']} 100%);
    }}
    .page-breadcrumb {{
        font-size: 0.68rem; color: {BRAND['text_dim']};
        margin: 0 0 4px 0; text-transform: uppercase; letter-spacing: 0.8px;
    }}
    .page-title {{
        font-size: 1.3rem; font-weight: 700;
        color: {BRAND['text']}; margin: 0; letter-spacing: -0.4px;
    }}
    .page-subtitle {{
        font-size: 0.76rem; color: {BRAND['text_muted']}; margin: 4px 0 0 0;
    }}

    /* ── Status badges ───────────────────────────────────────────────────── */
    .status-badge {{
        display: inline-flex; align-items: center; gap: 5px;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.7rem; font-weight: 600; letter-spacing: 0.3px;
    }}
    .badge-critical {{ background: rgba(231,76,60,0.15); color:{BRAND['critical']}; border:1px solid rgba(231,76,60,0.3); }}
    .badge-healthy  {{ background: rgba(39,174,96,0.15);  color:{BRAND['healthy']};  border:1px solid rgba(39,174,96,0.3); }}
    .badge-warning  {{ background: rgba(232,146,28,0.15); color:{BRAND['orange']};   border:1px solid rgba(232,146,28,0.3); }}

    /* ── KPI Cards ───────────────────────────────────────────────────────── */
    .kpi-card {{
        background: {BRAND['card']};
        border: 1px solid {BRAND['border']};
        border-top: 3px solid {BRAND['blue']};
        border-radius: 10px;
        padding: 16px 16px 14px 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
        transition: all 0.2s ease;
        min-height: 118px;
    }}
    .kpi-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.35);
        background: {BRAND['card_hover']};
    }}
    .kpi-card.critical {{ border-top-color: {BRAND['critical']}; }}
    .kpi-card.healthy  {{ border-top-color: {BRAND['healthy']}; }}
    .kpi-card.warning  {{ border-top-color: {BRAND['orange']}; }}
    .kpi-icon-row {{ display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px; }}
    .kpi-icon  {{ font-size: 1rem; }}
    .kpi-trend {{ font-size: 0.7rem; }}
    .kpi-label {{
        font-size: 0.67rem; color: {BRAND['text_muted']};
        text-transform: uppercase; letter-spacing: 0.8px;
        margin: 0 0 3px 0; font-weight: 600;
    }}
    .kpi-value {{
        font-size: 1.5rem; font-weight: 700;
        color: {BRAND['text']}; margin: 0;
        line-height: 1.1; letter-spacing: -0.5px;
    }}
    .kpi-value.critical {{ color: {BRAND['critical']}; }}
    .kpi-value.healthy  {{ color: {BRAND['healthy']}; }}
    .kpi-value.warning  {{ color: {BRAND['orange']}; }}
    .kpi-sub {{ font-size: 0.68rem; color: {BRAND['text_dim']}; margin: 4px 0 0 0; }}

    /* ── Section header ──────────────────────────────────────────────────── */
    .section-header {{
        display: flex; align-items: center; gap: 10px;
        margin: 22px 0 12px 0;
    }}
    .section-header-line {{ flex:1; height:1px; background:{BRAND['border']}; }}
    .section-header h3 {{
        color: {BRAND['text_muted']}; font-size: 0.7rem;
        font-weight: 700; text-transform: uppercase;
        letter-spacing: 1.2px; margin: 0; white-space: nowrap;
    }}

    /* ── Alerts ──────────────────────────────────────────────────────────── */
    .alert-critical {{
        background: rgba(231,76,60,0.1); border: 1px solid rgba(231,76,60,0.3);
        border-left: 4px solid {BRAND['critical']}; border-radius: 8px;
        padding: 11px 16px; margin: 6px 0; font-size: 0.84rem; color:{BRAND['text']};
    }}
    .alert-warning {{
        background: rgba(232,146,28,0.1); border: 1px solid rgba(232,146,28,0.3);
        border-left: 4px solid {BRAND['orange']}; border-radius: 8px;
        padding: 11px 16px; margin: 6px 0; font-size: 0.84rem; color:{BRAND['text']};
    }}
    .alert-success {{
        background: rgba(39,174,96,0.1); border: 1px solid rgba(39,174,96,0.3);
        border-left: 4px solid {BRAND['healthy']}; border-radius: 8px;
        padding: 11px 16px; margin: 6px 0; font-size: 0.84rem; color:{BRAND['text']};
    }}

    /* ── Content cards ───────────────────────────────────────────────────── */
    .content-card {{
        background: {BRAND['card']};
        border: 1px solid {BRAND['border']};
        border-radius: 10px; padding: 20px; margin-bottom: 16px;
    }}
    .content-card-title {{
        color: {BRAND['text']}; font-size: 0.85rem; font-weight: 600;
        margin: 0 0 14px 0; padding-bottom: 10px;
        border-bottom: 1px solid {BRAND['border']};
    }}

    /* ── Buttons ─────────────────────────────────────────────────────────── */
    .stButton > button, .stDownloadButton > button {{
        background: {BRAND['navy']} !important;
        color: {BRAND['text']} !important;
        border: 1px solid {BRAND['border_light']} !important;
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
        box-shadow: 0 4px 14px rgba(232,146,28,0.35) !important;
    }}

    /* ── Plotly + DataFrames ─────────────────────────────────────────────── */
    .stPlotlyChart {{ border-radius: 10px; overflow: hidden; border: 1px solid {BRAND['border']}; }}
    [data-testid="stDataFrame"] {{ border: 1px solid {BRAND['border']}; border-radius: 8px; overflow: hidden; }}

    /* ── Text area ───────────────────────────────────────────────────────── */
    textarea {{
        background-color: {BRAND['card']} !important;
        color: {BRAND['text']} !important;
        border: 1px solid {BRAND['border']} !important;
        border-radius: 8px !important;
        font-size: 0.875rem !important;
    }}
    textarea:focus {{
        border-color: {BRAND['orange']} !important;
        box-shadow: 0 0 0 2px rgba(232,146,28,0.15) !important;
    }}

    /* ── Sidebar scrollbar ───────────────────────────────────────────────── */
    [data-testid="stSidebar"] ::-webkit-scrollbar {{ width: 4px; }}
    [data-testid="stSidebar"] ::-webkit-scrollbar-thumb {{
        background: {BRAND['border']}; border-radius: 4px;
    }}

    /* ── Sidebar download buttons ────────────────────────────────────────── */
    [data-testid="stSidebar"] .stDownloadButton > button {{
        font-size: 0.76rem !important;
        padding: 4px 8px !important;
        background: rgba(27,53,102,0.5) !important;
    }}
    </style>
    """, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "", icon: str = "",
                       badge: str = "", badge_level: str = "") -> None:
    badge_html = (f'<span class="status-badge badge-{badge_level}">{badge}</span>'
                  if badge else "")
    st.markdown(f"""
    <div class="page-header">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <p class="page-breadcrumb">GrowthData Analytics &nbsp;›&nbsp; {title}</p>
                <h1 class="page-title">{icon}&nbsp; {title}</h1>
                <p class="page-subtitle">{subtitle}</p>
            </div>
            <div>{badge_html}</div>
        </div>
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
        st.markdown(
            f'<p style="color:{BRAND["text_muted"]};font-size:0.78rem;'
            f'margin:-6px 0 12px 0;">{subtitle}</p>',
            unsafe_allow_html=True,
        )


def render_kpi_card(label: str, sublabel: str, value: str, icon: str,
                    status: str = "neutral", delta: str | None = None) -> None:
    value_cls = status if status in ("critical", "healthy", "warning") else ""
    trend = {"critical": "🔴", "healthy": "🟢", "warning": "🟠"}.get(status, "")
    sub = delta if delta else sublabel
    st.markdown(f"""
    <div class="kpi-card {status}">
        <div class="kpi-icon-row">
            <span class="kpi-icon">{icon}</span>
            <span class="kpi-trend">{trend}</span>
        </div>
        <p class="kpi-label">{label}</p>
        <p class="kpi-value {value_cls}">{value}</p>
        <p class="kpi-sub">{sub}</p>
    </div>
    """, unsafe_allow_html=True)


def render_alert(message: str, level: str = "warning") -> None:
    icons = {"critical": "🔴", "warning": "🟠", "success": "✅"}
    st.markdown(
        f'<div class="alert-{level}">{icons.get(level, "ℹ️")}&nbsp; {message}</div>',
        unsafe_allow_html=True,
    )
