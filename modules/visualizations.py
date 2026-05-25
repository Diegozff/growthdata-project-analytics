"""
Visualizations Module — Plotly charts with dark corporate theme.
All charts share a unified GrowthData brand palette.
"""
from __future__ import annotations

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ── Brand palette (GrowthData: Navy #1B3566 | Blue #3D7EC5 | Orange #E8921C) ─
COLORS = {
    "pv":           "#3D7EC5",   # Medium blue (logo) — Planned Value
    "ac":           "#E74C3C",   # Red               — Actual Cost
    "ev":           "#27AE60",   # Green             — Earned Value
    "orange":       "#E8921C",   # Brand orange      — accents / highlights
    "navy":         "#1B3566",   # Brand dark navy
    "critical":     "#E74C3C",
    "warning":      "#E8921C",   # use brand orange for warnings
    "healthy":      "#27AE60",
    "neutral":      "#6B88A8",
    "grid":         "#1A3060",
    "bg":           "#0D1E38",
    "bg_paper":     "#08111E",
    "text":         "#E8EDF5",
    "text_muted":   "#8FA8C8",
    "quadrant_q1":  "rgba(39,174,96,0.07)",
    "quadrant_q2":  "rgba(232,146,28,0.07)",
    "quadrant_q3":  "rgba(231,76,60,0.12)",
    "quadrant_q4":  "rgba(232,146,28,0.07)",
}

_BASE_LAYOUT = dict(
    paper_bgcolor=COLORS["bg_paper"],
    plot_bgcolor=COLORS["bg"],
    font=dict(color=COLORS["text"], family="Inter, Segoe UI, system-ui, sans-serif", size=12),
    margin=dict(l=50, r=30, t=60, b=50),
    legend=dict(
        bgcolor="rgba(13,30,56,0.85)",
        bordercolor=COLORS["navy"],
        borderwidth=1,
        font=dict(size=11),
    ),
    hoverlabel=dict(
        bgcolor="#0F2044",
        bordercolor=COLORS["orange"],
        font=dict(color=COLORS["text"], size=12),
    ),
)

_AXIS_STYLE = dict(
    gridcolor=COLORS["grid"],
    zerolinecolor=COLORS["grid"],
    linecolor=COLORS["grid"],
    tickfont=dict(color=COLORS["text_muted"]),
    title_font=dict(color=COLORS["text_muted"]),
)


def _apply_base(fig: go.Figure, title: str, height: int = 420) -> go.Figure:
    fig.update_layout(
        **_BASE_LAYOUT,
        title=dict(
            text=title,
            font=dict(size=15, color=COLORS["orange"]),
            x=0.01,
            xanchor="left",
        ),
        height=height,
    )
    return fig


# ── Chart 1: S-Curve ────────────────────────────────────────────────────────
def plot_s_curve(s_data: pd.DataFrame) -> go.Figure:
    """Cumulative S-Curve: PV vs AC vs EV over time."""
    single_period = len(s_data) <= 1

    fig = go.Figure()

    if single_period:
        # Bar comparison for single-period snapshot
        categories = ["PV (Planificado)", "AC (Costo Real)", "EV (Valor Ganado)"]
        values     = [
            s_data["PV"].iloc[0],
            s_data["AC"].iloc[0],
            s_data["EV"].iloc[0],
        ]
        colors_bar = [COLORS["pv"], COLORS["ac"], COLORS["ev"]]
        fig.add_trace(go.Bar(
            x=categories, y=values,
            marker_color=colors_bar,
            text=[f"${v:,.0f}" for v in values],
            textposition="outside",
            textfont=dict(color=COLORS["text"], size=12),
        ))
        fig.update_layout(showlegend=False)
        fig.update_yaxes(tickprefix="$", tickformat=",.0f", **_AXIS_STYLE)
        fig.update_xaxes(**_AXIS_STYLE)
        title = "📊 Comparativa EVM — Período Único (sin datos temporales suficientes)"
    else:
        # Full S-Curve with cumulative lines
        x_dates = s_data["Fecha_Reporte"]

        traces = [
            ("PV_cum", "PV — Presupuesto Planificado", COLORS["pv"], "dot"),
            ("AC_cum", "AC — Costo Real Ejecutado",   COLORS["ac"], "solid"),
            ("EV_cum", "EV — Valor Ganado",            COLORS["ev"], "solid"),
        ]
        for col, name, color, dash in traces:
            fig.add_trace(go.Scatter(
                x=x_dates, y=s_data[col],
                mode="lines+markers",
                name=name,
                line=dict(color=color, width=2.5, dash=dash),
                marker=dict(size=6, symbol="circle"),
                hovertemplate=f"<b>{name}</b><br>Fecha: %{{x|%d/%m/%Y}}<br>Valor: $%{{y:,.0f}}<extra></extra>",
                fill=None,
            ))

        # Shaded area between AC and EV (cost variance zone)
        fig.add_trace(go.Scatter(
            x=pd.concat([x_dates, x_dates[::-1]]).reset_index(drop=True),
            y=pd.concat([s_data["AC_cum"], s_data["EV_cum"][::-1]]).reset_index(drop=True),
            fill="toself",
            fillcolor="rgba(231,76,60,0.08)",
            line=dict(width=0),
            name="Zona de Sobrecosto",
            showlegend=True,
            hoverinfo="skip",
        ))

        fig.update_xaxes(title="Fecha de Reporte", **_AXIS_STYLE)
        fig.update_yaxes(title="Valor Acumulado ($)", tickprefix="$", tickformat=",.0f", **_AXIS_STYLE)
        title = "📈 Curva S — Evolución Temporal Acumulada (PV / AC / EV)"

    return _apply_base(fig, title, height=440)


# ── Chart 2: SPI vs CPI Scatter (Quadrant) ──────────────────────────────────
def plot_scatter_quadrant(df: pd.DataFrame) -> go.Figure:
    """Scatter plot of tasks by CPI (Y) and SPI (X) with quadrant zones."""

    fig = go.Figure()

    # Quadrant background rectangles
    quad_configs = [
        # (x0, x1, y0, y1, color, label, label_x, label_y)
        (1.0, 2.5, 1.0, 2.5, COLORS["quadrant_q1"], "✅ Bajo Ppto / Adelantado", 1.8, 2.3),
        (0.0, 1.0, 1.0, 2.5, COLORS["quadrant_q2"], "⚠️ Sobre Ppto / Adelantado", 0.5, 2.3),
        (0.0, 1.0, 0.0, 1.0, COLORS["quadrant_q3"], "🔴 CRÍTICO\nSobre Ppto / Retrasado", 0.5, 0.15),
        (1.0, 2.5, 0.0, 1.0, COLORS["quadrant_q4"], "⚠️ Bajo Ppto / Retrasado",  1.8, 0.15),
    ]
    for x0, x1, y0, y1, color, label, lx, ly in quad_configs:
        fig.add_shape(type="rect", x0=x0, x1=x1, y0=y0, y1=y1,
                      fillcolor=color, line=dict(width=0), layer="below")
        fig.add_annotation(x=lx, y=ly, text=label, showarrow=False,
                           font=dict(size=9, color=COLORS["text_muted"]),
                           align="center", xanchor="center", yanchor="middle")

    # Reference lines at 1.0
    for val, axis in [(1.0, "x"), (1.0, "y")]:
        if axis == "x":
            fig.add_vline(x=val, line=dict(color=COLORS["neutral"], width=1.2, dash="dash"))
        else:
            fig.add_hline(y=val, line=dict(color=COLORS["neutral"], width=1.2, dash="dash"))

    # Color per task status
    def _color(row):
        if row["CPI"] >= 1 and row["SPI"] >= 1:
            return COLORS["healthy"]
        elif row["CPI"] < 0.85 or row["SPI"] < 0.85:
            return COLORS["critical"]
        return COLORS["warning"]

    df = df.copy()
    df["_color"] = df.apply(_color, axis=1)
    df["_size"]  = df["PV"].apply(lambda v: max(8, min(30, v / df["PV"].max() * 28 + 6)))

    fig.add_trace(go.Scatter(
        x=df["SPI"],
        y=df["CPI"],
        mode="markers+text",
        text=df["task_id"].str[:10],
        textposition="top center",
        textfont=dict(size=8, color=COLORS["text_muted"]),
        marker=dict(
            color=df["_color"],
            size=df["_size"],
            opacity=0.85,
            line=dict(color="rgba(255,255,255,0.2)", width=1),
        ),
        customdata=df[["task_id", "PV", "AC", "EV", "CV", "Subcontratista"]],
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "SPI: %{x:.3f}  |  CPI: %{y:.3f}<br>"
            "PV: $%{customdata[1]:,.0f}<br>"
            "AC: $%{customdata[2]:,.0f}<br>"
            "EV: $%{customdata[3]:,.0f}<br>"
            "CV: $%{customdata[4]:,.0f}<br>"
            "Subcontratista: %{customdata[5]}<extra></extra>"
        ),
        name="Tareas",
    ))

    fig.update_xaxes(title="SPI — Índice de Rendimiento de Cronograma",
                     range=[0, 2.5], **_AXIS_STYLE)
    fig.update_yaxes(title="CPI — Índice de Rendimiento de Costo",
                     range=[0, 2.5], **_AXIS_STYLE)

    return _apply_base(
        fig,
        "🎯 Mapa de Rendimiento — CPI vs SPI por Tarea (tamaño = PV)",
        height=480,
    )


