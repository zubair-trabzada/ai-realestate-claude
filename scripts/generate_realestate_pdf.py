#!/usr/bin/env python3
"""
AI Real Estate Property Report PDF Generator — AI Real Estate Claude Code Skills
Generates professional 6-page PDF property reports with Property Score gauge,
property details, comp analysis, cash flow projections, neighborhood scores,
investment analysis, and recommendation sections.

Requires: reportlab (pip install reportlab)

Usage:
  python3 generate_realestate_pdf.py                        # Demo mode
  python3 generate_realestate_pdf.py --demo                 # Demo mode (explicit)
  python3 generate_realestate_pdf.py data.json              # From JSON
  python3 generate_realestate_pdf.py data.json output.pdf   # From JSON with custom output
"""

import sys
import json
import os
import math
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, PageBreak)
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Line, Wedge
except ImportError:
    print("Error: reportlab is required. Install with: pip install reportlab")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color palette — Real Estate theme
# ---------------------------------------------------------------------------
COLORS = {
    "navy": HexColor("#1a2332"),              # Primary navy
    "navy_light": HexColor("#243347"),        # Lighter navy
    "forest_green": HexColor("#2d8a4e"),      # Forest green (primary accent)
    "green_light": HexColor("#3aaf63"),       # Light green
    "warm_gold": HexColor("#c9982e"),         # Warm gold
    "gold_light": HexColor("#e0b84a"),        # Light gold
    "danger": HexColor("#d9534f"),            # Danger red
    "sky_blue": HexColor("#4a9eff"),          # Sky blue (info)
    "gray": HexColor("#78909c"),              # Muted gray
    "light_bg": HexColor("#f5f7fa"),          # Light background
    "text": HexColor("#1e293b"),              # Dark text
    "text_light": HexColor("#64748b"),        # Light text
    "border": HexColor("#cbd5e1"),            # Border
    "header_bg": HexColor("#1a2332"),         # Table header (navy)
    "row_alt": HexColor("#f0f4f8"),           # Alternating row
    "white": white,
    "black": black,
}


def score_color(score):
    """Return color based on property score value."""
    if score >= 70:
        return COLORS["forest_green"]
    elif score >= 40:
        return COLORS["warm_gold"]
    else:
        return COLORS["danger"]


def score_grade(score):
    """Return property grade from score."""
    if score >= 85:
        return "A+"
    elif score >= 70:
        return "A"
    elif score >= 55:
        return "B"
    elif score >= 40:
        return "C"
    elif score >= 25:
        return "D"
    else:
        return "F"


def property_signal(score):
    """Return property investment signal from score."""
    if score >= 85:
        return "STRONG BUY"
    elif score >= 70:
        return "BUY"
    elif score >= 55:
        return "HOLD / WATCH"
    elif score >= 40:
        return "CAUTION"
    elif score >= 25:
        return "PASS"
    else:
        return "AVOID"


def signal_color(score):
    """Return color for the property signal."""
    if score >= 70:
        return COLORS["forest_green"]
    elif score >= 55:
        return COLORS["sky_blue"]
    elif score >= 40:
        return COLORS["warm_gold"]
    else:
        return COLORS["danger"]


