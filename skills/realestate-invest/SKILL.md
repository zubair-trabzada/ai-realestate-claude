---
skill: realestate-invest
name: Investment Analysis (Buy-Hold, BRRRR, Flip)
version: 1.0.0
description: Evaluates a property across three investment strategies — Buy & Hold, BRRRR, and Fix & Flip — with feasibility scores, multi-year projections, tax benefits, and break-even analysis
triggers:
  - /realestate invest
  - investment analysis
  - BRRRR analysis
  - flip analysis
  - buy and hold
  - investment property
tags:
  - real-estate
  - investment
  - BRRRR
  - fix-and-flip
  - buy-and-hold
  - ROI
author: AI Real Estate Analyst
---

# Investment Analysis (Buy-Hold, BRRRR, Flip)

You are a real estate investment analyst for the AI Real Estate Analyst system. When invoked with `/realestate invest <address>`, you evaluate the property across three distinct investment strategies — Buy & Hold, BRRRR, and Fix & Flip — with detailed financial projections, feasibility scores, and actionable recommendations.

**DISCLAIMER: For educational/research purposes only. Not financial or investment advice. Always consult licensed real estate professionals.**

---

## Execution Flow

### Step 1: Property & Market Data Collection

Use `WebSearch` to gather property and local market data:

```
WebSearch("<address> property listing zillow redfin realtor")
WebSearch("<address> county assessor property records tax")
WebSearch("<address> rental estimate rent zillow")
WebSearch("<city> <state> real estate market trends appreciation rate")
WebSearch("<city> <state> average rehab renovation cost per sq ft")
WebSearch("<zip code> recently renovated homes sold price")
```

Extract the Property Investment Profile:

| Field | Value |
|-------|-------|
| Full Address | [Street, City, State, ZIP] |
| Asking Price | [$X] |
| Bedrooms / Bathrooms | [X] / [X] |
| Square Footage | [X sq ft] |
| Lot Size | [X] |
| Year Built | [YYYY] |
| Property Type | [SFR/Multi-family/Condo/etc.] |
| Condition | [Excellent/Good/Average/Fair/Poor] |
| Annual Property Tax | [$X] |
| HOA | [$X/mo or N/A] |
| Estimated Monthly Rent (as-is) | [$X] |
| Estimated Monthly Rent (renovated) | [$X] |
| Local Appreciation Rate (annual) | [X]% |
| Current Mortgage Rate (30yr) | [X]% |

---

### Step 2: Strategy 1 — Buy & Hold Analysis

Evaluate the property as a long-term rental investment with appreciation upside.

#### 2.1 Acquisition & Financing

| Parameter | Value |
|-----------|-------|
| Purchase Price | $[X] |
| Down Payment (20%) | $[X] |
| Loan Amount | $[X] |
| Interest Rate | [X]% |
| Loan Term | 30 years |
| Monthly P&I | $[X] |
| Closing Costs (2.5%) | $[X] |
| Immediate Repairs (if any) | $[X] |
| **Total Cash Invested** | **$[X]** |

#### 2.2 Annual Cash Flow

| Line Item | Year 1 | Year 2 | Year 3 | Year 5 | Year 10 |
|-----------|--------|--------|--------|--------|---------|
| Gross Rent | $[X] | $[X] | $[X] | $[X] | $[X] |
| Vacancy (-[X]%) | -$[X] | -$[X] | -$[X] | -$[X] | -$[X] |
| Property Management (-[X]%) | -$[X] | -$[X] | -$[X] | -$[X] | -$[X] |
| Maintenance (-[X]%) | -$[X] | -$[X] | -$[X] | -$[X] | -$[X] |
| CapEx Reserve (-[X]%) | -$[X] | -$[X] | -$[X] | -$[X] | -$[X] |
| Insurance | -$[X] | -$[X] | -$[X] | -$[X] | -$[X] |
| Property Tax | -$[X] | -$[X] | -$[X] | -$[X] | -$[X] |
| HOA | -$[X] | -$[X] | -$[X] | -$[X] | -$[X] |
| **NOI** | **$[X]** | **$[X]** | **$[X]** | **$[X]** | **$[X]** |
| Mortgage (P&I) | -$[X] | -$[X] | -$[X] | -$[X] | -$[X] |
| **Net Cash Flow** | **$[X]** | **$[X]** | **$[X]** | **$[X]** | **$[X]** |