# ── Chart 3: Pareto de Subcontratistas ──────────────────────────────────────
def plot_pareto_subcontractors(pareto_df: pd.DataFrame) -> go.Figure:
    """Bar chart + Pareto line of cost variance by subcontractor."""

    if pareto_df.empty:
        fig = go.Figure()
        return _apply_base(fig, "Sin datos de subcontratistas", 300)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    bar_colors = [
        COLORS["critical"] if v < 0 else COLORS["healthy"]
        for v in pareto_df["CV"]
    ]

    # Bars — Cost Variance per subcontractor
    fig.add_trace(
        go.Bar(
            x=pareto_df["Subcontratista"],
            y=pareto_df["CV"],
            name="Variación de Costo (CV)",
            marker=dict(color=bar_colors, opacity=0.9,
                        line=dict(color="rgba(255,255,255,0.1)", width=0.5)),
            customdata=pareto_df[["AC", "PV", "CPI", "n_tasks"]],
            hovertemplate=(
                "<b>%{x}</b><br>"
                "CV: $%{y:,.0f}<br>"
                "AC: $%{customdata[0]:,.0f}<br>"
                "PV: $%{customdata[1]:,.0f}<br>"
                "CPI: %{customdata[2]:.3f}<br>"
                "Tareas: %{customdata[3]}<extra></extra>"
            ),
            text=[f"${v:,.0f}" for v in pareto_df["CV"]],
            textposition="outside",
            textfont=dict(size=10, color=COLORS["text"]),
        ),
        secondary_y=False,
    )

    # Pareto line (only for negative CV rows)
    neg_mask = pareto_df["cum_pct"].notna() & (pareto_df["CV"] < 0)
    if neg_mask.any():
        fig.add_trace(
            go.Scatter(
                x=pareto_df.loc[neg_mask, "Subcontratista"],
                y=pareto_df.loc[neg_mask, "cum_pct"],
                mode="lines+markers",
                name="% Acumulado Desvío",
                line=dict(color=COLORS["warning"], width=2.5, dash="dot"),
                marker=dict(size=7, color=COLORS["warning"]),
                hovertemplate="%{x}<br>Pareto: %{y:.1f}%<extra></extra>",
            ),
            secondary_y=True,
        )
        # 80% reference line
        fig.add_hline(y=80, line=dict(color=COLORS["warning"], width=1, dash="dash"),
                      secondary_y=True, annotation_text="80%",
                      annotation_font_color=COLORS["warning"])

    fig.update_yaxes(title_text="Variación de Costo — CV ($)",
                     tickprefix="$", tickformat=",.0f",
                     secondary_y=False, **_AXIS_STYLE)
    fig.update_yaxes(title_text="Pareto — % Acumulado de Desvíos",
                     secondary_y=True, range=[0, 105],
                     ticksuffix="%", **_AXIS_STYLE)
    fig.update_xaxes(title="Subcontratista", **_AXIS_STYLE,
                     tickangle=-30)

    fig.update_layout(**_BASE_LAYOUT, height=440,
                      title=dict(
                          text="📊 Pareto de Desvíos por Subcontratista — Variación de Costo (CV)",
                          font=dict(size=15, color=COLORS["orange"]),
                          x=0.01,
                      ))

    return fig


