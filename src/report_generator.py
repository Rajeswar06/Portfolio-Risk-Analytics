# ==========================================================
# PDF Report Generator
# ==========================================================
#
# This module generates a professional PDF report for the
# Portfolio Risk Analytics project.
#
# The report contains:
#
# • Company Information
# • Investment Summary
# • Performance Metrics
# • Value at Risk Metrics
# • Monte Carlo Price Paths
# • Distribution of Final Simulated Prices
#
# The generated report is downloaded directly from the
# Streamlit dashboard.
# ==========================================================


# ==========================================================
# Import Required Libraries
# ==========================================================

import os
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


# ==========================================================
# Image Locations
# ==========================================================

BASE_DIR = os.path.dirname(__file__)

MC_IMAGE = os.path.join(
    BASE_DIR,
    "monte_carlo_paths.png"
)

DIST_IMAGE = os.path.join(
    BASE_DIR,
    "distribution.png"
)


# ==========================================================
# Generate Portfolio PDF Report
# ==========================================================

def generate_pdf(report):
    """
    Generate a Portfolio Risk Analytics PDF report.

    Parameters
    ----------
    report : dict
        Dictionary containing all portfolio metrics
        calculated in dashboard.py.

    Returns
    -------
    BytesIO
        PDF report stored in memory.
    """

    # ======================================================
    # Create PDF Buffer
    # ======================================================

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        rightMargin=0.5 * inch,
        leftMargin=0.5 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch
    )

    # ======================================================
    # Register Unicode Font
    # ======================================================
    #
    # DejaVu Sans is used so that Unicode symbols such as
    # the Indian Rupee (₹) display correctly.
    #
    # ======================================================

    font_path = os.path.join(
        BASE_DIR,
        "DejaVuSans.ttf"
    )

    pdfmetrics.registerFont(
        TTFont(
            "DejaVu",
            font_path
        )
    )

    # ======================================================
    # PDF Styles
    # ======================================================

    styles = getSampleStyleSheet()

    styles["Title"].fontName = "DejaVu"
    styles["Heading2"].fontName = "DejaVu"
    styles["BodyText"].fontName = "DejaVu"

    story = []

    # ======================================================
    # Report Title
    # ======================================================

    title = Paragraph(
        "<font size=22><b>Portfolio Risk Analytics Report</b></font>",
        styles["Title"]
    )

    story.append(title)

    story.append(Spacer(1, 20))

    # ======================================================
    # Report Sections
    # ======================================================

    sections = [

        (
            "Company Information",
            [
                ["Company", report["Company"]],
                ["Ticker", report["Ticker"]],
                ["Sector", report["Sector"]],
                ["Industry", report["Industry"]],
                ["Benchmark", report["Benchmark"]],
                ["Analysis Period", report["Analysis Period"]]
            ]
        ),

        (
            "Investment Summary",
            [
                ["Current Stock Price", report["Current Stock Price"]],
                ["Investment Amount", report["Investment Amount"]],
                ["Current Portfolio Value", report["Current Portfolio Value"]],
                ["Expected Portfolio Value", report["Expected Portfolio Value"]],
                ["Best Portfolio Value", report["Best Portfolio Value"]],
                ["Worst Portfolio Value", report["Worst Portfolio Value"]]
            ]
        ),

        (
            "Performance Metrics",
            [
                ["CAGR", report["CAGR"]],
                ["Annual Volatility", report["Annual Volatility"]],
                ["Sharpe Ratio", report["Sharpe Ratio"]],
                ["Sortino Ratio", report["Sortino Ratio"]],
                ["Beta", report["Beta"]],
                ["Alpha", report["Alpha"]]
            ]
        ),

        (
            "Value at Risk",
            [
                ["Historical VaR", report["Historical VaR"]],
                ["Parametric VaR", report["Parametric VaR"]],
                ["Conditional VaR", report["Conditional VaR"]],
                ["Monte Carlo VaR", report["Monte Carlo VaR"]],
                ["Probability of Loss", report["Probability of Loss"]]
            ]
        )

    ]

    # ======================================================
    # Build Tables
    # ======================================================

    for heading, rows in sections:

        story.append(
            Paragraph(
                f"<b>{heading}</b>",
                styles["Heading2"]
            )
        )

        table = Table(
            rows,
            colWidths=[220, 220]
        )

        table.setStyle(

            TableStyle([

                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    colors.whitesmoke
                ),

                (
                    "FONTNAME",
                    (0, 0),
                    (-1, -1),
                    "DejaVu"
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                )

            ])

        )

        story.append(table)

        story.append(Spacer(1, 20))

    # ======================================================
    # Monte Carlo Price Paths
    # ======================================================

    if os.path.exists(MC_IMAGE):

        story.append(

            Paragraph(
                "<b>Monte Carlo Price Simulation</b>",
                styles["Heading2"]
            )

        )

        story.append(

            Image(
                MC_IMAGE,
                width=450,
                height=250
            )

        )

        story.append(
            Spacer(1, 20)
        )

    # ======================================================
    # Final Price Distribution
    # ======================================================

    if os.path.exists(DIST_IMAGE):

        story.append(

            Paragraph(
                "<b>Distribution of Final Simulated Prices</b>",
                styles["Heading2"]
            )

        )

        story.append(

            Image(
                DIST_IMAGE,
                width=450,
                height=250
            )

        )

    # ======================================================
    # Build PDF
    # ======================================================

    doc.build(story)

    buffer.seek(0)

    return buffer