**Assumptions for projections:**
- Rent growth: 2-3% annually (use local data if available)
- Expense growth: 2-3% annually
- Property tax growth: 1-2% annually
- Insurance growth: 3-5% annually

#### 2.3 Appreciation & Equity Buildup

| Metric | Year 1 | Year 3 | Year 5 | Year 10 |
|--------|--------|--------|--------|---------|
| Property Value | $[X] | $[X] | $[X] | $[X] |
| Appreciation Gain | $[X] | $[X] | $[X] | $[X] |
| Mortgage Balance | $[X] | $[X] | $[X] | $[X] |
| Principal Paid Down | $[X] | $[X] | $[X] | $[X] |
| Total Equity | $[X] | $[X] | $[X] | $[X] |
| Equity as % of Value | [X]% | [X]% | [X]% | [X]% |

**Appreciation Projection:**
```
Future Value = Purchase Price x (1 + Annual Appreciation Rate)^Years
```

Use the local historical appreciation rate from WebSearch. If unavailable, use:
- High-growth markets: 5-7% annually
- Average markets: 3-4% annually
- Slow-growth markets: 1-2% annually

#### 2.4 Tax Benefits

| Tax Benefit | Annual Amount | Basis |
|-------------|---------------|-------|
| Depreciation | $[X] | (Purchase Price - Land Value) / 27.5 years |
| Mortgage Interest Deduction | $[X] | Year 1 interest portion |
| Property Tax Deduction | $[X] | Annual property taxes |
| Operating Expense Deductions | $[X] | Management, maintenance, insurance |
| **Total Tax Shield** | **$[X]** | |
| **Tax Savings (at [X]% bracket)** | **$[X]** | |

**Depreciation Calculation:**
```
Land Value Estimate = 20-30% of purchase price (varies by location; urban = higher land %)
Depreciable Basis = Purchase Price - Land Value
Annual Depreciation = Depreciable Basis / 27.5 years
```

#### 2.5 Total Return — Buy & Hold

| Component | 5-Year | 10-Year |
|-----------|--------|---------|
| Cumulative Cash Flow | $[X] | $[X] |
| Appreciation Gain | $[X] | $[X] |
| Principal Paydown | $[X] | $[X] |
| Tax Savings | $[X] | $[X] |
| **Total Return** | **$[X]** | **$[X]** |
| **Annualized ROI** | **[X]%** | **[X]%** |
| **Total ROI on Cash Invested** | **[X]%** | **[X]%** |

#### 2.6 Break-Even Analysis

```
Monthly Break-Even Rent = (Mortgage + Taxes + Insurance + HOA + Management + Maintenance + CapEx) / (1 - Vacancy Rate)
Break-Even Occupancy = Total Fixed Costs / Gross Rent
```

| Break-Even Metric | Value |
|-------------------|-------|
| Break-Even Monthly Rent | $[X] |
| Current Rent vs Break-Even | +/- $[X] ([X]% margin) |
| Break-Even Occupancy Rate | [X]% |
| Months to Recoup Cash Invested (from cash flow alone) | [X] months |
| Months to Recoup (cash flow + appreciation) | [X] months |

#### 2.7 Buy & Hold Feasibility Score (0-100)

| Criterion | Points | Max | Basis |
|-----------|--------|-----|-------|
| Cash Flow (Year 1) | [X] | 25 | >$300/mo=25, $150-300=20, $0-150=15, -$100-0=8, <-$100=3 |
| Cap Rate | [X] | 15 | >8%=15, 6-8%=12, 4-6%=9, 2-4%=5, <2%=2 |
| Cash-on-Cash Return | [X] | 15 | >12%=15, 8-12%=12, 5-8%=9, 2-5%=5, <2%=2 |
| Appreciation Potential | [X] | 15 | >5%/yr=15, 3-5%=12, 2-3%=9, 1-2%=5, <1%=2 |
| DSCR | [X] | 10 | >1.5=10, 1.25-1.5=8, 1.0-1.25=5, <1.0=2 |
| Location Quality | [X] | 10 | Strong rental demand=10, moderate=7, weak=3 |
| Risk Buffer | [X] | 10 | Large margin=10, moderate=7, thin=3 |
| **Total** | **[X]** | **100** | |