# ── Chart 4: Task Status Gauge / Summary ────────────────────────────────────
def plot_project_gauge(avance: float, cpi: float, spi: float) -> go.Figure:
    """Three gauges: overall progress, CPI, SPI."""
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
        subplot_titles=["Avance Físico Global", "CPI — Rendimiento de Costo",
                        "SPI — Rendimiento de Cronograma"],
    )

    def _gauge(value, ref, suffix="", min_=0, max_=2):
        color = COLORS["healthy"] if value >= ref else (
            COLORS["critical"] if value < ref * 0.85 else COLORS["warning"]
        )
        return go.Indicator(
            mode="gauge+number+delta",
            value=round(value, 3),
            delta={"reference": ref, "valueformat": ".3f"},
            number={"suffix": suffix, "font": {"size": 30, "color": COLORS["text"]}},
            gauge=dict(
                axis=dict(range=[min_, max_], tickcolor=COLORS["text_muted"],
                          tickfont=dict(color=COLORS["text_muted"])),
                bar=dict(color=color, thickness=0.25),
                bgcolor=COLORS["bg"],
                borderwidth=1,
                bordercolor=COLORS["grid"],
                steps=[
                    dict(range=[min_, ref * 0.85], color="rgba(231,76,60,0.15)"),
                    dict(range=[ref * 0.85, ref], color="rgba(243,156,18,0.15)"),
                    dict(range=[ref, max_],        color="rgba(39,174,96,0.15)"),
                ],
                threshold=dict(line=dict(color=COLORS["text_muted"], width=2),
                               thickness=0.75, value=ref),
            ),
        )

    fig.add_trace(_gauge(avance, 100, suffix="%", min_=0, max_=100), row=1, col=1)
    fig.add_trace(_gauge(cpi, 1.0, min_=0, max_=2), row=1, col=2)
    fig.add_trace(_gauge(spi, 1.0, min_=0, max_=2), row=1, col=3)

    fig.update_layout(
        **_BASE_LAYOUT,
        height=280,
        title=dict(text="⚙️ Rendimiento Global del Proyecto",
                   font=dict(size=15, color=COLORS["orange"]), x=0.01),
    )
    # Subplot title color fix
    for ann in fig.layout.annotations:
        ann.font.color = COLORS["orange"]
        ann.font.size  = 10
        ann.font.family = "Inter, Segoe UI, sans-serif"

    return fig
