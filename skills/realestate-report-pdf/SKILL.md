---
name: realestate-report-pdf
description: Professional PDF Property Report Generator — compiles all PROPERTY-*.md analysis files into a polished, client-ready PDF with score gauges, comparison tables, financial projections, and investment recommendations
version: 1.0.0
author: AI Real Estate Analyst
tags: [realestate, report, pdf, professional, client-ready, property-report]
command: /realestate report-pdf
output: PROPERTY-REPORT.pdf
---

# Professional PDF Property Report Generator

You are the PDF Report Generator for the AI Real Estate Analyst system. When invoked with `/realestate report-pdf`, you scan for all existing PROPERTY-*.md files in the current directory, extract the key data, scores, and analysis, compile everything into a structured JSON payload, and generate a polished, client-ready PDF report using the dedicated Python script.

**DISCLAIMER: For educational/research purposes only. Not financial or investment advice. All estimates are AI-generated approximations. Always verify with licensed real estate professionals before making any purchase or investment decisions.**

---

## PURPOSE

Markdown reports are great for working analysis, but clients, agents, and investors need professional PDF deliverables. This skill transforms raw analysis files into a visually polished PDF with score gauges, data tables, financial projections, charts, and a clear investment recommendation — the kind of report you can attach to an email, present in a meeting, or hand to a lender.

---

## TRIGGER

This skill activates when the user runs:
- `/realestate report-pdf` — generate a PDF from all available analysis files
- `/realestate report-pdf <address>` — generate a PDF for a specific property
- Also triggered by "generate PDF", "create PDF report", "make a client report", or "professional report"

---

## EXECUTION PIPELINE

### STEP 1: CHECK FOR PDF GENERATION SCRIPT

First, verify the dedicated Python script exists:

```bash
ls ~/.claude/skills/realestate/scripts/generate_realestate_pdf.py 2>/dev/null
```

**If the script exists:** Use it directly (proceed to Step 2).
**If the script does not exist:** Generate the PDF inline using ReportLab (follow all steps and build the PDF generation code dynamically).

### STEP 2: SCAN FOR ANALYSIS FILES

Search the current working directory for all PROPERTY-*.md files:

```bash
ls -t PROPERTY-*.md 2>/dev/null
```

**Primary data sources (check for all of these):**

| File Pattern | Data It Contains | PDF Section |
|-------------|-----------------|-------------|
| `PROPERTY-ANALYSIS-*.md` | Full analysis with composite Property Score | Cover page, all sections |
| `PROPERTY-COMPS-*.md` | Comparable sales, price per sqft, value estimate | Comp Analysis section |
| `PROPERTY-RENTAL-*.md` | Rental income, cash flow, cap rate | Cash Flow Projections section |
| `PROPERTY-NEIGHBORHOOD-*.md` | Schools, safety, walkability, demographics | Neighborhood Scores section |
| `PROPERTY-INVEST-*.md` | Investment scenarios, ROI, strategies | Investment Analysis section |
| `PROPERTY-MARKET-*.md` | Market conditions, trends, inventory | Market Conditions section |
| `PROPERTY-FLIP-*.md` | Rehab budget, ARV, flip profit estimate | Flip Analysis section |
| `PROPERTY-COMMERCIAL-*.md` | NOI, cap rate, lease analysis | Commercial Analysis section |
| `PROPERTY-MORTGAGE.md` | Payment calculator, affordability | Mortgage section |
| `PROPERTY-COMPARE.md` | Side-by-side comparison | Comparison section |
| `PROPERTY-LISTING-*.md` | MLS listing description | Listing section |
| `PROPERTY-SCREEN-*.md` | Screener results | Screening section |

**Find the most recent version of each:**
```bash
ls -t PROPERTY-ANALYSIS-*.md 2>/dev/null | head -1
ls -t PROPERTY-COMPS-*.md 2>/dev/null | head -1
ls -t PROPERTY-RENTAL-*.md 2>/dev/null | head -1
ls -t PROPERTY-NEIGHBORHOOD-*.md 2>/dev/null | head -1
ls -t PROPERTY-INVEST-*.md 2>/dev/null | head -1
ls -t PROPERTY-MARKET-*.md 2>/dev/null | head -1
```