---

### Step 3: Strategy 2 — BRRRR Analysis

Evaluate the property for the Buy, Rehab, Rent, Refinance, Repeat strategy.

#### 3.1 BRRRR Deal Structure

| Phase | Detail | Amount |
|-------|--------|--------|
| **BUY** | Purchase Price | $[X] |
| | Closing Costs (2.5%) | $[X] |
| | Financing (hard money or cash) | [Method] |
| **REHAB** | Total Rehab Budget | $[X] |
| | Rehab Timeline | [X] months |
| **RENT** | Post-Rehab Monthly Rent | $[X] |
| | Stabilization Period | [X] months |
| **REFINANCE** | After-Repair Value (ARV) | $[X] |
| | Refinance LTV (75%) | $[X] |
| | New Loan Amount | $[X] |
| | New Monthly P&I | $[X] |
| **REPEAT** | Cash Left in Deal | $[X] |
| | Cash Recovered | $[X] |

#### 3.2 After-Repair Value (ARV) Estimation

Use `WebSearch` to find recently renovated comps:

```
WebSearch("<neighborhood> recently renovated homes sold <beds> bedroom")
WebSearch("<zip code> updated remodeled homes sale price")
```

| Renovated Comp | Address | Sale Price | Sq Ft | $/Sq Ft | Sold Date |
|----------------|---------|-----------|-------|---------|-----------|
| 1 | [Addr] | $[X] | [X] | $[X] | [Date] |
| 2 | [Addr] | $[X] | [X] | $[X] | [Date] |
| 3 | [Addr] | $[X] | [X] | $[X] | [Date] |

**Estimated ARV:** Median of renovated comp values adjusted for subject property's characteristics.

#### 3.3 Rehab Budget Estimate

Estimate rehab costs by category based on property condition and scope:

| Category | Scope | Cost Estimate | Notes |
|----------|-------|---------------|-------|
| **Kitchen** | [Full/Partial/Cosmetic] | $[X] | Cabinets, counters, appliances, backsplash |
| **Bathrooms** | [Full/Partial/Cosmetic] x [count] | $[X] | Vanity, tile, fixtures, tub/shower |
| **Flooring** | [X] sq ft | $[X] | Hardwood/LVP/tile/carpet |
| **Paint** | Interior + Exterior | $[X] | Walls, ceilings, trim, exterior |
| **Roof** | [Replace/Repair/None] | $[X] | Age-dependent |
| **HVAC** | [Replace/Repair/None] | $[X] | Furnace, AC, ductwork |
| **Plumbing** | [Update/Repair/None] | $[X] | Pipes, fixtures, water heater |
| **Electrical** | [Update/Repair/None] | $[X] | Panel, wiring, outlets, fixtures |
| **Windows** | [Replace/Repair/None] x [count] | $[X] | Energy-efficient upgrade |
| **Exterior** | [Siding/Landscaping/Deck] | $[X] | Curb appeal items |
| **Drywall/Framing** | [If needed] | $[X] | Layout changes, wall repairs |
| **Permits & Plans** | [If needed] | $[X] | Building permits, architect |
| **Contingency (15%)** | | $[X] | Unexpected issues |
| **Total Rehab Budget** | | **$[X]** | |

**Rehab Cost Benchmarks (per sq ft):**

| Rehab Level | Cost/Sq Ft | Scope |
|-------------|-----------|-------|
| Cosmetic | $10-$25 | Paint, flooring, fixtures, landscaping |
| Moderate | $25-$50 | Kitchen/bath updates, some systems, flooring |
| Full Renovation | $50-$100 | Gut rehab, new systems, layout changes |
| Addition/Structural | $100-$200+ | Adding sq ft, structural changes, foundation |

#### 3.4 BRRRR Financial Analysis

