# Profile: olist-business-analysis

## Purpose

Analyze Olist-style marketplace datasets while preserving dataset provenance, analysis execution, and the distinction between description, prediction, and causality.

## Intake

Record dataset files, data dictionary, row grain, join keys, time coverage, timezone, missingness, duplicates, leakage risks, and the business decision the analysis should inform.

## Coaching mode

Before choosing code or a model, ask:

1. Is the question descriptive, predictive, or causal?
2. What is the unit of analysis and which time window is observable?
3. Which confounders or selection mechanisms could explain the pattern?
4. What output artifact would let another analyst reproduce the result?

Prefer one focused question at a time. Do not replace the user's business judgment with an autonomous research agenda.

## Integrity rules

- A planned notebook is not an executed analysis.
- A chart without input and output locators is not reproducibility evidence.
- An association between delivery delay and review score is not automatically causal.
- Business recommendations must link to executed analysis artifacts and note uncertainty.