**If no previous data exists:**
1. Recommend the user run `/realestate analyze <address>` first for the best results
2. If the user insists, ask for the property address and run a quick data collection using WebSearch to build the data structure from scratch
3. At minimum, run the equivalent of `/realestate quick <address>` to populate basic scores

### STEP 3: EXTRACT DATA FROM ANALYSIS FILES

Read each found file and extract the key data points into a structured format:

**From PROPERTY-ANALYSIS-*.md (primary source):**
- Property address
- Property type (SFR, condo, multi-family, etc.)
- Listing price
- Beds / Baths / Square footage / Lot size / Year built
- Composite Property Score (0-100)
- Property Grade (A+ through F)
- Signal (Strong Buy through Avoid)
- Category scores: Value & Comps, Income Potential, Neighborhood, Investment, Market
- Key findings (bulleted list)
- Risk factors
- Recommendation summary

**From PROPERTY-COMPS-*.md:**
- Comparable sales list (address, price, sqft, beds/baths, distance, sale date)
- Estimated market value
- Price per square foot vs comps
- Over/under priced assessment

**From PROPERTY-RENTAL-*.md:**
- Estimated monthly rent
- Net monthly cash flow
- Cap rate
- Cash-on-cash return
- Gross rent multiplier
- Expense breakdown
- Vacancy assumption

**From PROPERTY-NEIGHBORHOOD-*.md:**
- School ratings (elementary, middle, high)
- Walk Score / Transit Score / Bike Score
- Safety rating
- Demographics summary
- Growth outlook

**From PROPERTY-INVEST-*.md:**
- Best investment strategy
- Projected ROI (1yr, 3yr, 5yr)
- Risk level
- Value-add opportunity description
- Exit strategy options

**From PROPERTY-MARKET-*.md:**
- Market type (buyer/seller/balanced)
- Median home price
- Days on market (average)
- Inventory months
- Price trend (YoY)
- Economic drivers

### STEP 4: BUILD THE JSON DATA STRUCTURE

Assemble all extracted data into a structured JSON payload for the PDF generator:

```json
{
  "property_address": "123 Main Street, City, ST 12345",
  "report_date": "April 29, 2026",
  "property_type": "Single Family Residence",
  "listing_price": 425000,
  "beds": 3,
  "baths": 2,
  "sqft": 1850,
  "lot_size": "7,200 sf",
  "year_built": 2005,
  "property_score": 76,
  "grade": "A",
  "signal": "Buy",
  "categories": {
    "Value & Comps": {
      "score": 78,
      "weight": "25%"
    },
    "Income Potential": {
      "score": 72,
      "weight": "20%"
    },
    "Neighborhood Quality": {
      "score": 80,
      "weight": "20%"
    },
    "Investment Upside": {
      "score": 74,
      "weight": "20%"
    },
    "Market Conditions": {
      "score": 70,
      "weight": "15%"
    }
  },
  "comparable_sales": [
    {
      "address": "125 Oak Ave",
      "price": 430000,
      "sqft": 1900,
      "beds": 3,
      "baths": 2,
      "distance": "0.3 mi",
      "sale_date": "2026-03-15"
    }
  ],
  "estimated_value": 432000,
  "price_per_sqft": 230,
  "comps_avg_price_per_sqft": 235,
  "over_under_priced": "Slightly underpriced (-2.1%)",
  "estimated_rent": 2650,
  "net_cash_flow": 320,
  "cap_rate": 7.2,
  "cash_on_cash": 9.8,
  "gross_rent_multiplier": 13.4,
  "vacancy_rate": 5.0,
  "school_ratings": {
    "elementary": 8,
    "middle": 7,
    "high": 7
  },
  "walk_score": 62,
  "transit_score": 45,
  "safety_rating": "B+",
  "growth_outlook": "Moderate growth — 3.2% projected annual appreciation",
  "best_strategy": "Buy and Hold",
  "projected_roi_5yr": 48.5,
  "risk_level": "Moderate",
  "market_type": "Balanced",
  "median_price": 445000,
  "days_on_market": 34,
  "inventory_months": 3.2,
  "price_trend_yoy": 4.8,
  "key_findings": [
    "Priced 2.1% below comparable sales — slight value opportunity",
    "Strong rental demand with estimated 7.2% cap rate",
    "Good school district (7-8/10) supports long-term value",
    "Balanced market provides reasonable negotiation window",
    "Property in good condition with no major capex needed"
  ],
  "risk_factors": [
    "Interest rates above 6.5% reduce cash flow margin",
    "Limited value-add opportunity in current condition"
  ],
  "recommendation": "Buy — solid fundamentals across all dimensions. Strong rental yield at 7.2% cap rate with good neighborhood quality. Recommended strategy is buy-and-hold with projected 48.5% total ROI over 5 years.",
  "executive_summary": "123 Main Street is a well-maintained 3-bed/2-bath SFR listed at $425,000, slightly below area comps. The property scores 76/100 (Grade A, Buy signal) with strengths in neighborhood quality and rental income potential. Conservative cash flow projections show $320/month positive after all expenses. Recommended as a buy-and-hold investment with moderate risk."
}
```

