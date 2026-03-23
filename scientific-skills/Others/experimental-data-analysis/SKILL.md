---
name: experimental-data-analysis
description: Perform statistical analysis on experimental data (descriptive stats, t-tests, ANOVA, multiple comparisons) when you need to interpret experimental results, assess statistical significance, or generate reproducible reports.
license: MIT
skill-author: AIPOCH
---

## When to Use

- You have experimental results in CSV format and need a reproducible end-to-end analysis workflow.
- You need to compare two conditions (independent or paired) using a t-test (or a non-parametric alternative when assumptions fail).
- You need to compare 3+ groups or multiple factors using one-way or multi-way ANOVA, including post-hoc multiple comparisons.
- You must generate report-ready outputs (tables/figures) including p-values, effect sizes, and assumption notes.
- You need strict execution hygiene where every run writes only into a timestamped run directory.

## Key Features

- Reproducible run-based execution: each analysis is isolated under `outputs/runs/<timestamp>/`.
- Data preparation guidance: missing values, outliers, and variable type identification (continuous/categorical, grouping factors).
- Descriptive statistics: mean, standard deviation, confidence intervals, and grouped summary tables.
- Inferential statistics: independent/paired t-tests, ANOVA (one-way/multi-way), and post-hoc tests (e.g., Tukey).
- Reporting outputs: test statistics, p-values, effect sizes, charts/tables, and explicit assumption documentation.
- Built-in references for method selection and reporting templates:
  - `references/stats-method-selection.md`
  - `references/reporting-template.md`

## Dependencies

- Python 3.10+ (recommended)
- pandas >= 2.0
- numpy >= 1.24
- scipy >= 1.10

## Example Usage

### 1) Initialize a new run directory

```bash
python scripts/init_run.py
```

This creates a new directory like:

```text
outputs/runs/<timestamp>/
  config.json
  (sample input files, if provided by the initializer)
```

### 2) Run the analysis (descriptive stats + t-test/ANOVA)

```bash
python scripts/analyze_experiment.py
```

**Execution standard (required):**
- Run `python scripts/init_run.py` before each execution to generate `outputs/runs/<timestamp>/`.
- All intermediate files (config, inputs, outputs) must be written inside that run directory; writing elsewhere is prohibited.
- Scripts default to using the latest run directory under `outputs/runs/`.

## Implementation Details

### Workflow Stages

1. **Data Preparation**
   - Handle missing values and outliers.
   - Identify variable types:
     - continuous vs. categorical variables
     - grouping factors (e.g., treatment group, timepoint, subject ID)

2. **Descriptive Statistics**
   - Compute summary metrics such as:
     - mean, standard deviation
     - confidence intervals (CI)
   - Produce grouped summary tables by factor levels.

3. **Inferential Statistics**
   - Choose tests based on design and assumptions:
     - **t-tests**: independent vs. paired
     - **non-parametric alternatives** when assumptions are violated
     - **ANOVA**: one-way or multi-way depending on number of factors
   - **Multiple comparisons / post-hoc**
     - Apply post-hoc procedures (e.g., Tukey) after ANOVA when appropriate.
     - Define and document the multiple-comparison control strategy.

4. **Reporting**
   - Report (at minimum):
     - test statistic, degrees of freedom (if applicable), p-value
     - effect size(s)
   - Include visualizations and result tables.
   - Explicitly document assumption checks and any deviations from the planned analysis.

### Assumption Checks and Reproducibility Notes

- Validate **normality** and **homogeneity of variance** before using parametric tests.
- Predefine how you will control for **multiple comparisons** (e.g., Tukey post-hoc after ANOVA).
- Retain analysis code, configuration, and random seeds within the run directory to ensure reproducibility.

### Script Responsibilities

- `scripts/init_run.py`
  - Creates a timestamped run directory under `outputs/runs/`
  - Generates `config.json` and (optionally) sample input data

- `scripts/analyze_experiment.py`
  - Reads CSV-based inputs from the active run directory
  - Produces descriptive statistics and inferential test outputs (t-test/ANOVA)
  - Writes all outputs back into the same run directory