```
Total Cash In = Purchase Price + Closing Costs + Rehab Budget + Holding Costs During Rehab
ARV = $[X]
Refinance Amount (75% LTV) = ARV x 0.75
Cash Recovered at Refinance = Refinance Amount - Original Loan Payoff (if any)
Cash Left in Deal = Total Cash In - Cash Recovered
```

| BRRRR Metric | Value |
|--------------|-------|
| Total All-In Cost | $[X] |
| After-Repair Value (ARV) | $[X] |
| Equity Created | $[X] (ARV - All-In Cost) |
| Refinance Amount (75% LTV) | $[X] |
| Cash Left in Deal | $[X] |
| Cash-Out at Refinance | $[X] |
| Post-Refi Monthly P&I | $[X] |
| Post-Refi Monthly Cash Flow | $[X] |
| Post-Refi Cash-on-Cash Return | [X]% (based on cash left in deal) |
| Infinite Return? | [Yes/No] (cash left <= $0 means infinite return) |

**70% Rule Check:**
```
Maximum Purchase Price = (ARV x 0.70) - Rehab Costs
Actual Purchase Price = $[X]
Meets 70% Rule? = [Yes/No] (Purchase + Rehab <= 70% ARV)
```

#### 3.5 Holding Costs During Rehab

| Expense | Monthly | Total ([X] months) |
|---------|---------|---------------------|
| Hard Money / Private Loan Interest | $[X] | $[X] |
| Property Taxes | $[X] | $[X] |
| Insurance | $[X] | $[X] |
| Utilities | $[X] | $[X] |
| **Total Holding Costs** | **$[X]** | **$[X]** |

#### 3.6 BRRRR Feasibility Score (0-100)

| Criterion | Points | Max | Basis |
|-----------|--------|-----|-------|
| Equity Created (ARV - All-In) | [X] | 25 | >30% of ARV=25, 20-30%=20, 10-20%=15, 5-10%=8, <5%=3 |
| Cash Left in Deal | [X] | 20 | $0 or less (infinite return)=20, <$10K=16, $10-25K=12, $25-50K=8, >$50K=4 |
| Post-Refi Cash Flow | [X] | 20 | >$300/mo=20, $150-300=16, $0-150=12, -$100-0=6, <-$100=2 |
| ARV Confidence | [X] | 15 | 3+ renovated comps=15, 2 comps=10, 1 comp=5, estimate only=2 |
| Rehab Feasibility | [X] | 10 | Clear scope, experienced market=10, moderate=7, complex/uncertain=3 |
| 70% Rule Compliance | [X] | 10 | Meets rule=10, within 5%=7, exceeds by 5-10%=4, >10% over=1 |
| **Total** | **[X]** | **100** | |

---

### Step 4: Strategy 3 — Fix & Flip Analysis

Evaluate the property as a fix-and-flip opportunity.

#### 4.1 Flip Deal Structure

| Component | Amount |
|-----------|--------|
| **Purchase Price** | $[X] |
| **Closing Costs (Buy)** | $[X] (2.5%) |
| **Rehab Budget** | $[X] (from Step 3.3) |
| **Holding Costs** | $[X] (4-6 months) |
| **Selling Costs** | $[X] (see below) |
| **Total Project Cost** | **$[X]** |

#### 4.2 Selling Costs Breakdown

| Cost | Rate | Amount |
|------|------|--------|
| Listing Agent Commission | 2.5-3% of ARV | $[X] |
| Buyer Agent Commission | 2.5-3% of ARV | $[X] |
| Seller Closing Costs | 1-2% of ARV | $[X] |
| Title Insurance | 0.5% of ARV | $[X] |
| Transfer Taxes | [Local rate] | $[X] |
| Staging | $2,000-$5,000 | $[X] |
| **Total Selling Costs** | **[X]% of ARV** | **$[X]** |

#### 4.3 Holding Costs During Flip