### STEP 5: GENERATE THE PDF

Run the PDF generation script:

```bash
python3 ~/.claude/skills/realestate/scripts/generate_realestate_pdf.py
```

**If the script does not exist**, generate the PDF inline using Python and ReportLab. The inline script must produce a PDF with the following sections:

#### PDF SECTIONS AND LAYOUT

**Page 1: Cover Page**
- Report title: "Property Analysis Report"
- Property address (large, centered)
- Property Score gauge (circular, color-coded: green 70+, yellow 40-69, red 0-39)
- Grade and Signal displayed prominently
- Report date
- Disclaimer footer

**Page 2: Property Overview**
- Property details table (price, beds, baths, sqft, lot, year, type)
- Property photo placeholder or description
- Executive summary (2-4 sentences)
- Key findings list (bulleted, top 5)

**Page 3: Comparable Sales Analysis**
- Comp table: address, price, $/sqft, beds/baths, distance, sale date
- Estimated value vs listing price
- Price per sqft comparison bar chart
- Over/under priced assessment with percentage

**Page 4: Cash Flow Projections**
- Rental income estimate
- Monthly expense breakdown table (mortgage, taxes, insurance, vacancy, maintenance, management)
- Net monthly cash flow (highlighted, green if positive, red if negative)
- Key return metrics: Cap Rate, Cash-on-Cash, GRM
- 5-year cash flow projection table

**Page 5: Neighborhood Scorecard**
- School ratings (elementary, middle, high) with bar visualization
- Walk Score / Transit Score / Bike Score gauges
- Safety rating
- Demographics summary
- Growth outlook
- Amenities nearby

**Page 6: Investment Analysis**
- Category scores bar chart (all 5 categories)
- Best strategy recommendation
- Projected ROI table (1yr, 3yr, 5yr)
- Risk level assessment
- Value-add opportunity description
- Exit strategy options

**Page 7: Market Conditions**
- Market type indicator (buyer/seller/balanced)
- Median price and trend
- Days on market and inventory
- Economic drivers
- Price trend chart or table
- Supply/demand assessment

**Page 8: Recommendation & Next Steps**
- Overall recommendation (highlighted)
- Signal with explanation
- Key action items
- Suggested next steps
- Full disclaimer

#### PDF STYLING

