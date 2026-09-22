# The Degree Dividend

### An interactive analysis of early-career earnings, student debt, and financial value across the 50 most commonly awarded U.S. bachelor's degree fields

[![Open the Streamlit app](https://img.shields.io/badge/Live_App-Open_in_Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://degreeroi.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

<!-- After adding the screenshot to assets/dashboard-overview.png, uncomment this line:
![The Degree Dividend dashboard](assets/dashboard-overview.png)
-->

## Overview

The Degree Dividend explores a practical question: **How do popular college majors compare on early-career financial outcomes?**

The project combines U.S. degree-completion data with program-level earnings and debt data to evaluate the 50 most frequently conferred bachelor's degree fields. The accompanying Streamlit dashboard allows users to compare majors using several measures or build a personalized value ranking by changing the importance assigned to earnings, debt burden, and wage growth.

> **[Explore the live dashboard](https://degreeroi.streamlit.app/)**

## What the Dashboard Does

- Ranks the 50 most commonly conferred bachelor's degree fields by seven criteria
- Compares median earnings four years after completion with typical student debt
- Measures earnings growth from one to four years after completion
- Shows each field's earnings premium relative to the median across bachelor's programs
- Includes a 25th-percentile earnings measure to represent downside risk
- Lets users create a custom value score by weighting earnings, low debt burden, and wage growth
- Visualizes the relationship among debt, earnings, and annual degree volume in an interactive bubble chart

## Key Findings

Based on the processed dataset included in this repository:

- **Computer Engineering** has the highest four-year median earnings ($105,640), the lowest debt-to-earnings ratio (0.218), and the highest earnings premium (70.1%) among the 50 fields analyzed.
- **Communication Disorders Sciences and Services** shows the largest increase from first- to fourth-year earnings (137.1%).
- **Registered Nursing and related nursing fields** represent the largest field by annual conferrals (162,729) while also producing four-year median earnings of $86,383.
- With the dashboard's default weights—40% earnings, 35% low debt burden, and 25% wage growth—**Computer Engineering** receives the highest composite value score.

These results describe aggregated early-career outcomes, not the experience of every graduate. Institution, location, occupation, graduate education, labor-market conditions, and individual circumstances can all affect outcomes.

## Data Sources

| Source | Role in the analysis |
| --- | --- |
| [IPEDS Completions Survey (2022)](https://nces.ed.gov/ipeds/use-the-data/annual-survey-forms-packages-archived/2022) | Identifies bachelor's degree fields and total conferrals across U.S. institutions |
| [College Scorecard Field-of-Study Data](https://collegescorecard.ed.gov/data/) | Supplies program-level student debt and earnings measures |
| [NCES Classification of Instructional Programs](https://nces.ed.gov/ipeds/cipcode/) | Provides standardized four-digit CIP codes and field titles |

The analysis uses the versions of these sources processed for this project. Because federal datasets are revised over time, rerunning the analysis with newer releases may produce different results.

## Methodology

1. **Select degree fields.** IPEDS completions are filtered to primary bachelor's degree awards (`AWLEVEL = 05`, `MAJORNUM = 1`) and aggregated at the four-digit CIP level.
2. **Identify the top 50.** Fields are ranked by total conferrals across reporting institutions.
3. **Prepare financial outcomes.** College Scorecard records are limited to bachelor's-level programs. Privacy-suppressed values are converted to missing values before aggregation.
4. **Aggregate nationally.** Median debt and median earnings one and four years after completion are calculated across reporting programs within each CIP field. The 25th percentile of four-year earnings is retained as a downside-risk measure.
5. **Engineer comparison metrics.** The two sources are joined by four-digit CIP code, and the indicators below are calculated.

### Derived Metrics

| Metric | Definition |
| --- | --- |
| Debt-to-Earnings Ratio | Median student debt divided by median earnings four years after completion; lower is better |
| Earnings Premium | Percentage difference between a field's four-year median earnings and the median across all bachelor's fields in the processed Scorecard data |
| Early Wage Growth | Percentage change from median earnings one year after completion to median earnings four years after completion |
| Downside Risk Floor | 25th percentile of four-year earnings among reporting programs within the field |

### Custom Value Score

The dashboard min-max normalizes three measures to a 0–1 scale:

- Four-year median earnings
- Low debt-to-earnings ratio (inverted so lower debt burden receives a higher score)
- Early wage growth

It then calculates a weighted average using the user's selected weights and converts the result to a 0–100 score. The score is a comparison tool—not a prediction of an individual's return on investment.

## Technology Stack

- **Python** for analysis and application logic
- **Pandas** and **NumPy** for data preparation and feature engineering
- **DuckDB** for SQL-based transformation of the source datasets
- **Plotly** for interactive visualization
- **Streamlit** for the web application
- **Jupyter Notebook** for the analytical workflow

## Repository Structure

```text
DegreeROI/
├── app.py                                  # Streamlit dashboard
├── college_major_earnings_analysis.ipynb   # Data preparation and analysis
├── top_50_majors_outcomes.csv              # Processed data used by the app
├── requirements.txt                        # App dependencies
└── README.md
```

## Run the Dashboard Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/aniruddhapochimcherla/DegreeROI.git
   cd DegreeROI
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   ```

   On macOS or Linux:

   ```bash
   source .venv/bin/activate
   ```

   On Windows PowerShell:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

3. Install the application dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

## Limitations

- The dashboard compares broad four-digit CIP fields; results can vary substantially among concentrations, institutions, and locations.
- College Scorecard outcomes cover students receiving federal financial aid and are subject to reporting and privacy-suppression rules.
- National values are unweighted medians across reporting programs, so they should not be interpreted as graduate-level population estimates.
- Earnings and debt may refer to different underlying cohorts and reporting periods.
- The analysis focuses on early-career financial outcomes and does not include tuition paid, completion probability, cost of living, employment rates, graduate education, or nonfinancial value.
- The custom score is sensitive to both the selected weights and the range of the 50 fields included in the dashboard.

## Future Improvements

- Make the notebook fully reproducible by programmatically retrieving every source and CIP reference file
- Add filters for field families and side-by-side major comparisons
- Incorporate tuition, employment, geographic cost-of-living, and longer-term earnings measures
- Add automated data validation and tests for the scoring logic
- Track changes across multiple data-release years

## Author

**Aniruddha Pochimcherla**

I built this as a data analytics portfolio project to demonstrate data integration, SQL-based transformation, feature engineering, interactive visualization, and deployment.

## Disclaimer

This project is for exploratory and educational purposes. Please do not treat this as financial, career, or educational advice, though it might be a good tool to explore predictive outcomes for each career path, especially if you are undecided on your major.