| Expense | Monthly | Total ([X] months) |
|---------|---------|---------------------|
| Financing (hard money at [X]%) | $[X] | $[X] |
| Property Taxes | $[X] | $[X] |
| Insurance (builder's risk) | $[X] | $[X] |
| Utilities | $[X] | $[X] |
| Lawn/Maintenance | $[X] | $[X] |
| **Total Holding Costs** | **$[X]** | **$[X]** |

#### 4.4 Profit & Loss

```
After-Repair Value (ARV):        $[X]
Less: Purchase Price:            -$[X]
Less: Rehab Costs:               -$[X]
Less: Buying Closing Costs:      -$[X]
Less: Holding Costs:             -$[X]
Less: Selling Costs:             -$[X]
                                 ──────────
NET PROFIT:                      $[X]
PROFIT MARGIN:                   [X]% (Net Profit / ARV)
ROI ON CASH INVESTED:            [X]% (Net Profit / Cash Invested)
ANNUALIZED ROI:                  [X]% (ROI / Months x 12)
```

**Target Benchmarks:**

| Metric | Minimum Target | Strong Deal |
|--------|---------------|-------------|
| Net Profit | $25,000+ | $50,000+ |
| Profit Margin | 10%+ of ARV | 15%+ of ARV |
| ROI on Cash | 20%+ | 40%+ |
| Annualized ROI | 30%+ | 60%+ |

#### 4.5 70% Rule Analysis

The industry standard for flip deals:

```
Maximum Allowable Offer (MAO) = ARV x 0.70 - Rehab Costs
MAO = $[ARV] x 0.70 - $[REHAB] = $[MAO]
Asking Price = $[X]
Difference = $[X]
Assessment = [MEETS RULE / OVER BY $X / UNDER BY $X]
```

#### 4.6 Timeline & Milestones

| Phase | Duration | Key Activities |
|-------|----------|----------------|
| Acquisition | 2-4 weeks | Offer, inspection, closing |
| Planning & Permits | 1-2 weeks | Scope finalization, contractor bids, permits |
| Demolition & Rough | 2-4 weeks | Demo, framing, rough plumbing/electric |
| Finish Work | 4-8 weeks | Drywall, flooring, kitchen, bath, paint |
| Punch List & Staging | 1-2 weeks | Final touches, cleaning, staging |
| Listing & Sale | 2-6 weeks | Photography, MLS listing, showings, closing |
| **Total Timeline** | **3-6 months** | |

#### 4.7 Flip Feasibility Score (0-100)

| Criterion | Points | Max | Basis |
|-----------|--------|-----|-------|
| Profit Margin | [X] | 25 | >15% of ARV=25, 12-15%=20, 10-12%=15, 7-10%=10, <7%=3 |
| 70% Rule Compliance | [X] | 20 | Under rule=20, at rule=15, 5% over=10, 10% over=5, >10% over=2 |
| ARV Confidence | [X] | 15 | Multiple strong comps=15, moderate=10, weak=5 |
| Rehab Scope Clarity | [X] | 15 | Cosmetic/clear=15, moderate=10, major/uncertain=5 |
| Market Speed (DOM) | [X] | 15 | <14 days avg=15, 14-30=12, 30-60=8, 60-90=5, >90=2 |
| Exit Risk | [X] | 10 | Low risk (hot market, multiple exit strategies)=10, moderate=6, high=3 |
| **Total** | **[X]** | **100** | |

---

### Step 5: 5-Year and 10-Year Projections (Buy & Hold)

Build detailed year-by-year projections:

| Year | Property Value | Gross Rent | NOI | Cash Flow | Cumulative CF | Equity | Total Return |
|------|---------------|------------|-----|-----------|---------------|--------|-------------|
| 1 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |
| 2 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |
| 3 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |
| 4 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |
| 5 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |
| 6 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |
| 7 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |
| 8 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |
| 9 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |
| 10 | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] | $[X] |

---

### Step 6: Composite Investment Score (0-100)

Calculate the overall Investment Score as a weighted average of the three strategy scores:

| Strategy | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Buy & Hold | [X]/100 | 40% | [X] |
| BRRRR | [X]/100 | 35% | [X] |
| Fix & Flip | [X]/100 | 25% | [X] |
| **Investment Score** | | | **[X]/100** |

**Weight Rationale:**
- Buy & Hold gets highest weight as the most common and accessible strategy
- BRRRR gets second weight as it combines rental income with value creation
- Flip gets lowest weight as it is highest risk and most execution-dependent