def draw_score_gauge(score, size=140):
    """Create a circular Property Score gauge with color-coded ring."""
    d = Drawing(size + 20, size + 20)

    cx = size / 2 + 10
    cy = size / 2 + 10

    # Outer ring background
    d.add(Circle(cx, cy, size / 2,
                 fillColor=COLORS["light_bg"], strokeColor=COLORS["navy"], strokeWidth=2))

    # Score arc (colored ring)
    color = score_color(score)
    inner_r = size / 2 - 8
    d.add(Circle(cx, cy, inner_r,
                 fillColor=color, strokeColor=None))

    # White center
    d.add(Circle(cx, cy, inner_r - 14,
                 fillColor=COLORS["white"], strokeColor=None))

    # Score text
    d.add(String(cx, cy + 2, str(int(score)),
                 fontSize=36, fillColor=COLORS["navy"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    # "/ 100" label
    d.add(String(cx, cy - 18, "/ 100",
                 fontSize=10, fillColor=COLORS["gray"],
                 textAnchor="middle", fontName="Helvetica"))

    return d


def create_bar_chart(categories, scores, width=470, height=200):
    """Create horizontal bar charts for category scores."""
    d = Drawing(width, height)

    bar_height = 20
    gap = 14
    max_bar_width = width - 200
    start_y = height - 25
    label_x = 5
    bar_x = 170

    for i, (cat, score) in enumerate(zip(categories, scores)):
        y = start_y - i * (bar_height + gap)

        # Category label
        d.add(String(label_x, y + 5, cat[:25],
                     fontSize=9, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica"))

        # Background bar
        d.add(Rect(bar_x, y, max_bar_width, bar_height,
                   fillColor=COLORS["light_bg"], strokeColor=None, rx=3))

        # Score bar — color coded by range
        bar_width = max((score / 100) * max_bar_width, 2)
        color = score_color(score)
        d.add(Rect(bar_x, y, bar_width, bar_height,
                   fillColor=color, strokeColor=None, rx=3))

        # Score label
        d.add(String(bar_x + max_bar_width + 10, y + 5, f"{int(score)}/100",
                     fontSize=10, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica-Bold"))

    return d


def create_neighborhood_bar_chart(categories, scores, width=470, height=160):
    """Create horizontal bar chart for neighborhood scores."""
    d = Drawing(width, height)

    bar_height = 18
    gap = 10
    max_bar_width = width - 200
    start_y = height - 20
    label_x = 5
    bar_x = 150

    for i, (cat, score) in enumerate(zip(categories, scores)):
        y = start_y - i * (bar_height + gap)

        d.add(String(label_x, y + 4, cat[:22],
                     fontSize=9, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica"))

        d.add(Rect(bar_x, y, max_bar_width, bar_height,
                   fillColor=COLORS["light_bg"], strokeColor=None, rx=3))

        bar_width = max((score / 100) * max_bar_width, 2)
        if score >= 80:
            color = COLORS["forest_green"]
        elif score >= 60:
            color = COLORS["sky_blue"]
        elif score >= 40:
            color = COLORS["warm_gold"]
        else:
            color = COLORS["danger"]

        d.add(Rect(bar_x, y, bar_width, bar_height,
                   fillColor=color, strokeColor=None, rx=3))

        d.add(String(bar_x + max_bar_width + 10, y + 4, f"{int(score)}/100",
                     fontSize=9, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica-Bold"))

    return d


# ---------------------------------------------------------------------------
# Custom styles
# ---------------------------------------------------------------------------
def get_styles():
    """Create custom paragraph styles for real estate reports."""
    styles = getSampleStyleSheet()

    custom = {
        "title": ParagraphStyle(
            "RETitle", parent=styles["Title"],
            fontSize=28, textColor=COLORS["navy"],
            spaceAfter=4, fontName="Helvetica-Bold",
            leading=34
        ),
        "address": ParagraphStyle(
            "REAddress", parent=styles["Title"],
            fontSize=22, textColor=COLORS["forest_green"],
            spaceAfter=4, fontName="Helvetica-Bold",
            leading=28
        ),
        "price": ParagraphStyle(
            "REPrice", parent=styles["Title"],
            fontSize=36, textColor=COLORS["warm_gold"],
            spaceAfter=4, fontName="Helvetica-Bold",
            leading=42
        ),
        "subtitle": ParagraphStyle(
            "RESubtitle", parent=styles["Normal"],
            fontSize=14, textColor=COLORS["gray"],
            spaceAfter=6, fontName="Helvetica"
        ),
        "heading": ParagraphStyle(
            "REHeading", parent=styles["Heading1"],
            fontSize=20, textColor=COLORS["navy"],
            spaceBefore=16, spaceAfter=10,
            fontName="Helvetica-Bold"
        ),
        "subheading": ParagraphStyle(
            "RESubheading", parent=styles["Heading2"],
            fontSize=14, textColor=COLORS["forest_green"],
            spaceBefore=12, spaceAfter=6,
            fontName="Helvetica-Bold"
        ),
        "body": ParagraphStyle(
            "REBody", parent=styles["Normal"],
            fontSize=10, textColor=COLORS["text"],
            spaceAfter=6, fontName="Helvetica", leading=14
        ),
        "body_small": ParagraphStyle(
            "REBodySmall", parent=styles["Normal"],
            fontSize=8, textColor=COLORS["text"],
            spaceAfter=4, fontName="Helvetica", leading=11
        ),
        "signal": ParagraphStyle(
            "RESignal", parent=styles["Title"],
            fontSize=22, textColor=COLORS["forest_green"],
            spaceAfter=4, fontName="Helvetica-Bold",
            alignment=1
        ),
        "footer": ParagraphStyle(
            "REFooter", parent=styles["Normal"],
            fontSize=7, textColor=COLORS["gray"],
            fontName="Helvetica", leading=10
        ),
        "disclaimer": ParagraphStyle(
            "REDisclaimer", parent=styles["Normal"],
            fontSize=6.5, textColor=COLORS["gray"],
            fontName="Helvetica", leading=9,
            spaceBefore=8
        ),
        "grade_large": ParagraphStyle(
            "REGrade", parent=styles["Title"],
            fontSize=18, textColor=COLORS["navy"],
            spaceAfter=6, fontName="Helvetica-Bold",
            alignment=1
        ),
        "bullet": ParagraphStyle(
            "REBullet", parent=styles["Normal"],
            fontSize=10, textColor=COLORS["text"],
            spaceAfter=4, fontName="Helvetica", leading=14,
            leftIndent=16, bulletIndent=4
        ),
    }
    return custom


# ---------------------------------------------------------------------------
# Table style helpers
# ---------------------------------------------------------------------------
def standard_table_style(extra=None):
    """Return a standard table style with real estate navy header."""
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_bg"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLORS["white"], COLORS["light_bg"]]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if extra:
        cmds.extend(extra)
    return TableStyle(cmds)


DISCLAIMER_TEXT = (
    "DISCLAIMER: This report is generated by AI for educational and research purposes only. "
    "It is NOT financial or investment advice. Real estate values, rental estimates, and "
    "investment projections are AI-generated approximations based on publicly available data. "
    "Always verify all information with licensed professionals — real estate agents, appraisers, "
    "inspectors, and financial advisors — before making any purchase or investment decisions. "
    "The authors and creators of this tool accept no liability for any losses incurred."
)


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------
def generate_report(data, output_path):
    """Generate a professional 6-page property research PDF report."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    S = get_styles()
    elements = []

    address = data.get("address", "123 Main Street, Austin, TX 78701")
    price = data.get("price", "$425,000")
    date_str = data.get("date", datetime.now().strftime("%B %d, %Y"))
    overall_score = data.get("overall_score", 0)
    grade = score_grade(overall_score)
    signal = property_signal(overall_score)
    sig_color = signal_color(overall_score)

    # =====================================================================
    # PAGE 1 — COVER
    # =====================================================================
    elements.append(Spacer(1, 0.5 * inch))
    elements.append(Paragraph("AI Property Analysis Report", S["title"]))
    elements.append(Spacer(1, 30))
    elements.append(Paragraph(address, S["address"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(price, S["price"]))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(f"Generated: {date_str}", S["subtitle"]))
    elements.append(Spacer(1, 30))

    # Property Score gauge
    gauge = draw_score_gauge(overall_score, size=140)
    elements.append(gauge)
    elements.append(Spacer(1, 24))

    # Grade + signal
    color = score_color(overall_score)
    elements.append(Paragraph(
        f'Property Score: <font color="{color.hexval()}">{int(overall_score)}/100</font> '
        f'(Grade: <font color="{color.hexval()}">{grade}</font>)',
        S["grade_large"]
    ))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        f'Signal: <font color="{sig_color.hexval()}">{signal}</font>',
        ParagraphStyle("SignalLine", parent=S["signal"],
                       textColor=sig_color, fontSize=24)
    ))

    elements.append(Spacer(1, 30))

    # Property details mini-table on cover
    prop_details = data.get("property_details", {})
    beds = prop_details.get("beds", "3")
    baths = prop_details.get("baths", "2")
    sqft = prop_details.get("sqft", "1,850")
    year_built = prop_details.get("year_built", "1998")
    lot_size = prop_details.get("lot_size", "0.18 acres")
    prop_type = prop_details.get("property_type", "Single Family Residence")

    details_data = [
        ["Property Type", prop_type, "Year Built", year_built],
        ["Bedrooms", beds, "Bathrooms", baths],
        ["Square Feet", sqft, "Lot Size", lot_size],
    ]
    details_table = Table(details_data, colWidths=[100, 130, 100, 130])
    details_style = [
        ("BACKGROUND", (0, 0), (0, -1), COLORS["light_bg"]),
        ("BACKGROUND", (2, 0), (2, -1), COLORS["light_bg"]),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("TEXTCOLOR", (0, 0), (-1, -1), COLORS["text"]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    details_table.setStyle(TableStyle(details_style))
    elements.append(details_table)

    elements.append(Spacer(1, 24))
    elements.append(Paragraph(DISCLAIMER_TEXT, S["disclaimer"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 2 — SCORE DASHBOARD & COMP ANALYSIS
    # =====================================================================
    elements.append(Paragraph("Score Dashboard", S["heading"]))
    elements.append(Spacer(1, 6))

    categories = data.get("categories", {})
    default_cats = {
        "Value & Comps": {"score": 72, "weight": "25%"},
        "Income Potential": {"score": 68, "weight": "20%"},
        "Neighborhood Quality": {"score": 75, "weight": "20%"},
        "Investment Upside": {"score": 65, "weight": "20%"},
        "Market Conditions": {"score": 70, "weight": "15%"},
    }
    if not categories:
        categories = default_cats

    cat_names = list(categories.keys())
    cat_scores = [categories[c].get("score", 50) if isinstance(categories[c], dict)
                  else categories[c] for c in cat_names]

    # Bar chart
    chart = create_bar_chart(cat_names, cat_scores)
    elements.append(chart)
    elements.append(Spacer(1, 12))

    # Signal badge line
    elements.append(Paragraph(
        f'Property Score: <font color="{color.hexval()}">'
        f'{int(overall_score)}/100</font> &nbsp; | &nbsp; '
        f'Grade: <font color="{color.hexval()}">{grade}</font> &nbsp; | &nbsp; '
        f'Signal: <font color="{sig_color.hexval()}">{signal}</font>',
        ParagraphStyle("SignalBadge", parent=S["body"], fontSize=12,
                       fontName="Helvetica-Bold", alignment=1, spaceAfter=12)
    ))

    # Score breakdown table
    score_data = [["Category", "Score", "Weight", "Status"]]
    for name, sc in zip(cat_names, cat_scores):
        weight = categories[name].get("weight", "--") if isinstance(categories[name], dict) else "--"
        if sc >= 70:
            status = "Strong"
        elif sc >= 40:
            status = "Mixed"
        else:
            status = "Weak"
        score_data.append([name, f"{int(sc)}/100", weight, status])

    score_table = Table(score_data, colWidths=[160, 80, 60, 100])
    score_style_extra = [("ALIGN", (1, 0), (-1, -1), "CENTER")]
    for i, sc in enumerate(cat_scores, 1):
        c = score_color(sc)
        score_style_extra.append(("TEXTCOLOR", (3, i), (3, i), c))
        score_style_extra.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
    score_table.setStyle(standard_table_style(score_style_extra))
    elements.append(score_table)
    elements.append(Spacer(1, 16))

    # Comp analysis summary
    elements.append(Paragraph("Comparable Sales Analysis", S["subheading"]))
    comps = data.get("comps", [])
    default_comps = [
        {"address": "135 Oak Ave", "price": "$412,000", "sqft": "1,780", "price_sqft": "$231", "sold_date": "Mar 2026", "distance": "0.3 mi"},
        {"address": "204 Elm St", "price": "$438,500", "sqft": "1,920", "price_sqft": "$228", "sold_date": "Feb 2026", "distance": "0.5 mi"},
        {"address": "89 Pine Dr", "price": "$405,000", "sqft": "1,750", "price_sqft": "$231", "sold_date": "Jan 2026", "distance": "0.7 mi"},
        {"address": "312 Cedar Ln", "price": "$445,000", "sqft": "2,010", "price_sqft": "$221", "sold_date": "Mar 2026", "distance": "0.4 mi"},
    ]
    if not comps:
        comps = default_comps

    comp_data = [["Address", "Sale Price", "Sq Ft", "$/Sq Ft", "Sold", "Distance"]]
    for c in comps:
        comp_data.append([
            c.get("address", ""), c.get("price", ""), c.get("sqft", ""),
            c.get("price_sqft", ""), c.get("sold_date", ""), c.get("distance", "")
        ])

    comp_table = Table(comp_data, colWidths=[100, 80, 60, 60, 70, 60])
    comp_table.setStyle(standard_table_style([("ALIGN", (1, 0), (-1, -1), "CENTER")]))
    elements.append(comp_table)

    # Comp summary line
    comp_summary = data.get("comp_summary", {})
    avg_price = comp_summary.get("avg_price", "$425,125")
    avg_sqft = comp_summary.get("avg_price_sqft", "$228/sq ft")
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        f'<b>Comp Average:</b> {avg_price} &nbsp; | &nbsp; '
        f'<b>Avg $/Sq Ft:</b> {avg_sqft}',
        ParagraphStyle("CompSummary", parent=S["body"], fontSize=10, alignment=1)
    ))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 3 — CASH FLOW PROJECTION
    # =====================================================================
    elements.append(Paragraph("Cash Flow Projection", S["heading"]))
    elements.append(Spacer(1, 6))

    # Monthly cash flow table
    elements.append(Paragraph("Monthly &amp; Annual Cash Flow", S["subheading"]))
    cashflow = data.get("cashflow", {})

    cf_items = cashflow.get("items", [
        {"item": "Gross Rental Income", "monthly": "$2,200", "annual": "$26,400"},
        {"item": "Vacancy Loss (8%)", "monthly": "-$176", "annual": "-$2,112"},
        {"item": "Effective Gross Income", "monthly": "$2,024", "annual": "$24,288"},
        {"item": "Mortgage (P&I)", "monthly": "-$1,285", "annual": "-$15,420"},
        {"item": "Property Taxes", "monthly": "-$354", "annual": "-$4,250"},
        {"item": "Insurance", "monthly": "-$125", "annual": "-$1,500"},
        {"item": "Maintenance (5%)", "monthly": "-$110", "annual": "-$1,320"},
        {"item": "Property Management (10%)", "monthly": "-$202", "annual": "-$2,429"},
        {"item": "Net Cash Flow", "monthly": "-$52", "annual": "-$631"},
    ])

    cf_data = [["Item", "Monthly", "Annual"]]
    for item in cf_items:
        cf_data.append([item.get("item", ""), item.get("monthly", ""), item.get("annual", "")])

    cf_table = Table(cf_data, colWidths=[220, 110, 110])
    cf_style_extra = [
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
    ]
    # Highlight net cash flow row (last row)
    last_row = len(cf_items)
    cf_style_extra.append(("FONTNAME", (0, last_row), (-1, last_row), "Helvetica-Bold"))
    cf_style_extra.append(("BACKGROUND", (0, last_row), (-1, last_row), COLORS["light_bg"]))
    cf_table.setStyle(standard_table_style(cf_style_extra))
    elements.append(cf_table)
    elements.append(Spacer(1, 16))

    # Investment metrics
    elements.append(Paragraph("Investment Metrics", S["subheading"]))
    inv_metrics = data.get("investment_metrics", {})

    metrics_items = [
        ["Metric", "Value", "Assessment"],
        ["Cap Rate", inv_metrics.get("cap_rate", "5.2%"), inv_metrics.get("cap_rate_status", "Fair — above 5% threshold")],
        ["Cash-on-Cash Return", inv_metrics.get("cash_on_cash", "3.8%"), inv_metrics.get("coc_status", "Below average — aim for 8%+")],
        ["Gross Rent Multiplier", inv_metrics.get("grm", "16.1x"), inv_metrics.get("grm_status", "Average for metro area")],
        ["Debt Service Coverage", inv_metrics.get("dscr", "1.05"), inv_metrics.get("dscr_status", "Tight — lenders prefer 1.25+")],
        ["1% Rule", inv_metrics.get("one_pct", "0.52%"), inv_metrics.get("one_pct_status", "Below 1% — typical for appreciation market")],
        ["Break-Even Occupancy", inv_metrics.get("breakeven", "92%"), inv_metrics.get("breakeven_status", "Tight margin — low vacancy tolerance")],
    ]

    metrics_table = Table(metrics_items, colWidths=[140, 80, 240])
    metrics_table.setStyle(standard_table_style([
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elements.append(metrics_table)

    elements.append(Spacer(1, 16))

    # Mortgage summary
    elements.append(Paragraph("Mortgage Summary", S["subheading"]))
    mortgage = data.get("mortgage", {})

    mort_data = [
        ["Parameter", "Value"],
        ["Purchase Price", mortgage.get("purchase_price", "$425,000")],
        ["Down Payment", mortgage.get("down_payment", "$85,000 (20%)")],
        ["Loan Amount", mortgage.get("loan_amount", "$340,000")],
        ["Interest Rate", mortgage.get("rate", "6.75%")],
        ["Loan Term", mortgage.get("term", "30-year fixed")],
        ["Monthly P&I", mortgage.get("monthly_pi", "$2,205")],
        ["Total Monthly (PITI)", mortgage.get("monthly_piti", "$2,684")],
    ]
    mort_table = Table(mort_data, colWidths=[160, 200])
    mort_style = [
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
        ("FONTNAME", (1, 6), (1, 7), "Helvetica-Bold"),
    ]
    mort_table.setStyle(standard_table_style(mort_style))
    elements.append(mort_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 4 — NEIGHBORHOOD ANALYSIS
    # =====================================================================
    elements.append(Paragraph("Neighborhood Analysis", S["heading"]))
    elements.append(Spacer(1, 6))

    # Neighborhood scores bar chart
    neighborhood = data.get("neighborhood", {})
    hood_scores = neighborhood.get("scores", {
        "School Rating": 78,
        "Safety / Crime": 72,
        "Walkability": 65,
        "Transit Access": 55,
        "Dining & Shopping": 82,
        "Growth Trajectory": 88,
    })

    hood_names = list(hood_scores.keys())
    hood_values = list(hood_scores.values())

    hood_chart = create_neighborhood_bar_chart(hood_names, hood_values)
    elements.append(hood_chart)
    elements.append(Spacer(1, 14))

    # Neighborhood details table
    elements.append(Paragraph("Neighborhood Details", S["subheading"]))
    hood_details = neighborhood.get("details", [
        {"factor": "Top School", "detail": "Austin ISD — Rated 7/10", "notes": "Strong elementary, mixed middle school options"},
        {"factor": "Crime Rate", "detail": "22% below city average", "notes": "Property crime trending down 3 years"},
        {"factor": "Walk Score", "detail": "65 / Somewhat Walkable", "notes": "Groceries and restaurants within 0.5 mi"},
        {"factor": "Median Household Income", "detail": "$78,500", "notes": "12% above metro median"},
        {"factor": "Population Growth (5yr)", "detail": "+8.2%", "notes": "Strong in-migration, new developments"},
        {"factor": "Median Home Value", "detail": "$415,000", "notes": "Up 18% over 3 years"},
    ])

    hood_data = [["Factor", "Detail", "Notes"]]
    for h in hood_details:
        hood_data.append([h.get("factor", ""), h.get("detail", ""),
                          Paragraph(h.get("notes", ""), S["body_small"])])

    hood_table = Table(hood_data, colWidths=[130, 130, 210])
    hood_table.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(hood_table)
    elements.append(Spacer(1, 16))

    # Demographics
    elements.append(Paragraph("Area Demographics &amp; Trends", S["subheading"]))
    demographics = neighborhood.get("demographics", {})
    pop_growth = demographics.get("population_growth", "+8.2% (5-year)")
    median_age = demographics.get("median_age", "34.5 years")
    employment = demographics.get("employment_rate", "96.2%")
    major_employers = demographics.get("major_employers", "Tech sector, University, Healthcare")

    demo_data = [
        ["Demographic", "Value"],
        ["Population Growth", pop_growth],
        ["Median Age", median_age],
        ["Employment Rate", employment],
        ["Major Employers", major_employers],
    ]
    demo_table = Table(demo_data, colWidths=[160, 310])
    demo_table.setStyle(standard_table_style([("ALIGN", (1, 0), (1, -1), "LEFT")]))
    elements.append(demo_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 5 — INVESTMENT ANALYSIS & SCENARIOS
    # =====================================================================
    elements.append(Paragraph("Investment Analysis", S["heading"]))
    elements.append(Spacer(1, 6))

    # Investment strategies
    elements.append(Paragraph("Investment Strategy Comparison", S["subheading"]))
    strategies = data.get("strategies", [])
    default_strategies = [
        {"strategy": "Buy & Hold (Rental)", "projected_return": "7-9% annually", "timeframe": "5-10 years",
         "pros": "Passive income, appreciation, tax benefits",
         "risk": "Vacancy, maintenance, market downturn"},
        {"strategy": "BRRRR", "projected_return": "12-18% CoC", "timeframe": "12-18 months cycle",
         "pros": "Recycle capital, forced appreciation, scale faster",
         "risk": "Rehab overruns, appraisal risk, refi risk"},
        {"strategy": "Fix & Flip", "projected_return": "$35K-55K profit", "timeframe": "4-6 months",
         "pros": "Quick return, no tenant management",
         "risk": "Market timing, rehab costs, holding costs"},
    ]
    if not strategies:
        strategies = default_strategies

    strat_data = [["Strategy", "Projected Return", "Timeframe", "Key Risk"]]
    for s in strategies:
        strat_data.append([s.get("strategy", ""), s.get("projected_return", ""),
                           s.get("timeframe", ""),
                           Paragraph(s.get("risk", ""), S["body_small"])])

    strat_table = Table(strat_data, colWidths=[110, 100, 95, 165])
    strat_table.setStyle(standard_table_style([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
    ]))
    elements.append(strat_table)
    elements.append(Spacer(1, 14))

    # Appreciation projections
    elements.append(Paragraph("Appreciation Projections", S["subheading"]))
    projections = data.get("appreciation_projections", [])
    default_projections = [
        {"year": "Year 1", "conservative": "$429,250", "moderate": "$438,750", "aggressive": "$451,250"},
        {"year": "Year 3", "conservative": "$441,580", "moderate": "$466,915", "aggressive": "$503,235"},
        {"year": "Year 5", "conservative": "$458,240", "moderate": "$500,645", "aggressive": "$565,820"},
        {"year": "Year 10", "conservative": "$510,650", "moderate": "$601,810", "aggressive": "$762,430"},
    ]
    if not projections:
        projections = default_projections

    proj_data = [["Timeline", "Conservative (1%)", "Moderate (3.5%)", "Aggressive (6%)"]]
    for p in projections:
        proj_data.append([p.get("year", ""), p.get("conservative", ""),
                          p.get("moderate", ""), p.get("aggressive", "")])

    proj_table = Table(proj_data, colWidths=[80, 130, 130, 130])
    proj_style = [
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("TEXTCOLOR", (3, 1), (3, -1), COLORS["forest_green"]),
        ("FONTNAME", (3, 1), (3, -1), "Helvetica-Bold"),
    ]
    proj_table.setStyle(standard_table_style(proj_style))
    elements.append(proj_table)
    elements.append(Spacer(1, 14))

    # Scenario analysis
    elements.append(Paragraph("Scenario Analysis", S["subheading"]))
    scenarios = data.get("scenarios", [])
    default_scenarios = [
        {"scenario": "Bull Case", "probability": "25%", "return": "+25% to +40% (5yr)",
         "trigger": "Tech job growth, rate cuts, low inventory, population boom"},
        {"scenario": "Base Case", "probability": "50%", "return": "+10% to +20% (5yr)",
         "trigger": "Steady appreciation, stable rental market, moderate growth"},
        {"scenario": "Bear Case", "probability": "25%", "return": "-5% to -15% (5yr)",
         "trigger": "Job losses, oversupply, rate hikes, recession, natural disaster"},
    ]
    if not scenarios:
        scenarios = default_scenarios

    sc_data = [["Scenario", "Probability", "Expected Return", "Trigger"]]
    for sc in scenarios:
        sc_data.append([sc.get("scenario", ""), sc.get("probability", ""),
                        sc.get("return", ""),
                        Paragraph(sc.get("trigger", ""), S["body_small"])])
    sc_table = Table(sc_data, colWidths=[85, 75, 120, 190])
    sc_style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (2, -1), "CENTER"),
    ]
    if len(scenarios) >= 3:
        sc_style.append(("TEXTCOLOR", (2, 1), (2, 1), COLORS["forest_green"]))
        sc_style.append(("TEXTCOLOR", (2, 2), (2, 2), COLORS["sky_blue"]))
        sc_style.append(("TEXTCOLOR", (2, 3), (2, 3), COLORS["danger"]))
        sc_style.append(("FONTNAME", (2, 1), (2, 3), "Helvetica-Bold"))
    sc_table.setStyle(standard_table_style(sc_style))
    elements.append(sc_table)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 6 — RECOMMENDATION & RISKS
    # =====================================================================
    elements.append(Paragraph("Recommendation &amp; Risk Factors", S["heading"]))
    elements.append(Spacer(1, 6))

    # Recommendation summary
    elements.append(Paragraph("Investment Recommendation", S["subheading"]))
    recommendation = data.get("recommendation", {})
    rec_signal = recommendation.get("signal", signal)
    rec_summary = recommendation.get("summary",
        "This property presents a moderate investment opportunity with solid neighborhood "
        "fundamentals and appreciation potential. Cash flow is thin at current pricing and rates, "
        "making it better suited for a buy-and-hold appreciation play rather than pure cash flow. "
        "The neighborhood's growth trajectory and below-average crime rate are strong positives. "
        "Consider negotiating 3-5% below asking price to improve returns."
    )
    rec_offer = recommendation.get("suggested_offer", "$405,000 - $415,000")
    rec_action = recommendation.get("action_items", [
        "Get a professional inspection — focus on roof, HVAC, and foundation",
        "Request seller concessions for closing costs or rate buydown",
        "Verify rental estimates with 3 local property managers",
        "Review HOA documents if applicable (special assessments, rental restrictions)",
        "Check flood zone status and insurance requirements",
    ])

    # Signal display
    rec_color = signal_color(overall_score)
    elements.append(Paragraph(
        f'Signal: <font color="{rec_color.hexval()}">{rec_signal}</font> &nbsp; | &nbsp; '
        f'Suggested Offer: <font color="{COLORS["forest_green"].hexval()}">{rec_offer}</font>',
        ParagraphStyle("RecLine", parent=S["body"], fontSize=13,
                       fontName="Helvetica-Bold", alignment=1, spaceAfter=12)
    ))

    elements.append(Paragraph(rec_summary, S["body"]))
    elements.append(Spacer(1, 10))

    # Action items
    elements.append(Paragraph("Action Items Before Purchase", S["subheading"]))
    for i, item in enumerate(rec_action, 1):
        elements.append(Paragraph(f"{i}. {item}", S["body"]))
    elements.append(Spacer(1, 14))

    # Risk factors
    elements.append(Paragraph("Risk Factors", S["subheading"]))
    risk_factors = data.get("risk_factors", [])
    default_risks = [
        {"factor": "Market Risk", "probability": "Medium", "impact": "High",
         "notes": "Local market correction, rising rates reducing buyer pool"},
        {"factor": "Vacancy Risk", "probability": "Low-Medium", "impact": "Medium",
         "notes": "Strong rental demand in area, but thin cash flow margin"},
        {"factor": "Maintenance / Capex", "probability": "Medium", "impact": "Medium",
         "notes": "Roof age, HVAC condition, plumbing should be inspected"},
        {"factor": "Regulatory Risk", "probability": "Low", "impact": "Medium",
         "notes": "Rent control proposals, STR restrictions, zoning changes"},
        {"factor": "Natural Disaster", "probability": "Low", "impact": "High",
         "notes": "Check flood zone, wildfire risk, storm/hail history"},
    ]
    if not risk_factors:
        risk_factors = default_risks

    rf_data = [["Risk Factor", "Probability", "Impact", "Notes"]]
    for rf in risk_factors:
        rf_data.append([rf.get("factor", ""), rf.get("probability", ""),
                        rf.get("impact", ""),
                        Paragraph(rf.get("notes", ""), S["body_small"])])
    rf_table = Table(rf_data, colWidths=[110, 80, 65, 215])
    rf_style = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("ALIGN", (1, 0), (2, -1), "CENTER")]
    rf_table.setStyle(standard_table_style(rf_style))
    elements.append(rf_table)

    elements.append(Spacer(1, 20))

    # Footer + disclaimer
    elements.append(Paragraph(
        "Generated by AI Real Estate Analyst for Claude Code", S["footer"]
    ))
    elements.append(Paragraph(DISCLAIMER_TEXT, S["disclaimer"]))

    # Build PDF
    doc.build(elements)
    return output_path


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------
def get_demo_data():
    """Return sample data for demo mode."""
    return {
        "address": "4821 Ridgeview Drive, Austin, TX 78735",
        "price": "$425,000",
        "date": datetime.now().strftime("%B %d, %Y"),
        "overall_score": 72,
        "property_details": {
            "beds": "3",
            "baths": "2",
            "sqft": "1,850",
            "year_built": "1998",
            "lot_size": "0.18 acres",
            "property_type": "Single Family Residence",
        },
        "categories": {
            "Value & Comps": {"score": 74, "weight": "25%"},
            "Income Potential": {"score": 62, "weight": "20%"},
            "Neighborhood Quality": {"score": 78, "weight": "20%"},
            "Investment Upside": {"score": 72, "weight": "20%"},
            "Market Conditions": {"score": 68, "weight": "15%"},
        },
        "comps": [
            {"address": "135 Oak Ave", "price": "$412,000", "sqft": "1,780", "price_sqft": "$231", "sold_date": "Mar 2026", "distance": "0.3 mi"},
            {"address": "204 Elm St", "price": "$438,500", "sqft": "1,920", "price_sqft": "$228", "sold_date": "Feb 2026", "distance": "0.5 mi"},
            {"address": "89 Pine Dr", "price": "$405,000", "sqft": "1,750", "price_sqft": "$231", "sold_date": "Jan 2026", "distance": "0.7 mi"},
            {"address": "312 Cedar Ln", "price": "$445,000", "sqft": "2,010", "price_sqft": "$221", "sold_date": "Mar 2026", "distance": "0.4 mi"},
        ],
        "comp_summary": {
            "avg_price": "$425,125",
            "avg_price_sqft": "$228/sq ft",
        },
        "cashflow": {
            "items": [
                {"item": "Gross Rental Income", "monthly": "$2,200", "annual": "$26,400"},
                {"item": "Vacancy Loss (8%)", "monthly": "-$176", "annual": "-$2,112"},
                {"item": "Effective Gross Income", "monthly": "$2,024", "annual": "$24,288"},
                {"item": "Mortgage (P&I)", "monthly": "-$1,285", "annual": "-$15,420"},
                {"item": "Property Taxes", "monthly": "-$354", "annual": "-$4,250"},
                {"item": "Insurance", "monthly": "-$125", "annual": "-$1,500"},
                {"item": "Maintenance (5%)", "monthly": "-$110", "annual": "-$1,320"},
                {"item": "Property Mgmt (10%)", "monthly": "-$202", "annual": "-$2,429"},
                {"item": "Net Cash Flow", "monthly": "-$52", "annual": "-$631"},
            ],
        },
        "investment_metrics": {
            "cap_rate": "5.2%",
            "cap_rate_status": "Fair — above 5% threshold for metro area",
            "cash_on_cash": "3.8%",
            "coc_status": "Below average — aim for 8%+ for pure cash flow",
            "grm": "16.1x",
            "grm_status": "Average for Austin metro area",
            "dscr": "1.05",
            "dscr_status": "Tight — most lenders require 1.25+",
            "one_pct": "0.52%",
            "one_pct_status": "Below 1% rule — typical for appreciation markets",
            "breakeven": "92%",
            "breakeven_status": "Tight margin — low vacancy tolerance",
        },
        "mortgage": {
            "purchase_price": "$425,000",
            "down_payment": "$85,000 (20%)",
            "loan_amount": "$340,000",
            "rate": "6.75%",
            "term": "30-year fixed",
            "monthly_pi": "$2,205",
            "monthly_piti": "$2,684",
        },
        "neighborhood": {
            "scores": {
                "School Rating": 78,
                "Safety / Crime": 72,
                "Walkability": 65,
                "Transit Access": 55,
                "Dining & Shopping": 82,
                "Growth Trajectory": 88,
            },
            "details": [
                {"factor": "Top School", "detail": "Austin ISD — Rated 7/10", "notes": "Strong elementary, mixed middle school"},
                {"factor": "Crime Rate", "detail": "22% below city avg", "notes": "Property crime trending down 3 years"},
                {"factor": "Walk Score", "detail": "65 / Somewhat Walkable", "notes": "Groceries and restaurants within 0.5 mi"},
                {"factor": "Median Income", "detail": "$78,500", "notes": "12% above metro median"},
                {"factor": "Pop. Growth (5yr)", "detail": "+8.2%", "notes": "Strong in-migration, new developments"},
                {"factor": "Median Home Value", "detail": "$415,000", "notes": "Up 18% over 3 years"},
            ],
            "demographics": {
                "population_growth": "+8.2% (5-year)",
                "median_age": "34.5 years",
                "employment_rate": "96.2%",
                "major_employers": "Tech sector, University of Texas, Healthcare",
            },
        },
        "strategies": [
            {"strategy": "Buy & Hold (Rental)", "projected_return": "7-9% annually", "timeframe": "5-10 years",
             "pros": "Passive income, appreciation, tax benefits",
             "risk": "Vacancy, maintenance costs, market downturn"},
            {"strategy": "BRRRR", "projected_return": "12-18% CoC", "timeframe": "12-18 month cycle",
             "pros": "Recycle capital, forced appreciation, scale faster",
             "risk": "Rehab cost overruns, appraisal risk, refi rates"},
            {"strategy": "Fix & Flip", "projected_return": "$35K-55K profit", "timeframe": "4-6 months",
             "pros": "Quick return, no tenant management",
             "risk": "Market timing, rehab costs, holding costs"},
        ],
        "appreciation_projections": [
            {"year": "Year 1", "conservative": "$429,250", "moderate": "$438,750", "aggressive": "$451,250"},
            {"year": "Year 3", "conservative": "$441,580", "moderate": "$466,915", "aggressive": "$503,235"},
            {"year": "Year 5", "conservative": "$458,240", "moderate": "$500,645", "aggressive": "$565,820"},
            {"year": "Year 10", "conservative": "$510,650", "moderate": "$601,810", "aggressive": "$762,430"},
        ],
        "scenarios": [
            {"scenario": "Bull Case", "probability": "25%", "return": "+25% to +40% (5yr)",
             "trigger": "Tech hiring boom, rate cuts, low inventory persists"},
            {"scenario": "Base Case", "probability": "50%", "return": "+10% to +20% (5yr)",
             "trigger": "Steady appreciation, stable rental market, moderate growth"},
            {"scenario": "Bear Case", "probability": "25%", "return": "-5% to -15% (5yr)",
             "trigger": "Tech layoffs, oversupply from new builds, rate hikes"},
        ],
        "recommendation": {
            "signal": "BUY",
            "summary": (
                "This property presents a solid buy-and-hold opportunity in a high-growth Austin "
                "neighborhood. Cash flow is thin at current interest rates, but the neighborhood's "
                "strong appreciation trajectory (18% over 3 years) and population growth (+8.2%) "
                "make it a compelling appreciation play. The property scores well on comps — priced "
                "at fair market value with room for negotiation. School ratings and declining crime "
                "support long-term demand. Best suited for investors with a 5+ year horizon who "
                "prioritize equity growth over immediate cash flow."
            ),
            "suggested_offer": "$405,000 - $415,000",
            "action_items": [
                "Get a professional inspection — home is 28 years old, check roof, HVAC, plumbing",
                "Request seller concessions for 2-1 rate buydown to improve Year 1 cash flow",
                "Verify rental estimates with 3 local property managers before closing",
                "Check flood zone status and get insurance quotes (Austin has flood-prone areas)",
                "Run title search — confirm no liens, easements, or encumbrances",
            ],
        },
        "risk_factors": [
            {"factor": "Market Risk", "probability": "Medium", "impact": "High",
             "notes": "Austin saw 15% correction in 2022-23; cyclical risk remains"},
            {"factor": "Vacancy Risk", "probability": "Low-Med", "impact": "Medium",
             "notes": "Strong rental demand, but new supply coming online in 2026-27"},
            {"factor": "Maintenance / Capex", "probability": "Medium", "impact": "Medium",
             "notes": "1998 build — HVAC, water heater, roof may need replacement within 5 years"},
            {"factor": "Interest Rate Risk", "probability": "Medium", "impact": "Medium",
             "notes": "Rate drops improve refinance and buyer pool; rate hikes hurt both"},
            {"factor": "Natural Disaster", "probability": "Low", "impact": "High",
             "notes": "Austin has flood and hail risk; verify flood zone and insurance coverage"},
        ],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--demo":
        # Demo mode
        data = get_demo_data()
        output = "PROPERTY-REPORT-sample.pdf"
        generate_report(data, output)
        print(f"Sample report generated: {output}")
        return

    # JSON input mode
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "PROPERTY-REPORT.pdf"

    with open(input_file, "r") as f:
        data = json.load(f)

    generate_report(data, output_file)
    print(f"Report generated: {output_file}")


if __name__ == "__main__":
    main()
