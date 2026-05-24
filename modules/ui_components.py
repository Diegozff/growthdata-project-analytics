"""
UI Components — Custom CSS injection, KPI cards, section headers.
Brand palette: Navy #1B3566 | Blue #3D7EC5 | Orange #E8921C
"""

import streamlit as st

# ── Brand tokens (single source of truth) ────────────────────────────────────
BRAND = {
    "orange":       "#E8921C",   # PRIMARY — logo orange / CTA
    "navy":         "#1B3566",   # logo dark navy
    "blue":         "#3D7EC5",   # logo medium blue
    "bg":           "#08111E",   # page background
    "card":         "#0D1E38",   # card / sidebar background
    "border":       "#1A3060",   # subtle border
    "border_acc":   "#E8921C",   # accent border (orange)
    "text":         "#E8EDF5",   # primary text
    "text_muted":   "#8FA8C8",   # secondary text
    "critical":     "#E74C3C",   # red alert
    "warning":      "#F5A623",   # amber warning (close to orange brand)
    "healthy":      "#27AE60",   # green OK
}


def apply_custom_css() -> None:
    """Inject global CSS aligned with GrowthData brand identity."""
    st.markdown(f"""
    <style>
    /* ── Google Font ───────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
    }}
    .stApp {{ background-color: {BRAND['bg']}; }}

    /* ── Main container ─────────────────────────────────────────────────── */
    .main .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1440px;
    }}

    /* ── Sidebar ────────────────────────────────────────────────────────── */
    [data-testid="stSidebar"] {{
        background-color: {BRAND['card']};
        border-right: 1px solid {BRAND['border']};
    }}
    [data-testid="stSidebar"] .block-container {{ padding-top: 1rem; }}

    /* ── Dividers ───────────────────────────────────────────────────────── */
    hr {{ border-color: {BRAND['border']} !important; margin: 1rem 0; }}

    /* ── File uploader ──────────────────────────────────────────────────── */
    [data-testid="stFileUploader"] {{
        border: 1.5px dashed {BRAND['navy']};
        border-radius: 10px;
        padding: 6px;
        background: rgba(27,53,102,0.18);
    }}

    /* ── Buttons ────────────────────────────────────────────────────────── */
    .stButton > button, .stDownloadButton > button {{
        background: linear-gradient(135deg, {BRAND['navy']}, #1E4080);
        color: {BRAND['text']};
        border: 1px solid {BRAND['orange']};
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }}
    .stButton > button:hover, .stDownloadButton > button:hover {{
        background: linear-gradient(135deg, {BRAND['orange']}, #c97618);
        border-color: {BRAND['orange']};
        color: #fff;
        transform: translateY(-1px);
        box-shadow: 0 4px 14px rgba(232,146,28,0.35);
    }}

    /* ── DataFrames ─────────────────────────────────────────────────────── */
    [data-testid="stDataFrame"] {{
        border: 1px solid {BRAND['border']};
        border-radius: 8px;
        overflow: hidden;
    }}

    /* ── Plotly charts ──────────────────────────────────────────────────── */
    .stPlotlyChart {{ border-radius: 12px; overflow: hidden; }}

    /* ── Tabs ───────────────────────────────────────────────────────────── */
    [data-testid="stTabs"] [role="tab"] {{
        color: {BRAND['text_muted']};
        border-radius: 8px 8px 0 0;
    }}
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {{
        color: {BRAND['orange']};
        border-bottom: 2px solid {BRAND['orange']};
        font-weight: 600;
    }}

    /* ── Text area ──────────────────────────────────────────────────────── */
    textarea {{
        background-color: {BRAND['card']} !important;
        color: {BRAND['text']} !important;
        border: 1px solid {BRAND['navy']} !important;
        border-radius: 8px !important;
    }}

    /* ── Slider / Select ────────────────────────────────────────────────── */
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stSlider"] > div {{ color: {BRAND['text']}; }}

    /* ── Alerts ─────────────────────────────────────────────────────────── */
    .alert-critical {{
        background: rgba(231,76,60,0.12);
        border: 1px solid {BRAND['critical']};
        border-left: 4px solid {BRAND['critical']};
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
    }}
    .alert-warning {{
        background: rgba(232,146,28,0.12);
        border: 1px solid {BRAND['orange']};
        border-left: 4px solid {BRAND['orange']};
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
    }}
    .alert-success {{
        background: rgba(39,174,96,0.12);
        border: 1px solid {BRAND['healthy']};
        border-left: 4px solid {BRAND['healthy']};
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
    }}

    /* ── Section header ─────────────────────────────────────────────────── */
    .section-header {{
        background: linear-gradient(90deg, rgba(27,53,102,0.55), transparent);
        padding: 10px 18px;
        border-left: 4px solid {BRAND['orange']};
        border-radius: 4px;
        margin: 24px 0 12px 0;
    }}
    .section-header h3 {{ color: {BRAND['text']}; margin: 0 0 2px 0; font-size: 1rem; font-weight: 600; }}
    .section-header p  {{ color: {BRAND['text_muted']}; margin: 0; font-size: 0.78rem; }}

    /* ── KPI Cards ──────────────────────────────────────────────────────── */
    .kpi-card {{
        background: linear-gradient(145deg, #0F2144 0%, {BRAND['card']} 100%);
        border: 1px solid {BRAND['navy']};
        border-radius: 14px;
        padding: 18px 14px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
        transition: transform 0.2s;
        min-height: 140px;
    }}
    .kpi-card:hover {{ transform: translateY(-2px); }}
    .kpi-card.critical {{
        border-color: {BRAND['critical']};
        box-shadow: 0 4px 20px rgba(231,76,60,0.2);
    }}
    .kpi-card.healthy {{
        border-color: {BRAND['healthy']};
        box-shadow: 0 4px 20px rgba(39,174,96,0.2);
    }}
    .kpi-card.warning {{
        border-color: {BRAND['orange']};
        box-shadow: 0 4px 20px rgba(232,146,28,0.18);
    }}
    .kpi-card.neutral {{
        border-color: {BRAND['blue']};
        box-shadow: 0 4px 20px rgba(61,126,197,0.12);
    }}
    .kpi-icon   {{ font-size: 1.5rem; margin-bottom: 6px; }}
    .kpi-label  {{ font-size: 0.72rem; color: {BRAND['orange']}; text-transform: uppercase;
                   letter-spacing: 1px; margin: 0; font-weight: 600; }}
    .kpi-sub    {{ font-size: 0.65rem; color: {BRAND['text_muted']}; margin: 0 0 6px 0; }}
    .kpi-value  {{ font-size: 1.65rem; font-weight: 700; color: {BRAND['text']};
                   margin: 6px 0; line-height: 1.1; }}
    .kpi-value.critical {{ color: {BRAND['critical']}; }}
    .kpi-value.healthy  {{ color: {BRAND['healthy']}; }}
    .kpi-value.warning  {{ color: {BRAND['orange']}; }}
    .kpi-delta  {{ font-size: 0.78rem; margin-top: 4px; color: {BRAND['text_muted']}; }}
    </style>
    """, unsafe_allow_html=True)


def render_kpi_card(
    label: str,
    sublabel: str,
    value: str,
    icon: str,
    status: str = "neutral",
    delta: str | None = None,
) -> None:
    value_class = status if status in ("critical", "healthy", "warning") else ""
    delta_html  = f'<p class="kpi-delta">{delta}</p>' if delta else ""
    st.markdown(f"""
    <div class="kpi-card {status}">
        <div class="kpi-icon">{icon}</div>
        <p class="kpi-label">{label}</p>
        <p class="kpi-sub">{sublabel}</p>
        <div class="kpi-value {value_class}">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title: str, subtitle: str = "") -> None:
    sub_html = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(f"""
    <div class="section-header">
        <h3>{title}</h3>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_alert(message: str, level: str = "warning") -> None:
    icons = {"critical": "🔴", "warning": "🟠", "success": "✅"}
    icon  = icons.get(level, "ℹ️")
    st.markdown(f"""
    <div class="alert-{level}">
        {icon} {message}
    </div>
    """, unsafe_allow_html=True)
