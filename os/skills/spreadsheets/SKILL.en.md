# Spreadsheets Skill

Framework for creating Excel files. Used by CFO, PM, Sales.

## Available Spreadsheet Types

### 1. Financial Model / P&L — Owner: CFO
- Tabs: Assumptions, Monthly P&L, Annual Summary, Unit Economics, Scenarios
- Color coding: blue = input, black = formula, green = cross-sheet reference
- All assumptions in dedicated cells, never hardcoded in formulas

### 2. Pricing Calculator — Owner: CFO + Sales
- Tabs: Pricing Tiers, Quote Builder, Competitor Comparison, Discount Matrix
- Formulas for automatic calculation based on: users, tier, contract duration, add-ons
- Discounts applied automatically with validation (max 20% without approval)

### 3. KPI Dashboard — Owner: CFO + CEO
- Tabs: Monthly Metrics, Charts, Funnel Analysis, Cohort Analysis
- Built-in charts for trend visualization
- Formulas for automatic calculations: m/m growth rate, churn, NRR, LTV/CAC

## How to generate the Excel files

To generate a real `.xlsx` file, ask Claude Code:
"Generate an Excel file for [type] following the framework in `os/skills/spreadsheets/SKILL.md`"

Claude Code can generate real Excel files with formulas, formatting, and charts.

## Excel Best Practices

### Structure
- First tab = "Instructions" or "Summary" with an overview
- Assumptions separated from calculations
- One tab per logical concept
- Flow left-to-right, top-to-bottom

### Formulas
- Zero errors: no #REF!, #DIV/0!, #VALUE!, #N/A
- Use IFERROR to guard against divisions by zero
- Assumption cells in blue, formulas in black
- Never hardcoded: every editable number lives in a dedicated cell

### Formatting
- Consistent font (Arial)
- Headers with colored background
- Formatted numbers: currency with €, percentages with %, thousands separator
- Negatives in parentheses: (1.234) not -1.234
- Light borders for readability
