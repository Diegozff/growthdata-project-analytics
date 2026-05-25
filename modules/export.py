"""
Export Module — Excel and PDF report generation.
"""

from __future__ import annotations
import io
import datetime
import pandas as pd
import numpy as np


# ── EXCEL EXPORT ─────────────────────────────────────────────────────────────
def export_to_excel(
    df: pd.DataFrame,
    totals: dict,
    project_notes: str = "",
) -> bytes:
    """
    Generate a styled Excel workbook with:
    - Sheet 1: Executive Summary (KPIs)
    - Sheet 2: EVM Data Table
    - Sheet 3: Raw Input Data
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        workbook = writer.book

        # ── Formats ──────────────────────────────────────────────────────
        hdr_fmt = workbook.add_format({
            "bold": True, "font_color": "#FFFFFF",
            "bg_color": "#1A3A6E", "border": 1,
            "align": "center", "valign": "vcenter", "font_size": 10,
        })
        title_fmt = workbook.add_format({
            "bold": True, "font_color": "#4A90D9",
            "font_size": 16, "align": "left",
        })
        sub_fmt = workbook.add_format({
            "font_color": "#8FA8C8", "font_size": 9, "italic": True,
        })
        kpi_label_fmt = workbook.add_format({
            "bold": True, "font_color": "#8FA8C8",
            "bg_color": "#0D1F35", "font_size": 9,
            "align": "right", "valign": "vcenter", "border": 1,
        })
        kpi_val_fmt = workbook.add_format({
            "bold": True, "font_color": "#E8EDF5",
            "bg_color": "#1A2B4A", "font_size": 12,
            "align": "center", "valign": "vcenter",
            "num_format": '#,##0.00', "border": 1,
        })
        kpi_red_fmt = workbook.add_format({
            "bold": True, "font_color": "#E74C3C",
            "bg_color": "#2B0D0D", "font_size": 12,
            "align": "center", "valign": "vcenter",
            "num_format": '0.000', "border": 1,
        })
        kpi_green_fmt = workbook.add_format({
            "bold": True, "font_color": "#27AE60",
            "bg_color": "#0D2B1A", "font_size": 12,
            "align": "center", "valign": "vcenter",
            "num_format": '0.000', "border": 1,
        })
        currency_fmt = workbook.add_format({
            "num_format": '"$"#,##0.00', "border": 1,
            "bg_color": "#0D1F35", "font_color": "#E8EDF5",
        })
        pct_fmt = workbook.add_format({
            "num_format": '0.00"%"', "border": 1,
            "bg_color": "#0D1F35", "font_color": "#E8EDF5", "align": "center",
        })
        red_cell_fmt = workbook.add_format({
            "num_format": '"$"#,##0.00', "border": 1,
            "bg_color": "#2B0D0D", "font_color": "#E74C3C", "bold": True,
        })
        green_cell_fmt = workbook.add_format({
            "num_format": '"$"#,##0.00', "border": 1,
            "bg_color": "#0D2B1A", "font_color": "#27AE60", "bold": True,
        })
        data_fmt = workbook.add_format({
            "border": 1, "bg_color": "#0D1F35", "font_color": "#E8EDF5", "font_size": 9,
        })
        notes_fmt = workbook.add_format({
            "font_color": "#E8EDF5", "bg_color": "#0D1F35",
            "text_wrap": True, "valign": "top", "border": 1,
        })

        # ════════════════════════════════════════════════════════════════════
        # SHEET 1 — Executive Summary
        # ════════════════════════════════════════════════════════════════════
        ws1 = workbook.add_worksheet("Resumen Ejecutivo")
        ws1.set_tab_color("#4A90D9")
        ws1.hide_gridlines(2)
        ws1.set_column("A:A", 28)
        ws1.set_column("B:B", 22)
        ws1.set_column("C:C", 28)
        ws1.set_column("D:D", 22)
        ws1.set_row(0, 35)
        ws1.set_row(1, 18)

        ws1.write("A1", "GrowthData Analytics LLC — Reporte Ejecutivo EVM", title_fmt)
        ws1.write("A2", f"Generado: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')} | Tareas analizadas: {totals['n_tasks']}", sub_fmt)

        # KPI table
        kpis = [
            ("Presupuesto Planificado (PV)",   totals["total_PV"],  "currency"),
            ("Costo Real Ejecutado (AC)",       totals["total_AC"],  "currency"),
            ("Valor Ganado (EV)",               totals["total_EV"],  "currency"),
            ("Variación de Costo (CV)",         totals["CV"],        "currency_cv"),
            ("Variación de Cronograma (SV)",    totals["SV"],        "currency_cv"),
            ("Avance Físico Ponderado",         totals["avance_ponderado"], "pct"),
            ("CPI — Índ. Rendimiento Costo",    totals["CPI"],       "index"),
            ("SPI — Índ. Rendimiento Cronograma", totals["SPI"],     "index"),
            ("EAC — Costo Estimado al Cierre",  totals["EAC"],       "currency"),
            ("VAC — Variación al Cierre",       totals["VAC"],       "currency_cv"),
            ("TCPI — Perf. Requerida al Cierre",totals["TCPI"],      "index"),
            ("Tareas en Zona Crítica (CPI<1)",  totals["n_critical"],"count"),
        ]

        row = 4
        ws1.write(row - 1, 0, "INDICADORES CLAVE DE RENDIMIENTO", hdr_fmt)
        ws1.write(row - 1, 1, "VALOR",                            hdr_fmt)
        ws1.write(row - 1, 2, "INDICADOR",                        hdr_fmt)
        ws1.write(row - 1, 3, "VALOR",                            hdr_fmt)

        for i, (lbl, val, ftype) in enumerate(kpis):
            r   = row + i // 2
            col = (i % 2) * 2
            ws1.write(r, col,     lbl, kpi_label_fmt)
            if ftype == "index":
                fmt = kpi_green_fmt if val >= 1 else kpi_red_fmt
                ws1.write(r, col + 1, val, fmt)
            elif ftype == "currency_cv":
                fmt = green_cell_fmt if val >= 0 else red_cell_fmt
                ws1.write(r, col + 1, val, fmt)
            elif ftype == "pct":
                ws1.write(r, col + 1, val, pct_fmt)
            elif ftype == "count":
                ws1.write(r, col + 1, int(val), kpi_val_fmt)
            else:
                ws1.write(r, col + 1, val, currency_fmt)

        # Notes
        note_row = row + len(kpis) // 2 + 2
        ws1.write(note_row, 0, "MINUTA DEL ESTADO DE OBRA", hdr_fmt)
        ws1.merge_range(note_row, 0, note_row, 3, "MINUTA DEL ESTADO DE OBRA", hdr_fmt)
        ws1.set_row(note_row + 1, 120)
        ws1.merge_range(note_row + 1, 0, note_row + 1, 3,
                        project_notes or "(Sin comentarios registrados)", notes_fmt)

        # ════════════════════════════════════════════════════════════════════
        # SHEET 2 — EVM Data Table
        # ════════════════════════════════════════════════════════════════════
        evm_cols = ["task_id", "Subcontratista", "Fecha_Reporte",
                    "PV", "AC", "Avance_Fisico", "EV",
                    "CV", "SV", "CPI", "SPI", "status"]
        available = [c for c in evm_cols if c in df.columns]
        df_evm    = df[available].copy()
        df_evm["Fecha_Reporte"] = df_evm["Fecha_Reporte"].dt.strftime("%d/%m/%Y")

        df_evm.to_excel(writer, sheet_name="Datos EVM", index=False, startrow=1)
        ws2 = writer.sheets["Datos EVM"]
        ws2.set_tab_color("#27AE60")
        ws2.hide_gridlines(2)

        # Header row styling
        headers = {
            "task_id": "Tarea / EDT", "Subcontratista": "Subcontratista",
            "Fecha_Reporte": "Fecha", "PV": "PV ($)", "AC": "AC ($)",
            "Avance_Fisico": "Avance (%)", "EV": "EV ($)",
            "CV": "CV ($)", "SV": "SV ($)", "CPI": "CPI", "SPI": "SPI",
            "status": "Estado",
        }
        col_widths = [18, 22, 12, 14, 14, 10, 14, 14, 14, 8, 8, 18]
        for ci, col_name in enumerate(available):
            ws2.write(1, ci, headers.get(col_name, col_name), hdr_fmt)
            ws2.set_column(ci, ci, col_widths[ci] if ci < len(col_widths) else 12)

        ws2.write("A1", "GrowthData Analytics — Tabla de Datos EVM", title_fmt)

        # Conditional formatting on CPI / SPI columns
        for col_name in ["CPI", "SPI"]:
            if col_name in available:
                ci = available.index(col_name)
                col_letter = chr(ord("A") + ci)
                ws2.conditional_format(
                    f"{col_letter}3:{col_letter}{len(df_evm)+2}",
                    {"type": "cell", "criteria": "<", "value": 1,
                     "format": workbook.add_format({"font_color": "#E74C3C", "bold": True})}
                )

        # ════════════════════════════════════════════════════════════════════
        # SHEET 3 — Raw Data
        # ════════════════════════════════════════════════════════════════════
        df_raw = df.copy()
        df_raw["Fecha_Reporte"] = df_raw["Fecha_Reporte"].dt.strftime("%d/%m/%Y")
        df_raw.to_excel(writer, sheet_name="Datos Origen", index=False, startrow=1)
        ws3 = writer.sheets["Datos Origen"]
        ws3.set_tab_color("#7F8C8D")
        ws3.write("A1", "GrowthData Analytics — Datos de Origen Cargados", title_fmt)
        for ci, col_name in enumerate(df_raw.columns):
            ws3.write(1, ci, str(col_name), hdr_fmt)
            ws3.set_column(ci, ci, 16)

    return output.getvalue()


# ── PDF EXPORT ───────────────────────────────────────────────────────────────
def export_to_pdf(
    totals: dict,
    df: pd.DataFrame,
    project_notes: str = "",
    logo_path: str | None = None,
) -> bytes:
    """
    Generate a professional PDF report using fpdf2.
    """
    from fpdf import FPDF, XPos, YPos

    def _s(text: str) -> str:
        """Sanitize text for Helvetica (latin-1): replace non-encodable chars."""
        return (
            text
            .replace("—", "--")   # em-dash → --
            .replace("–", "-")    # en-dash → -
            .replace("·", ".")    # middle dot → .
            .replace("’", "'")    # right single quote → '
            .replace("‘", "'")    # left single quote → '
            .replace("“", '"')    # left double quote → "
            .replace("”", '"')    # right double quote → "
            .encode("latin-1", errors="replace").decode("latin-1")
        )

    class _Report(FPDF):
        DARK_BG   = (10, 22, 40)
        CARD_BG   = (26, 43, 74)
        BLUE      = (74, 144, 217)
        GREEN     = (39, 174, 96)
        RED       = (231, 76, 60)
        ORANGE    = (243, 156, 18)
        LIGHT     = (232, 237, 245)
        MUTED     = (143, 168, 200)
        WHITE     = (255, 255, 255)

        def header(self):
            self.set_fill_color(*self.DARK_BG)
            self.rect(0, 0, 210, 28, "F")
            if logo_path:
                try:
                    self.image(logo_path, x=8, y=4, h=18)
                    logo_offset = 40
                except Exception:
                    logo_offset = 8
            else:
                logo_offset = 8
            self.set_xy(logo_offset, 8)
            self.set_font("Helvetica", "B", 13)
            self.set_text_color(*self.BLUE)
            self.cell(0, 6, "GrowthData Analytics LLC", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_x(logo_offset)
            self.set_font("Helvetica", "", 7)
            self.set_text_color(*self.MUTED)
            self.cell(0, 4, "Project Controls & Earned Value Management Platform")
            self.set_y(30)

        def footer(self):
            self.set_y(-14)
            self.set_fill_color(*self.DARK_BG)
            self.rect(0, self.get_y() - 2, 210, 16, "F")
            self.set_font("Helvetica", "I", 7)
            self.set_text_color(*self.MUTED)
            self.cell(0, 6,
                      f"GrowthData Analytics LLC  |  Reporte generado: "
                      f"{datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}  |  "
                      f"Pagina {self.page_no()}/{{nb}}",
                      align="C")

    pdf = _Report(orientation="P", unit="mm", format="A4")
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(True, margin=18)
    pdf.set_margins(12, 32, 12)
    pdf.add_page()

    # ── Dark background ───────────────────────────────────────────────────
    pdf.set_fill_color(*_Report.DARK_BG)
    pdf.rect(0, 0, 210, 297, "F")

    # ── Report title ──────────────────────────────────────────────────────
    pdf.set_font("Helvetica", "B", 15)
    pdf.set_text_color(*_Report.LIGHT)
    pdf.cell(0, 8, _s("REPORTE EJECUTIVO DE CONTROL DE PROYECTO"), align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*_Report.MUTED)
    pdf.cell(0, 5,
             _s(f"Analisis EVM -- {totals['n_tasks']} tareas  |  Fecha: "
             f"{datetime.date.today().strftime('%d/%m/%Y')}"),
             align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # ── Section helper ────────────────────────────────────────────────────
    def section_title(text: str):
        pdf.set_fill_color(*_Report.CARD_BG)
        pdf.set_draw_color(*_Report.BLUE)
        pdf.set_font("Helvetica", "B", 9)
        pdf.set_text_color(*_Report.LIGHT)
        pdf.set_line_width(0.8)
        pdf.cell(186, 7, _s(f"  {text}"), border="LB", fill=True,
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)

    # ── KPI Grid ──────────────────────────────────────────────────────────
    section_title("INDICADORES CLAVE DE RENDIMIENTO (EVM)")

    kpi_pairs = [
        ("Presupuesto Planificado (PV)", f"${totals['total_PV']:,.2f}", None),
        ("Costo Real Ejecutado (AC)",    f"${totals['total_AC']:,.2f}", None),
        ("Valor Ganado (EV)",            f"${totals['total_EV']:,.2f}", None),
        ("Avance Fisico Ponderado",      f"{totals['avance_ponderado']:.1f}%", None),
        ("CPI - Rendimiento de Costo",   f"{totals['CPI']:.4f}",
            _Report.GREEN if totals['CPI'] >= 1 else _Report.RED),
        ("SPI - Rendimiento de Cronograma", f"{totals['SPI']:.4f}",
            _Report.GREEN if totals['SPI'] >= 1 else _Report.RED),
        ("Variacion de Costo (CV)",      f"${totals['CV']:+,.2f}",
            _Report.GREEN if totals['CV'] >= 0 else _Report.RED),
        ("Variacion de Cronograma (SV)", f"${totals['SV']:+,.2f}",
            _Report.GREEN if totals['SV'] >= 0 else _Report.RED),
        ("EAC - Costo Estimado al Cierre", f"${totals['EAC']:,.2f}",
            _Report.GREEN if totals['EAC'] <= totals['total_PV'] else _Report.RED),
        ("VAC - Variacion al Cierre",    f"${totals['VAC']:+,.2f}",
            _Report.GREEN if totals['VAC'] >= 0 else _Report.RED),
        ("TCPI - Rendimiento Requerido", f"{totals['TCPI']:.4f}",
            _Report.GREEN if totals['TCPI'] <= 1 else _Report.ORANGE),
        ("Tareas Criticas (CPI < 1)",    str(totals['n_critical']),
            _Report.RED if totals['n_critical'] > 0 else _Report.GREEN),
    ]

    card_w, card_h = 91, 16
    x_start = pdf.get_x()
    for i, (lbl, val, color) in enumerate(kpi_pairs):
        col_x = x_start + (i % 2) * (card_w + 4)
        if i % 2 == 0 and i > 0:
            pdf.ln(card_h + 2)
        elif i == 0:
            pass  # first item
        pdf.set_xy(col_x, pdf.get_y())

        # Card background
        pdf.set_fill_color(*_Report.CARD_BG)
        pdf.rect(col_x, pdf.get_y(), card_w, card_h, "F")

        # Label
        pdf.set_xy(col_x + 2, pdf.get_y() + 1)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(*_Report.MUTED)
        pdf.cell(card_w - 4, 5, lbl, new_x=XPos.LEFT, new_y=YPos.NEXT)
        # Value
        pdf.set_x(col_x + 2)
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(*(color if color else _Report.LIGHT))
        pdf.cell(card_w - 4, 7, val)

    pdf.ln(card_h + 6)

    # ── Alerts ───────────────────────────────────────────────────────────
    section_title("ALERTAS Y DIAGNÓSTICO")

    def alert_row(icon: str, text: str, color):
        pdf.set_fill_color(*color)
        pdf.rect(pdf.get_x(), pdf.get_y(), 4, 7, "F")
        pdf.set_x(pdf.get_x() + 5)
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(*_Report.LIGHT)
        pdf.cell(181, 7, f"{icon}  {text}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)

    if totals["CPI"] < 1:
        pct = (1 - totals["CPI"]) * 100
        alert_row("COSTO", _s(f"Proyecto con SOBRECOSTO - CPI={totals['CPI']:.3f} ({pct:.1f}% sobre presupuesto ejecutado)"), _Report.RED)
    else:
        alert_row("COSTO", _s(f"Costo bajo control - CPI={totals['CPI']:.3f} (proyecto dentro de presupuesto)"), _Report.GREEN)

    if totals["SPI"] < 1:
        alert_row("CRONOGRAMA", _s(f"Proyecto RETRASADO - SPI={totals['SPI']:.3f} (avance por debajo de lo planificado)"), _Report.RED)
    else:
        alert_row("CRONOGRAMA", _s(f"Cronograma bajo control - SPI={totals['SPI']:.3f}"), _Report.GREEN)

    if totals["EAC"] > totals["total_PV"]:
        overrun = totals["EAC"] - totals["total_PV"]
        alert_row("PROYECCION", _s(f"EAC supera BAC en ${overrun:,.0f} - revision de contingencia requerida"), _Report.ORANGE)

    if totals["n_critical"] > 0:
        alert_row("TAREAS", _s(f"{totals['n_critical']} tarea(s) en zona critica (CPI < 1.0) requieren intervencion inmediata"), _Report.RED)

    pdf.ln(4)

    # ── Top 10 critical tasks table ───────────────────────────────────────
    section_title("TOP 10 TAREAS CRÍTICAS (CPI MÁS BAJO)")

    critical = df.nsmallest(10, "CPI")[
        ["task_id", "Subcontratista", "PV", "AC", "EV", "CV", "CPI", "SPI", "Avance_Fisico"]
    ]

    col_widths_t = [30, 34, 20, 20, 18, 10, 10, 16]
    headers_t    = ["Tarea/EDT", "Subcontratista", "PV ($)", "AC ($)", "CV ($)", "CPI", "SPI", "Avance (%)"]

    pdf.set_fill_color(*_Report.CARD_BG)
    pdf.set_text_color(*_Report.LIGHT)
    pdf.set_font("Helvetica", "B", 7)
    for w, h in zip(col_widths_t, headers_t):
        pdf.cell(w, 6, h, border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 7)
    for _, row_data in critical.iterrows():
        row_vals = [
            _s(str(row_data["task_id"])[:20]),
            _s(str(row_data["Subcontratista"])[:22]),
            f"${row_data['PV']:,.0f}",
            f"${row_data['AC']:,.0f}",
            f"${row_data['CV']:+,.0f}",
            f"{row_data['CPI']:.3f}",
            f"{row_data['SPI']:.3f}",
            f"{row_data['Avance_Fisico']:.1f}%",
        ]
        cpi_val = row_data["CPI"]
        for j, (w, v) in enumerate(zip(col_widths_t, row_vals)):
            if j == 5:  # CPI column
                pdf.set_text_color(*(_Report.RED if cpi_val < 1 else _Report.GREEN))
                pdf.set_font("Helvetica", "B", 7)
            else:
                pdf.set_text_color(*_Report.LIGHT)
                pdf.set_font("Helvetica", "", 7)
            pdf.cell(w, 5, v, border=1, align="R" if j > 1 else "L")
        pdf.ln()

    pdf.ln(4)

    # ── Project notes ─────────────────────────────────────────────────────
    section_title("MINUTA DEL ESTADO DE OBRA")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*_Report.LIGHT)
    pdf.set_fill_color(*_Report.CARD_BG)
    content = _s(project_notes.strip()) if project_notes.strip() else "(Sin comentarios registrados por el Director de Obra)"
    pdf.multi_cell(186, 6, content, border=1, fill=True)

    # ── Signature block ───────────────────────────────────────────────────
    pdf.ln(8)
    pdf.set_draw_color(*_Report.BLUE)
    pdf.set_line_width(0.3)
    pdf.line(12, pdf.get_y(), 100, pdf.get_y())
    pdf.line(110, pdf.get_y(), 198, pdf.get_y())
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*_Report.MUTED)
    pdf.cell(93, 5, "Director de Obra / Project Manager", align="C")
    pdf.cell(93, 5, "Controller / Responsable de Costos", align="C")

    pdf_output = io.BytesIO()
    pdf_bytes  = pdf.output()
    return bytes(pdf_bytes)