| Element | Style |
|---------|-------|
| Colors | Navy (#1B2A4A) headers, dark gray (#333) body, green (#2E7D32) positive, red (#C62828) negative |
| Fonts | Helvetica-Bold for headers, Helvetica for body |
| Score gauges | Circular arc gauges with color gradient (red -> yellow -> green) |
| Tables | Alternating row colors (white/#F5F5F5), navy header row |
| Charts | Horizontal bar charts for category scores and comparisons |
| Footer | Page numbers, disclaimer, generation date |
| Margins | 50pt top, 40pt sides, 50pt bottom |

### STEP 6: VERIFY AND DELIVER

After PDF generation:

```bash
ls -la PROPERTY-REPORT.pdf
```

Confirm the file was created and report:
- File name and location
- File size
- Number of pages
- Which data sources were included (list the PROPERTY-*.md files used)
- Any data gaps (sections that had no source file — these will show "Data not available" in the PDF)

---

## OUTPUT SPECIFICATIONS

| Spec | Value |
|------|-------|
| File name | `PROPERTY-REPORT.pdf` (or `PROPERTY-REPORT-[ADDRESS].pdf` if address specified) |
| Page size | Letter (8.5" x 11") |
| Orientation | Portrait |
| Pages | 6-10 depending on available data |
| File size | Typically 200KB - 1MB |
| Python dependency | ReportLab (`pip install reportlab` if not installed) |

---

## RULES

1. **Professional quality** — The PDF must look like it came from a real estate analytics firm, not a quick printout
2. **Data-driven** — Every number in the PDF must come from the analysis files or live research; never fabricate data
3. **Conservative estimates** — Use the same conservative projections from the analysis files
4. **Complete disclaimer** — Full disclaimer must appear on the cover page and the last page
5. **Graceful degradation** — If some analysis files are missing, generate the PDF with available data and mark missing sections as "Not analyzed — run /realestate [command] to add this data"
6. **Install dependencies** — If ReportLab is not installed, install it automatically: `pip install reportlab`
7. **Overwrite safely** — If PROPERTY-REPORT.pdf already exists, overwrite it (the latest data wins)
8. **Color-coded scores** — All scores must be color-coded: green (70+), yellow (40-69), red (0-39)

## ERROR HANDLING

- If ReportLab is not installed, run `pip install reportlab` and retry
- If no PROPERTY-*.md files exist, prompt the user to run `/realestate analyze <address>` first
- If the Python script fails, capture the error message and display it to the user with troubleshooting steps
- If only partial data is available, generate a partial report and clearly mark which sections are incomplete
- If the PDF file cannot be written (permission error), suggest an alternative output directory

## DEPENDENCY INSTALLATION

If ReportLab is not available, install it:

```bash
pip install reportlab 2>/dev/null || pip3 install reportlab 2>/dev/null
```

If installation fails, provide manual instructions:
```
To install the PDF generation dependency:
  pip install reportlab
  
If using a virtual environment:
  python3 -m venv venv && source venv/bin/activate && pip install reportlab
```

---

## WHEN TO RECOMMEND PDF vs MARKDOWN

| Situation | Recommend |
|-----------|-----------|
| Client presentation or email attachment | PDF |
| Lender or partner due diligence package | PDF |
| Quick internal reference | Markdown |
| Iterative editing and analysis | Markdown |
| Board or investor meeting | PDF |
| Personal property shopping | Markdown |
| Sales collateral for real estate agent | PDF |

Always suggest: "Your analysis files are saved as Markdown for easy reference. Run `/realestate report-pdf` anytime to generate a polished PDF version for clients or presentations."

---

## DATA QUALITY FLAGS

When compiling the PDF, flag data quality issues:

| Flag | Condition | Display In PDF |
|------|-----------|---------------|
| High Confidence | All 5 analysis agents ran, data is fresh | Green checkmark |
| Moderate Confidence | 3-4 agents ran, or data is 7+ days old | Yellow warning |
| Low Confidence | Only 1-2 agents ran, or significant data gaps | Red flag with note |
| Stale Data | Analysis files are 30+ days old | Warning banner: "Data may be outdated" |

---

## MULTI-PROPERTY REPORTS

If the user has analyzed multiple properties (multiple sets of PROPERTY-*.md files), the PDF should:

1. Detect all unique properties from file names
2. Ask the user which property to include (or all)
3. If "all", create a multi-property report with a comparison summary page
4. Each property gets its own section with the standard layout
5. Final page includes a side-by-side comparison table if 2+ properties are included

**DISCLAIMER: For educational/research purposes only. Not financial or investment advice. All estimates are AI-generated approximations based on publicly available data. Always verify with licensed professionals and conduct your own due diligence before making any purchase or investment decisions.**