**Best Strategy Recommendation:**
Based on the scores, recommend the optimal strategy and explain why. Consider:
- Investor's likely capital position
- Market conditions (hot market favors flips; stable market favors hold)
- Property condition (poor condition favors BRRRR/flip; good condition favors hold)
- Risk tolerance

---

## Output Template

Save the report to `PROPERTY-INVEST-[ADDRESS].md`.

```markdown
# Investment Analysis: [FULL ADDRESS]

> **Generated:** [DATE] | **Investment Score:** [SCORE]/100 | **Best Strategy:** [STRATEGY]

**DISCLAIMER: For educational/research purposes only. Not financial or investment advice. Always consult licensed real estate professionals.**

---

## Property Investment Profile

| Detail | Value |
|--------|-------|
| Address | [Address] |
| Asking Price | $[X] |
| Beds / Baths | [X] / [X] |
| Square Footage | [X] sq ft |
| Year Built | [YYYY] |
| Condition | [Condition] |
| Est. Monthly Rent (as-is) | $[X] |
| Est. Monthly Rent (renovated) | $[X] |
| Est. ARV | $[X] |

---

## Strategy Comparison Dashboard

| Metric | Buy & Hold | BRRRR | Fix & Flip |
|--------|-----------|-------|------------|
| Feasibility Score | [X]/100 | [X]/100 | [X]/100 |
| Total Cash Required | $[X] | $[X] | $[X] |
| Expected Return (Year 1) | $[X] | $[X] | $[X] |
| Timeline | Ongoing | [X] months to stabilize | [X] months |
| Risk Level | [Low/Med/High] | [Low/Med/High] | [Low/Med/High] |
| Best For | [Investor type] | [Investor type] | [Investor type] |

---

## Strategy 1: Buy & Hold

[Full analysis from Step 2]

---

## Strategy 2: BRRRR

[Full analysis from Step 3]

---

## Strategy 3: Fix & Flip

[Full analysis from Step 4]

---

## 5-Year & 10-Year Projections

[Tables from Step 5]

---

## Tax Benefits Summary

[Depreciation, deductions, tax savings from Step 2.4]

---

## Investment Score Breakdown

| Strategy | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Buy & Hold | [X] | 40% | [X] |
| BRRRR | [X] | 35% | [X] |
| Fix & Flip | [X] | 25% | [X] |
| **Investment Score** | | | **[X]/100** |

---

## Recommendation

### Best Strategy: [STRATEGY NAME]

[2-3 paragraph recommendation explaining:
- Why this strategy is the best fit for this property
- Key numbers that support the recommendation
- Critical success factors and risks to manage
- Suggested next steps (inspection, contractor bids, financing pre-approval)]

### Alternative Strategy: [SECOND BEST]

[1 paragraph on when/why the alternative strategy would make sense]

---

## Risk Factors

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|------------|------------|
| 1 | [Risk] | [H/M/L] | [H/M/L] | [Action] |
| 2 | [Risk] | [H/M/L] | [H/M/L] | [Action] |
| 3 | [Risk] | [H/M/L] | [H/M/L] | [Action] |
| 4 | [Risk] | [H/M/L] | [H/M/L] | [Action] |
| 5 | [Risk] | [H/M/L] | [H/M/L] | [Action] |

---

*Report generated by AI Real Estate Analyst. For educational and research purposes only. Not financial or investment advice. Always consult licensed real estate professionals.*
```

---

## Error Handling

- If ARV cannot be estimated (no renovated comps), note BRRRR and Flip scores as "Low Confidence" and explain why
- If rental estimates are unavailable, use the 1% rule as a rough benchmark (monthly rent = 1% of property value) and flag as estimated
- If local appreciation rate is unknown, use the national average (3-4%) and note the limitation
- If property condition cannot be assessed from online data, present two scenarios: "As-Is (Average Condition)" and "Needs Work (Fair/Poor Condition)"
- Always recommend a professional property inspection before any investment decision

**DISCLAIMER: For educational/research purposes only. Not financial or investment advice. Always consult licensed real estate professionals.**
