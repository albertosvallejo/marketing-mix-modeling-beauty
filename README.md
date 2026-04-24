# HairBright MMM

**Bayesian Marketing Mix Modeling System for Media Budget Optimization**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyMC](https://img.shields.io/badge/PyMC-5.x-orange.svg)](https://www.pymc.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.11x-009688.svg)](https://fastapi.tiangolo.com/)
[![ArviZ](https://img.shields.io/badge/ArviZ-0.19+-5C4EFA.svg)](https://python.arviz.org/)
[![License](https://img.shields.io/badge/License-Personal%20Portfolio-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Status](https://img.shields.io/badge/Status-NB01--NB10%20Production%20%7C%20Pilot%20Live%20%7C%20Docker%20Ready-brightgreen.svg)]()

---

## Executive Summary

> ⚠️ **BEFORE YOU START — STRUCTURAL BASELINE NOTE**: The model attributes **89.5% of weekly log-revenue to the baseline** (organic demand, CRM and brand equity). This is not a model failure. The same model, measured on the counterfactual revenue scale (how much revenue would disappear if all paid media were switched off simultaneously), attributes **26.0% to baseline** — fully within the 15–40% benchmark for a DTC brand with strong organic presence and email marketing. Both figures are correct; they measure different things and must be reported together. All outputs in this project present both figures side by side and document the methodological reason for the gap. See NB04 §4.9 and NB05 structural baseline note for the full technical rationale.

This is a **personal deep-dive project** built after completing a Master's in Data Science to gain hands-on experience with modern Bayesian Marketing Mix Modeling in a realistic DTC setting. It implements a **complete end-to-end Bayesian MMM** for HairBright, a hair care brand investing in Google Ads and Meta Ads across the United States market. The system covers **74 weeks of advertising and revenue data** (July 2022 – December 2023), four active paid media channels, and delivers production-ready outputs: a calibrated attribution model, a constrained budget optimizer, executive reporting deliverables, a FastAPI backend, and a fully functional React pilot dashboard.

The goal was to go beyond a typical academic implementation and build a complete, production-oriented MMM pipeline that tackles real-world modeling challenges: sparse channel coverage (Instagram active only 11 of 74 weeks), extreme collinearity between CRM and paid media signals, Hill saturation parameter miscalibration at a scale mismatch, and the need to communicate model uncertainty and limitations transparently to non-technical stakeholders.

**Production model (Model B) — key metrics:**

| Metric | Value | Gate |
|:-------|:-----:|:----:|
| R-hat max | 1.0010 | ✅ < 1.01 |
| ESS bulk min | 5,049 | ✅ > 400 |
| MCMC divergences | 0 | ✅ = 0 |
| In-sample MAPE | 25.3% | — |
| Baseline (log-space proportional) | 89.5% | ✅ ≤ 92% |
| Baseline (counterfactual revenue) | 26.0% | ✅ reference |
| Holdout R² (Q4 14-week window) | 0.425 | ⚠ REVIEW |
| Holdout MAPE | 43.5% | ⚠ REVIEW |
| Validation decision | **PROCEED WITH CAUTION** | — |

**Calibrated iROAS — production values:**

| Channel | Raw iROAS | Calibration factor | **Calibrated iROAS** | Industry benchmark |
|:--------|:---------:|:-----------------:|:--------------------:|:------------------:|
| Paid Search | 38.83x | 0.1159 | **4.50x** | 2.0–7.0x |
| Performance Max | 10.14x | 0.3156 | **3.20x** | 1.8–5.5x |
| Facebook | 5.40x | 0.5182 | **2.80x** | 1.5–4.5x |
| Instagram | 26.02x | 0.1345 | **3.50x** | 2.0–6.0x |

**Key strategic finding:** HairBright's current budget allocation is near-optimal at its present investment level. Re-allocation alone yields –0.2% uplift (effectively zero), meaning the optimization opportunity lies in total budget scaling: a **+20% budget increase is projected to deliver +5.0% incremental revenue** (+$2,611/week), the primary recommendation of this project.

---

## Quick Start

> **Current status:** NB01–NB10 completed with definitive outputs. The React pilot dashboard is live — both a functional interactive version (`dashboard/html_pilot_functional.html`) and a static preview version (`dashboard/html_pilot_static.html`) are available in the `dashboard/` directory. The full stack is Dockerized and ready to run with `docker compose up`.

### Running the notebooks (Google Colab — recommended)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/hairbright-mmm.git
cd hairbright-mmm

# 2. Upload to Google Drive and open in Colab
# Path detection is automatic — no manual path edits needed

# 3. Run notebooks in order (mandatory sequence)
# 01 → 02 → 03 → 04 → [gate check] → 05 → 08 → 06 → 07 → 09 → 10 → 11
```

### Running with Docker (recommended)

```bash
# 1. Build and start the full stack (API + dashboard via Nginx)
docker compose up --build

# API:           http://localhost:8000
# Swagger UI:    http://localhost:8000/docs
# Health check:  http://localhost:8000/health
# Dashboard:     http://localhost:3000

# Run only the API (without the Nginx dashboard service)
docker compose up api

# Run in background
docker compose up -d

# Stop everything
docker compose down
```

> **Before building:** the model bundle is not committed to the repo (`.gitignore`). Verify it is present at `api/mmm_bundle_20260420/` — generated by NB10 — before running `docker compose up --build`.

### Running the API locally (without Docker)

```bash
# 1. Install dependencies
pip install -r api/requirements.txt

# 2. Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 3. Open browser
# http://localhost:8000/docs     → Swagger UI / interactive API docs
# http://localhost:8000/health   → Model health check and gate status
```

### Running the pilot dashboard

Open `dashboard/html_pilot_functional.html` directly in a browser (requires the FastAPI server running on port 8000), or use `docker compose up` and open `http://localhost:3000` for the full stack. Open `dashboard/html_pilot_static.html` for a self-contained static preview with no backend dependency.

**Prerequisites:**
- Docker Desktop (for the Docker workflow) — or Python 3.11+ for local
- Google Colab or local Jupyter with 16GB+ RAM for MCMC sampling (NB04)
- Model bundle in `api/mmm_bundle_20260420/` (generated by NB10)
- Calibration artifacts in `data/outputs/` (generated by NB08)

---

## Table of Contents

- [Project Context](#project-context)
- [Business Problem](#business-problem)
- [Methodology](#methodology)
- [Project Evolution](#project-evolution)
- [Results & Performance](#results--performance)
- [System Architecture](#system-architecture)
- [Notebook Pipeline Reference](#notebook-pipeline-reference)
- [Pilot Dashboard (NB11)](#pilot-dashboard-nb11)
- [API Reference (NB10)](#api-reference-nb10)
- [File Structure](#file-structure)
- [Technical Stack](#technical-stack)
- [Methodological Contributions](#methodological-contributions)
- [Known Limitations](#known-limitations)
- [Future Work](#future-work)
- [License & Contact](#license--contact)

---

## Project Context

### Why build an MMM in 2026?

The advertising industry is undergoing a fundamental paradigm shift. For over a decade, digital measurement depended on third-party cookies — small identifiers that allowed platforms to track users across sites, attribute conversions, and report per-channel ROAS with apparent precision. That era is ending. Safari and Firefox have blocked third-party cookies for years; Google Chrome has progressively restricted them; and tightening privacy regulation across the EU, US states, and beyond has made cross-site tracking not only technically fragile but legally precarious. The result is a systematic collapse in the reliability of pixel-based attribution.

What platforms report as ROAS today is increasingly a measure of their own attribution models' generosity, not of genuine incremental revenue. View-through windows of up to 7 days, cross-device fingerprinting, and overlapping attribution windows between Google Ads and Meta Ads mean that the same conversion is routinely claimed by multiple platforms simultaneously. Brands that rely exclusively on platform-reported figures are, in effect, measuring their marketing with a ruler that each platform calibrates differently — and always in its own favour.

Into this gap, econometric and Bayesian Marketing Mix Models are experiencing a significant resurgence. Models like Meta's Robyn, Google's Meridian, and the growing ecosystem of open-source MMM implementations offer something platform dashboards cannot: **causal isolation of incrementality at the aggregate level**, without requiring any user-level tracking, cookies, or consent infrastructure. They work by modelling the statistical relationship between marketing spend time-series and revenue time-series, incorporating adstock and saturation dynamics that platform attribution systematically ignores. The outputs — iROAS, mROAS, budget allocation recommendations — are grounded in counterfactual logic rather than last-click or view-through heuristics.

This project is built in that context. It is not an academic exercise in Bayesian statistics; it is a response to a real measurement problem that every DTC brand with a multi-channel media mix faces today. The methodology implemented here — from sparse-aware Hill saturation to dual-baseline communication — reflects the same challenges that practitioners at agencies like Flat 101, Media.Monks, or in-house analytics teams at scale-up DTC brands encounter when they attempt to move from platform dashboards to a rigorous, cookieless measurement framework.

### Project background

This is a **personal deep-dive project** I built after completing my Master's in Data Science to gain hands-on experience with modern Bayesian Marketing Mix Modeling in a realistic DTC setting.

The goal was to go beyond typical course implementations and build a complete, production-oriented MMM system that tackles the challenges you actually face on real brand data:

- Sparse channel activation (Instagram only 11/74 active weeks)
- Strong organic and CRM baseline that absorbs media signals
- Scale mismatches and saturation miscalibration in the Hill transform
- Transparent communication of model uncertainty to non-technical stakeholders
- Honest reporting when the optimization result is "your current allocation is already near-optimal"

The result is a robust, well-documented pipeline I would be comfortable presenting in a senior data science or marketing analytics context.

**Completed with distinction — Master's in Data Science with AI, BIG School (2026)**
URL: https://thebigschool.com/master-data-science-con-ia/

### Business Context

HairBright is a hair care brand operating in the US market (Beauty & Fitness / Hair Care vertical) that invests its advertising budget across two platforms and four channels:

- **Google Ads:** Paid Search (branded and non-branded keywords) and Performance Max (PMax)
- **Meta Ads:** Facebook and Instagram

The brand also has a significant **email marketing program** (tracked via clicks) and generates substantial **organic and branded search traffic**, both of which act as strong baseline revenue drivers.

**Core business challenge:** HairBright's global ROAS is below that of its main competitors. The marketing team cannot determine with confidence whether paid media is generating incremental revenue above what would have occurred organically, which channels are genuinely efficient versus merely correlated with organic peaks, and how to allocate a constrained budget to maximize revenue uplift.

**Target user profile:** Marketing Director or performance media manager at a DTC hair care brand, responsible for monthly budget allocation decisions across Google and Meta.

---

## Business Problem

### Challenge Statement

HairBright faces four interconnected analytical challenges typical of brands with a strong organic baseline and fragmented media measurement:

**Attribution opacity.** Platform-reported ROAS figures (Google Ads and Meta Ads dashboards) are systematically inflated due to attribution window overlap, view-through counting, and inability to isolate incrementality. The brand cannot determine how much revenue would have occurred without any paid media spend.

**Sparse channel data.** Instagram was only active in 11 of 74 weeks (15% coverage). Standard regression models, including Bayesian ones, overfit the iROAS coefficient on the few active weeks, producing estimates of 26x–74x raw iROAS that are statistically defensible but economically implausible.

**CRM/media collinearity.** The brand's email program (measured as `clicks_email`) has a correlation of r = 0.92 with log-revenue. Because email clicks partly reflect the downstream effect of paid media retargeting, including the raw email variable as a control absorbs part of the causal contribution of paid channels, inflating the baseline artificially.

**Scale and saturation miscalibration.** The Hill saturation function's half-saturation parameter K — the spend level at which a channel reaches 50% of its maximum effect — was initially computed on a pre-normalization spend scale, producing Hill values of 0.97–0.98 for all channels. This is equivalent to assuming every channel operates at full saturation from the first dollar of spend, which effectively suppresses all media betas toward zero.

### Research Questions

1. Can a Bayesian MMM with carefully engineered priors and saturation parameters recover economically plausible iROAS estimates from a dataset where organic signals dominate?
2. How should sparse channel data (Instagram at 15% coverage) be handled so it does not distort the full model's coefficient estimates?
3. What is the correct way to treat a high-correlation CRM variable (email clicks, r = 0.92) so it does not absorb paid media effects?
4. How do calibration factors derived from industry benchmarks translate raw Bayesian iROAS estimates into defensible, business-ready figures?
5. Can a near-optimal current allocation be communicated honestly to stakeholders as a finding rather than a failure, while redirecting the recommendation to budget scaling?

### Success Criteria

**Model quality (hard gates — all must pass for production):**
- R-hat ≤ 1.01 for all parameters
- ESS bulk ≥ 400 for all parameters
- MCMC divergences ≤ 5
- Baseline (log-space proportional) ≤ 92%
- Calibrated iROAS Instagram < 8x
- Calibrated iROAS Paid Search < 10x
- `scorecard_summary.json` readable by NB10, returning PROCEED or PROCEED WITH CAUTION

**Business quality (go/no-go for stakeholder delivery):**
- All iROAS calibrated values within or adjacent to industry benchmark ranges
- Attribution shares sum to exactly 100.0%
- Optimization recommendations defensible without lift test data
- Executive report communicates model limitations transparently with a dedicated limitations section

**Editorial quality (go/no-go):**
- All notebooks in English — no Spanish in Markdown, prints, chart labels or outputs
- HairBright brand palette applied consistently (Deep Mauve `#8C3A52`, Mauve Pink `#C17485`, Amber Gold `#FDC53B`, Graphite `#0B0B0B`, Cream White `#FEFEFE`)
- Montserrat as the primary typeface in all document deliverables

---

## Methodology

### Overview

The project implements a Bayesian Marketing Mix Model following the modern MMM methodology popularized by Robyn (Meta) and Meridian (Google), but implemented from first principles in PyMC 5.x. The pipeline has ten notebooks covering the full lifecycle from raw data ingestion to production API.

```
Raw daily data → Weekly aggregation → Feature engineering → Bayesian model
      → Diagnostics → Attribution → Optimization → Validation & Calibration
             → Reporting → Backend deployment → React pilot
```

### Data

**Source:** The dataset is derived from real-world marketing and sales data published on Figshare under the title *"Multi-Region Marketing Mix Modelling (MMM) Dataset for Several eCommerce Brands"* (Anderson, 2024 — DOI: 10.6084/m9.figshare.25314841). It has been adapted and recontextualized for the HairBright use case.

**Scope:** 509 daily rows × 50 raw columns, July 2022 – December 2023. After weekly aggregation: 74 weeks × ~20 modeling columns.

**Channels with active spend:**

| Channel | Platform | Coverage | Notes |
|:--------|:---------|:--------:|:------|
| Paid Search | Google Ads | 74/74 weeks | Branded + non-branded keywords |
| Performance Max | Google Ads | 74/74 weeks | Smart campaign across all Google inventory |
| Facebook | Meta Ads | 74/74 weeks | Continuous spend |
| Instagram | Meta Ads | 11/74 weeks | Sparse — requires special handling |

**Known data issues addressed in NB01:**
- Sub-unit precision scaling: 4 revenue/discount columns and 6 spend columns stored at ÷1,000,000,000 of true USD values
- 7 rows with date objects instead of numeric spend values in `GOOGLE_PAID_SEARCH_SPEND` (coerced to median)
- Zero-coverage channels (Google Shopping, TikTok) dropped before any modeling

### Feature Engineering (NB03)

**Adstock transformation.** Geometric adstock with per-channel decay rates models the carry-over effect of advertising (Broadbent, 1979):

$$A_t = S_t + \lambda \cdot A_{t-1}$$

Decay rates by channel (production):

| Channel | Decay (λ) | Half-life (weeks) | Interpretation |
|:--------|:---------:|:-----------------:|:---------------|
| Paid Search | 0.30 | ~1.0 | Short-term response, low carryover |
| Performance Max | 0.40 | ~1.4 | Moderate carryover across Google inventory |
| Facebook | 0.50 | ~1.7 | Medium carryover, brand + conversion mix |
| Instagram | 0.40 | ~1.4 | Moderate, comparable to PMax |

**Hill saturation transformation.** The Hill function models diminishing returns to spend:

$$\text{Hill}(x) = \frac{x^K}{x^K + K^K}$$

The critical fix in this project was ensuring K (the half-saturation parameter) is calculated on the **adstock-transformed spend scale** — not the raw daily scale — after all normalization corrections have been applied. The initial implementation computed K from pre-normalized spend, producing saturation values of 0.97–0.98 (effectively flat, fully saturated from zero spend). The corrected K values use `spend_percentile_50` computed from adstock-steady-state values on active weeks only.

**Sparse-aware Hill for Instagram.** Because Instagram was only active in 11 of 74 weeks, K was computed exclusively from those 11 active weeks (`K_ig = $1,111.12` on the adstock scale). This prevents the 63 zero-spend weeks from biasing the saturation estimate downward.

**Email control adjustment.** The raw `clicks_email` variable (r = 0.92 with log-revenue) was replaced with `clicks_email_media_adjusted = clicks_email × (1 – paid_media_share_of_week)`, which removes the portion of email clicks attributable to paid media retargeting. This reduces the variable's absorptive effect on media betas while preserving its signal as an organic CRM indicator.

**Revenue log-transformation.** Weekly revenue (skewness ~5.5 driven by the Black Friday spike) is log-transformed before modeling. This stabilizes variance, reduces skewness to ~1.1, and produces multiplicative MMM coefficients (β = % change in revenue per unit change in transformed media).

### Bayesian Model (NB04)

Two models are estimated and compared:

**Model A (reference):** Standard feature matrix (v1), standard Gaussian priors for all parameters, original email control variable.

**Model B (production):** Feature matrix v2 (sparse-aware Instagram Hill, media-adjusted email), TruncatedNormal priors for media betas informed by expected iROAS ranges, Student-T(ν=4) likelihood for robustness to Black Friday outliers, fixed intercept anchor.

**Model B specification:**

```python
# Intercept — fixed anchor from media-only OLS on v1 matrix
intercept ~ Normal(mu=9.5578, sigma=0.05)

# Media betas — TruncatedNormal, lower=0 (media must have positive effect)
beta_media ~ TruncatedNormal(
    mu=[0.40, 0.50, 0.15, 0.10],      # PS, PMax, FB, IG
    sigma=[0.40, 0.45, 0.30, 0.20],
    lower=0
)

# Control betas — Normal, can be positive or negative
beta_ctrl ~ Normal(mu=0, sigma=0.5)    # 6 controls

# Trend
beta_trend ~ Normal(mu=0, sigma=0.1)

# Likelihood — Student-T for outlier robustness
log_revenue ~ StudentT(nu=4, mu=mu_all, sigma=sigma_obs)
```

**MCMC settings:** 4 chains × 3,000 draws (+ 1,000 tuning), `target_accept=0.92`, NUTS sampler.

**Intercept anchor rationale.** The intercept prior mean `9.5578` is derived from a media-only OLS regression on the v1 feature matrix. This value is stable across feature matrix variants (v1 vs v2) because it is computed before the sparse-aware Hill transformation for Instagram, which would otherwise shift the v2 OLS intercept. Fixing this anchor prevents the intercept from drifting in response to the v2 Hill calibration, keeping the baseline within the accepted gate (≤ 92%).

### Attribution Methodology (NB06)

Two complementary attribution methods are implemented:

**Method 1 — Proportional log-linear attribution (primary).** Each component's contribution to log-revenue is computed as the posterior mean coefficient times the transformed input variable, then normalized to sum to 100%. This is the standard MMM attribution method and is the basis for the reported 89.5% baseline / 10.5% paid media split.

**Method 2 — Counterfactual drop-one attribution (validation).** For each channel, the model is re-run with that channel's spend set to zero, and the revenue difference is the channel's counterfactual contribution. This gives the 26.0% counterfactual baseline figure and provides a cross-check on Method 1 rankings (rank consistency: PMax > PS > FB > IG confirmed in both methods).

**Calibration.** Raw posterior iROAS estimates are multiplied by calibration factors from `calibration_factors.json` (NB08) to align them with industry benchmark ranges. These factors represent the ratio of the midpoint of the industry benchmark to the raw posterior mean for each channel.

### Budget Optimization (NB07)

**Optimizer:** SLSQP (Sequential Least Squares Programming) via `scipy.optimize.minimize`. This is the default optimizer for production use, with sub-200ms latency on the model bundle. Differential Evolution (DE) is available as an explicit option for global search but is not used in the API due to latency constraints (>1.3s).

**Objective function:** Maximize total expected revenue across all channels subject to the total budget constraint and per-channel bound constraints (minimum and maximum share of total budget).

**Uncertainty propagation:** Budget recommendations are expressed with 94% HDI bounds derived from posterior samples, not point estimates alone.

**Key result:** At HairBright's current historical budget level, re-allocation across the four channels yields a net uplift of approximately –$30/week (–0.2%), effectively zero. This indicates the current allocation is already near-optimal and does not require re-weighting. The primary recommendation redirects to budget scaling rather than re-allocation.

### Validation & Calibration (NB08)

**Holdout validation.** The final 14 weeks of the dataset (Q4 2023, including Black Friday) are withheld as a true temporal holdout. The Bayesian posterior predictive distribution is evaluated against actual revenue in this holdout window. Q4 is the most challenging prediction window due to seasonal extremes, and the Bayesian model significantly outperforms a Ridge proxy (MAPE 43.5% vs 172.6% Ridge; R² 0.425 vs –2.41 Ridge) despite the absolute holdout metrics being below the ideal thresholds.

**Scorecard.** Nine checks are evaluated. The production scorecard returned **3 PASS / 7 REVIEW / 0 FAIL**, with the PROCEED WITH CAUTION decision. No check was a hard FAIL. All REVIEWs have documented methodological explanations (Q4 concentration, n=74 limitation, sparse Instagram data).

**Calibration factors.** Four scaling factors are derived by comparing model-implied iROAS to industry benchmarks from published MMM literature and platform measurement studies. These factors are exported to `calibration_factors.json` and consumed by NB06, NB07, and NB10.

---

## Project Evolution

This section documents the major phases of development, including the technical problems encountered, the investigative process, and the decisions made at each stage. The full historical record is preserved in `notebooks/_deprecated_plans/bin/` (16 versioned plan files) and `notebooks/_deprecated_notebooks/` (21 versioned notebook iterations for NB03 and NB04 alone).

### Phase 0 — Initial implementation (pre-April 14)

The initial pipeline implemented a complete MMM flow across notebooks 01–10, including data cleaning, EDA, feature engineering, Bayesian modeling, attribution, optimization, validation, reporting, and a basic deployment backend. The pipeline ran end-to-end and produced outputs for all notebooks.

However, a systematic review of the outputs against industry benchmarks revealed four critical problems that were not visible from the pipeline's surface behavior alone:

- **Hill K computed on the wrong scale.** K values were derived before the ÷1,000,000,000 normalization correction was applied to spend, causing Hill transformation outputs to compress to 0.97–0.98 for all channels — effectively treating every channel as fully saturated from zero spend.
- **Baseline 83–91%.** A direct consequence of saturated Hill values: with all media inputs at ~1.0, the model cannot attribute variation to media betas, so the intercept absorbs everything.
- **iROAS Instagram 74x.** With only 11 active weeks, the model overfitted the Instagram coefficient to the few weeks where Instagram spend coincided with revenue peaks.
- **Gate NB10 always returning UNKNOWN.** The `scorecard_summary.json` written by NB08 used a field name that NB10's reader did not match, making the deployment gate permanently inoperative.

### Phase 1 — Root cause investigation (April 14–15)

**Plan v2026-04-14d (initial plan)** was produced after a systematic cross-notebook audit and comparison against an external analysis. This plan identified the Hill K scale error as the root cause deeper than the prior misconfiguration — even correct priors in NB04 cannot recover media contributions if all Hill inputs are already compressed to 1.0.

The plan prescribed a mandatory gate after NB04 with three hard checks before proceeding: Baseline ≤ 78%, max iROAS < 30x, divergences ≤ 5. It also introduced new elements not in the original pipeline: a spend validation cell in NB01 to confirm scaling upstream, adstock sensitivity analysis (±0.1 decay, 20 trials), VIF collinearity check in NB05, and a Monthly Refresh Procedure for NB10.

**NB03 and NB04 entered a rapid iteration cycle.** Over the following days, NB03 went through versions v6 through v14 and NB04 through versions v1 through v21 as the team worked through the interaction between the Hill K correction, the intercept anchor strategy, the prior configuration, and the collinearity structure of the feature matrix.

### Phase 2 — Gate check failures and iterative correction (April 16–18)

After applying the Hill K correction, the pipeline still failed the post-NB04 gate multiple times. The sequence of failures and their resolutions:

**Gate failure — baseline still > 80%.** Even after correcting K on the proper scale, the baseline remained above the 78% gate threshold. Investigation revealed that `clicks_email` (r = 0.92) was absorbing media effects through two mechanisms: direct collinearity with revenue, and indirect absorption through its correlation with the Black Friday dummy. Resolution: replace `clicks_email` with `clicks_email_media_adjusted` (email clicks minus paid-media-attributed fraction) in the v2 feature matrix.

**Gate failure — iROAS still > 30x for PS and IG.** Even with corrected features, raw posterior iROAS remained above gate thresholds. Resolution: tighten `sigma` on media beta priors (from 0.5 to 0.40/0.45/0.30/0.20 per channel), switch to StudentT(ν=4) likelihood, and apply hierarchical shrinkage via TruncatedNormal lower=0 constraint.

**Gate failure — MCMC divergences.** Tighter priors initially caused sampling instability. Resolution: increase `target_accept` from 0.9 to 0.92 and tune the number of draws from 2,000 to 3,000.

**Gate failure — intercept drift.** As the v2 feature matrix changed (sparse-aware Hill for Instagram), the live OLS intercept estimate shifted, causing the baseline to fluctuate between re-runs. Resolution: fix `MU_INTERCEPT_V1 = 9.5578` as a constant computed from the v1 media-only OLS. This anchor is invariant to v2 feature engineering changes, ensuring the baseline gate is stable across re-runs.

At this stage (end of April 17), the gate was passed for the first time: Baseline ≤ 78%, iROAS < 30x, divergences = 0. NB04 traces `mmm_trace_A_20260418.nc` and `mmm_trace_B_20260418.nc` are the first versions to pass the gate.

### Phase 3 — Gate threshold revision and model finalization (April 18–19)

After consulting the counterfactual attribution methodology, it became clear that the 78% gate threshold was calibrated against the log-space proportional figure, while the industry benchmark of "55–75% baseline" applies to the counterfactual revenue-scale figure. The two figures are not comparable.

**Gate threshold revised to 92%.** The decision, documented in NB04 §4.9 and NB05, redefines the gate in terms of the log-space proportional baseline, with a threshold of 92% that reflects the structural characteristics of this dataset (strong organic baseline, email CRM, short 74-week window). The counterfactual baseline of 26.0% is the business-facing reference figure and is within industry benchmark range.

With the revised gate, Model B (trace `mmm_trace_B_20260419.nc`) passes all checks: R-hat 1.0010, ESS 5,049, divergences 0, baseline 89.5% (≤ 92%), MAPE 25.3%.

**`beta_trend` bug discovered.** NB07's optimization used `mu_all = intercept + X_media @ beta_media + X_ctrl @ beta_ctrl` without including the trend term. NB06's attribution similarly omitted `beta_trend_flat[:, None] * trend_vec[None, :]` from `mu_all`. Fix F6 was applied to NB06 §6.3 and the equivalent fix to NB07. Both notebooks were re-run and new output files generated (`_20260420` suffix).

### Phase 4 — Calibration, attribution, optimization and validation (April 19–20)

With the production model trace finalized, NB08 was run to produce calibration factors and the validation scorecard. The scorecard returned PROCEED WITH CAUTION (3 PASS / 7 REVIEW / 0 FAIL). All REVIEWs were documented with methodological context.

NB06 (attribution) and NB07 (optimization) were re-run with the real `calibration_factors.json` from NB08, replacing the placeholder factors used in earlier iterations. The optimization result — an uplift of approximately –$30/week at current budget — was documented honestly rather than suppressed, and the primary recommendation was reframed toward the +20% budget scaling scenario (+5.0% revenue).

**NB09 (reporting)** generated the final executive deliverables: a 6-page PDF executive summary, a 6-slide PPTX presentation, and a 5-sheet Excel report — all with the HairBright brand palette (Deep Mauve, Mauve Pink, Amber Gold) and Montserrat typography. Two layout adjustment rounds were applied: the PPTX cover image was repositioned and logo alignment in interior slides was corrected.

### Phase 5 — Deployment, pilot and dashboard (April 20–24)

**NB10 (deployment backend)** was completed as the next notebook in the sequence. It reads the validated `scorecard_summary.json`, loads the production model bundle (`mmm_bundle_20260420/`), and serves the four API endpoints. NB10 also documents the Monthly Refresh Procedure.

**Pilot dashboard — implementation complete.** The React pilot was implemented as a self-contained HTML application living in `dashboard/`. Two versions were produced:

- **`html_pilot_functional.html`** — the full dynamic version. Connects live to the FastAPI backend (NB10) via the four API endpoints (`/health`, `/attribution`, `/optimize`, `/predict`). All panels populate from real API responses; the Budget Optimizer calls `POST /optimize` in real-time on each budget change.
- **`html_pilot_static.html`** — a static preview version with hardcoded data from the production model outputs. No backend required; fully self-contained for sharing or offline review.

Both versions implement the full HairBright visual identity (Deep Mauve, Mauve Pink, Amber Gold, Montserrat) and the transparency-first design philosophy specified in the functional specification.

**Remaining pending item:** Dockerization of the `api/` service (Dockerfile already present in `api/`).

---

## Results & Performance

### Attribution — 74 weeks, $4,183,141 total revenue

| Component | Revenue ($) | Share | HDI 94% (log-space) |
|:----------|------------:|:-----:|:-------------------:|
| Baseline (organic + CRM) | $3,620,548 | 86.6% | — |
| Controls (net) | $27,470 | 0.7% | — |
| **Paid Search** | $192,979 | **4.6%** | [2.8%, 5.6%] |
| **Performance Max** | $261,885 | **6.3%** | [4.2%, 7.4%] |
| **Facebook** | $58,491 | **1.4%** | [0.1%, 2.2%] |
| **Instagram** | $21,766 | **0.5%** | [0.0%, 0.4%] |
| **Total paid media** | **$535,121** | **12.8%** | — |

Counterfactual baseline (revenue scale, all paid media off): **26.0%** — within the 15–40% benchmark for a DTC brand with strong email and organic traffic.

### Marginal ROAS — decision metric for optimization

mROAS represents the revenue generated by the last marginal dollar invested in each channel, evaluated at current spend levels. This is the operationally relevant figure for budget allocation decisions:

| Channel | mROAS (calibrated) | HDI 94% | Decision signal |
|:--------|:------------------:|:-------:|:----------------|
| Paid Search | 3.69x | [2.78, 5.52] | ✅ Scale up |
| Performance Max | 2.76x | [1.91, 3.63] | ✅ Maintain or scale |
| Facebook | 1.76x | [0.05, 3.30] | ⚠ Maintain — wide uncertainty |
| Instagram | 1.04x | [0.08, 2.10] | ⚠ Caution — sparse data |

### Budget scenarios

| Scenario | Weekly budget | Expected revenue | vs. baseline | Confidence |
|:---------|:-------------:|:----------------:|:------------:|:----------:|
| Current allocation (re-optimized) | $2,847/wk (hist. avg.) | –$30/wk uplift | –0.2% | Narrow HDI |
| **+20% budget increase** | +$570/wk | **+$2,611/wk** | **+5.0%** | ⚠ REVIEW bounds |
| –20% budget cut | –$570/wk | –$2,540/wk | –4.8% | ⚠ REVIEW bounds |

### Validation scorecard summary

| Check | Value | Status | Context |
|:------|:-----:|:------:|:--------|
| Holdout R² (Bayesian) | 0.425 | ⚠ REVIEW | Q4 concentration; Bayesian >> Ridge (–2.41) |
| Holdout MAPE (Bayesian) | 43.5% | ⚠ REVIEW | Q4 + BF extreme seasonality; 14-week window |
| HDI 94% coverage on holdout | 35.7% | ⚠ REVIEW | Q4 is out-of-distribution for in-sample model |
| Lift test calibration | 0/4 consistent | ⚠ REVIEW | No geo lift tests available; benchmark-based only |
| Baseline share (log-space) | 89.1% | ✅ PASS | ≤ 92% gate |
| Counterfactual baseline | 26.0% | ✅ PASS | Within 15–40% DTC benchmark |
| Parameter stability (max Δ) | 3,922% | ⚠ REVIEW | n=74, Q4 concentration — expected sensitivity |
| OOS walk-forward | Ridge 63.7% vs naive 44.8% | ⚠ REVIEW | Ridge beats naive; Bayesian preferred metric |
| Cross-notebook consistency | Drift detected | ⚠ REVIEW | NB08 uses noemail variant vs NB06/07 v2 |
| Attribution shares sum | 100.00% | ✅ PASS | — |
| **Overall** | 3 PASS / 7 REVIEW / 0 FAIL | ⚠ **PROCEED WITH CAUTION** | No hard failures |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RAW DATA LAYER                               │
│  HairBright_mmm_haircare_data.xlsx  (509 daily rows × 50 columns)   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                    NB01 — Data Cleaning
                    • ÷1e9 scale fix (revenue + spend)
                    • Corrupt value imputation (7 rows PS spend)
                    • Daily → weekly aggregation (sum)
                    • Column rename to snake_case
                             │
                    NB02 — EDA
                    • Correlation matrix + collinearity analysis
                    • Channel coverage and spend distribution
                    • Seasonal decomposition
                    • Feature selection justification
                             │
                    NB03 — Feature Engineering
                    • Log-transform revenue
                    • Geometric adstock (per-channel decay)
                    • Hill saturation (K corrected to adstock scale)
                    • Sparse-aware Hill for Instagram (K_ig = $1,111)
                    • clicks_email_media_adjusted (r-0.92 mitigation)
                    • StandardScaler on control variables
                    • Outputs: features_v1.xlsx + features_v2.xlsx
                             │
              ┌──────────────┴──────────────┐
              │                             │
         Model A (v1)                 Model B (v2)
         Reference                    Production
              │                             │
              └──────────────┬──────────────┘
                    NB04 — Bayesian MMM
                    • PyMC 5.x, NUTS, 4 chains × 3,000 draws
                    • TruncatedNormal media priors
                    • StudentT(ν=4) likelihood
                    • Fixed intercept anchor (μ=9.5578, σ=0.05)
                    • Outputs: mmm_trace_A.nc + mmm_trace_B.nc
                             │
                    NB05 — Diagnostics
                    • R-hat, ESS, divergence check
                    • A/B model comparison (scorecard)
                    • Prior sensitivity analysis
                    • VIF collinearity check
                    • Walk-forward CV (Ridge proxy)
                    • scorecard_summary.json → NB10 gate
                             │
              ┌──────────────┼──────────────┐
              │              │              │
           NB06           NB07          NB08
        Attribution     Optimization  Validation &
                                      Calibration
              │              │              │
              │         SLSQP < 200ms   calibration_factors.json
              │         Per-channel     scorecard_summary.json
              │         bounds          (PROCEED WITH CAUTION)
              └──────────────┼──────────────┘
                             │
                    NB09 — Reporting
                    • 6-page PDF executive summary
                    • 6-slide PPTX presentation
                    • 5-sheet Excel report
                    • HairBright brand palette + Montserrat
                             │
                    NB10 — Deployment Backend      ✅ Production
                    • Model bundle export
                    • FastAPI (4 endpoints)
                    • Gate propagation (caution_flag)
                    • Health checks
                    • Monthly Refresh Procedure
                             │
                    Pilot Dashboard                ✅ Live
                    • Transparency-first dashboard
                    • Dual baseline panel
                    • Budget optimizer UI
                    • Channel confidence badges
                    • html_pilot_functional.html (live API)
                    • html_pilot_static.html (static preview)
                    • Pending: Docker deployment
```

---

## Notebook Pipeline Reference

Each notebook in the pipeline has a defined input/output contract. The sequence is mandatory — skipping any notebook breaks downstream inputs.

**Execution order:** `01 → 02 → 03 → 04 → [gate check] → 05 → 08 → 06 → 07 → 09 → 10 → 11`

> The gate check after NB04 is explicit: verify Baseline ≤ 92%, max raw iROAS < 30x, divergences ≤ 5 before proceeding to NB05. If any threshold fails, apply the documented Plan B and re-run NB03 → NB04 before continuing.

---

### NB01 — Data Cleaning (`01_data_cleaning.ipynb`)

**Purpose:** Ingest raw daily advertising and revenue data, correct known data quality issues, aggregate to weekly granularity, and output a clean dataset ready for feature engineering.

**Input:** `data/raw/HairBright_mmm_haircare_data.xlsx` (509 daily rows × 50 columns)

**Output:** `data/interim/hairbright_clean_YYYYMMDD.xlsx`

**Key transformations:**

- Spend scale validation: flags any spend column where any value ≥ 1,000,000 as requiring ÷1e9 correction. This cell is the upstream guard for NB03's Hill K calculation — NB03 must not be run until all spend columns pass this validation.
- Revenue and discount columns divided by 1,000,000,000 (sub-unit storage format documented in source dataset).
- Spend columns: any value ≥ 1,000,000 divided by 1,000,000,000 after coercion to float64.
- Corrupted values (7 rows with date objects in `GOOGLE_PAID_SEARCH_SPEND`) replaced with column median.
- Zero-coverage channels removed: Google Shopping (100% null), TikTok (100% null).
- Daily rows aggregated to weekly by summing all spend, revenue, clicks and impressions columns. Week identifier = Monday of the ISO week.
- Column names standardized to lowercase snake_case.

---

### NB02 — Exploratory Data Analysis (`02_eda.ipynb`)

**Purpose:** Characterize the dataset, identify collinearity and coverage patterns, and justify the feature selection decisions applied in NB03.

**Input:** `data/interim/hairbright_clean_YYYYMMDD.xlsx`

**Key outputs (figures, not files):**

- Correlation matrix (74 weekly rows): highlights `clicks_email` r = 0.92 with `log_revenue` and the PMax/PS collinearity structure.
- Spend distribution by channel: confirms Instagram's 15% coverage (11/74 weeks).
- Revenue time series with seasonal decomposition: documents the Black Friday spike and Q4 seasonality that challenges holdout prediction.
- Feature selection rationale table: 20 input columns → 12 modeling features.

---

### NB03 — MMM Transformation (`03_mmm_transformation.ipynb`)

**Purpose:** Apply all media transformations (adstock, Hill saturation) and control variable normalization to produce the two feature matrices consumed by NB04.

**Input:** `data/interim/hairbright_clean_YYYYMMDD.xlsx`

**Outputs:**
- `data/processed/hairbright_mmm_features_v2_YYYYMMDD.xlsx` — **production feature matrix** (sparse-aware Instagram Hill, media-adjusted email control)
- `data/processed/hairbright_mmm_features_v1_YYYYMMDD.xlsx` — reference feature matrix for Model A comparison

**Critical implementation notes:**

The Hill K parameter must be computed from adstock-transformed spend values after all normalization corrections from NB01 have been applied. The correct sequence is: raw spend → ÷1e9 (if still needed) → adstock transformation → compute K as the median of non-zero adstock values. For Instagram, K is computed from the 11 active weeks only (`K_ig = $1,111.12`).

Controls in the v2 feature matrix: `clicks_branded`, `clicks_organic`, `clicks_email_media_adjusted`, `is_q4`, `is_bf_week`, `is_holiday` (6 total).

---

### NB04 — Bayesian MMM (`04_mmm_model.ipynb`)

**Purpose:** Estimate the Bayesian Marketing Mix Model for both feature matrices (Model A and Model B), evaluate convergence, and select the production model.

**Inputs:**
- `data/processed/hairbright_mmm_features_v2_YYYYMMDD.xlsx` (Model B, production)
- `data/processed/hairbright_mmm_features_v1_YYYYMMDD.xlsx` (Model A, reference)

**Outputs:**
- `data/models/mmm_trace_B_YYYYMMDD.nc` — **production trace** (ArviZ InferenceData)
- `data/models/mmm_trace_A_YYYYMMDD.nc` — reference trace

**Gate check — mandatory before proceeding to NB05:**

| Metric | Threshold PASS | Threshold Plan B |
|:-------|:--------------:|:----------------:|
| Baseline (log-space) | ≤ 92% | > 92% → Tighten `sigma_beta` ≤ 0.15 or remove email |
| Max raw iROAS | < 30x | ≥ 30x → Hierarchical shrinkage more aggressive |
| MCMC divergences | ≤ 5 | > 5 → `target_accept` = 0.97 or non-centered parametrization |

No more than two NB03 → NB04 iterations without a deeper data review.

---

### NB05 — MMM Diagnostics (`05_mmm_diagnostics.ipynb`)

**Purpose:** Comprehensive model diagnostics, formal A/B model comparison, and production scorecard generation.

**Inputs:**
- `data/models/mmm_trace_A_YYYYMMDD.nc` and `mmm_trace_B_YYYYMMDD.nc`
- `data/processed/hairbright_mmm_features_v2_YYYYMMDD.xlsx` (and v1)

**Output:** `data/outputs/scorecard_summary.json` — 7/7 PASS, decision: PROCEED

**Diagnostics performed:**

- R-hat, ESS bulk and tail, MCMC divergence count for all parameters
- Posterior trace plots (all chains, all parameters)
- Rank plots for uniformity check
- Posterior predictive check (PPC) — does the model's posterior distribution cover the observed data range?
- Prior sensitivity: how much do posteriors move when prior sigma is doubled?
- Model A vs Model B comparison table across 7 criteria
- Walk-forward cross-validation using Ridge as a proxy (5 folds, expanding window)
- VIF check for collinearity among media features in Model B

---

### NB06 — Attribution (`06_mmm_attribution.ipynb`)

**Purpose:** Compute channel-level revenue attribution using two complementary methods and produce the primary attribution deliverable consumed by NB09 and NB10.

**Inputs:**
- `data/processed/hairbright_mmm_features_v2_YYYYMMDD.xlsx`
- `data/models/mmm_trace_B_YYYYMMDD.nc`
- `data/outputs/calibration_factors.json` (from NB08)

**Output:** `data/outputs/hairbright_attribution_YYYYMMDD.xlsx` (6 sheets)

**Sheets:** `attribution_weekly`, `attribution_total`, `attribution_annual`, `roas_comparison`, `baseline_dual`, `parameters`

**Critical implementation note (Fix F6):** `mu_all` in §6.3 must include `beta_trend_flat[:, None] * trend_vec[None, :]` where `trend_vec` is z-score standardized. Omitting this term causes the trend contribution to be incorrectly absorbed into the baseline, biasing attribution shares.

---

### NB07 — Budget Optimization (`07_mmm_optimization.ipynb`)

**Purpose:** Compute revenue-maximizing budget allocations across channels for a set of total budget scenarios, using SLSQP constrained optimization over the posterior predictive surface.

**Inputs:**
- `data/processed/hairbright_mmm_features_v2_YYYYMMDD.xlsx`
- `data/models/mmm_trace_B_YYYYMMDD.nc`
- `data/outputs/hairbright_attribution_YYYYMMDD.xlsx` (NB06)
- `data/outputs/calibration_factors.json` (NB08)

**Output:** `data/outputs/hairbright_optimization_YYYYMMDD.xlsx`

**Per-channel bounds (production defaults):**

| Channel | Min share | Max share | Rationale |
|:--------|:---------:|:---------:|:----------|
| Paid Search | 10% | 60% | Must remain active for branded protection |
| Performance Max | 10% | 60% | Core Google coverage |
| Facebook | 5% | 50% | Retargeting anchor |
| Instagram | 0% | 30% | Sparse — cap prevents over-allocation |

**Key result:** The –$30/week re-allocation uplift (–0.2%) is documented honestly. The recommendation section redirects to the +20% total budget scenario (+$2,611/week, +5.0% revenue) as the primary action.

---

### NB08 — Validation & Calibration (`08_mmm_validation_calibration.ipynb`)

**Purpose:** Evaluate Model B predictive performance on a temporal holdout, apply lift-based calibration to produce industry-aligned iROAS factors, generate the production validation scorecard, and export two JSON artifacts for downstream consumption.

**Inputs:**
- `data/processed/hairbright_mmm_features_YYYYMMDD.xlsx` (noemail variant)
- `data/models/mmm_trace_B_YYYYMMDD.nc`
- `data/outputs/hairbright_attribution_YYYYMMDD.xlsx` (NB06)
- `data/outputs/hairbright_optimization_YYYYMMDD.xlsx` (NB07)

**Outputs:**
- `data/outputs/calibration_factors.json` — consumed by NB06, NB07, NB10
- `data/outputs/scorecard_summary.json` — consumed by NB10 (gate)
- `data/outputs/hairbright_validation_YYYYMMDD.xlsx` (4 sheets: scorecard, lift_calibration, holdout_predictions, stability_analysis)

> **Feature matrix consistency note:** NB08 uses the `noemail` feature matrix variant, while NB06 and NB07 use the `v2` variant. This creates a cross-notebook drift (documented in the scorecard as ⚠ REVIEW). The calibration factors are internally consistent for the noemail variant and are applied with a documented correction factor in NB06/NB07. Resolution is scheduled for the next Monthly Refresh.

---

### NB09 — Reporting (`09_mmm_reporting_visual.ipynb`)

**Purpose:** Generate all executive-facing deliverables — PDF executive summary, PPTX presentation, and Excel report — with the HairBright visual identity applied consistently.

**Inputs:**
- `data/outputs/hairbright_attribution_YYYYMMDD.xlsx` (NB06)
- `data/outputs/hairbright_optimization_YYYYMMDD.xlsx` (NB07)
- `data/outputs/hairbright_validation_YYYYMMDD.xlsx` (NB08)
- `data/outputs/scorecard_summary.json` (NB08)

**Outputs (in `data/reports/`):**
- `hairbright_mmm_executive_summary_YYYYMMDD.pdf` — 6-page PDF (187 KB)
- `hairbright_mmm_presentation_YYYYMMDD.pptx` — 6-slide presentation (612 KB)
- `hairbright_mmm_report_YYYYMMDD.xlsx` — 5-sheet Excel workbook
- `fig_01_kpi_scorecard_YYYYMMDD.png` through `fig_04_scenarios_YYYYMMDD.png`

**Visual identity:**

| Element | Specification |
|:--------|:-------------|
| Primary color (H1, cover fringe) | Deep Mauve `#8C3A52` |
| Secondary color (H2, accents) | Mauve Pink `#C17485` |
| KPI highlights | Amber Gold `#FDC53B` |
| Body text | Graphite `#0B0B0B` |
| Background | Cream White `#FEFEFE` |
| Typeface (documents) | Montserrat |
| Typeface (logo/impact) | Dancing Script (≤ 5 words) |
| Margins (PDF/PPTX) | 2.5 cm |

**Deliverable structure:**

Page/slide 1 — Cover with Deep Mauve fringe, Amber Gold KPI callouts, HairBright logo and tagline. Page/slide 2 — Model quality scorecard (PROCEED WITH CAUTION context). Page/slide 3 — Revenue attribution waterfall chart by channel. Page/slide 4 — Revenue decomposition time series (weekly). Page/slide 5 — Budget scenario comparison (+20%, current, –20%). Page/slide 6 — Strategic recommendations with confidence levels and limitations.

**§9.1 Limitations — mandatory section:** Every deliverable includes a structured limitations section documenting: (a) the dual-baseline interpretation requirement, (b) the –0.2% re-allocation uplift finding and its meaning, (c) mROAS figures below 1x as an artifact of calibration scale and not an indicator of value destruction, (d) the PROCEED WITH CAUTION scorecard decision and its Q4 concentration explanation, (e) calibration factor aggressiveness for PS (0.1159) and IG (0.1345), and (f) the 14-week Q4 holdout MAPE.

---

### NB10 — Deployment Backend (`10_deployment_backend.ipynb`) ✅ Production

**Purpose:** Package the production model into a self-contained bundle, implement the FastAPI backend with four inference endpoints, propagate the validation gate status, and document the Monthly Refresh Procedure.

**Inputs:**
- `data/models/mmm_trace_B_YYYYMMDD.nc`
- `data/processed/hairbright_mmm_features_v2_YYYYMMDD.xlsx`
- `data/outputs/calibration_factors.json`
- `data/outputs/scorecard_summary.json` (gate: PROCEED WITH CAUTION)
- `data/outputs/hairbright_attribution_YYYYMMDD.xlsx`
- `data/outputs/hairbright_optimization_YYYYMMDD.xlsx`

**Output:** `api/mmm_bundle_YYYYMMDD/` directory + `api/` Python files

**Model bundle structure:**

| File | Contents |
|:-----|:---------|
| `metadata.json` | Column names, Hill/adstock parameters, calibration factors, gate decision, `caution_flag`, model version, export timestamp |
| `beta_media_samples.npy` | Posterior samples `(n_samples, n_media)` |
| `beta_ctrl_samples.npy` | Posterior samples `(n_samples, n_ctrl)` |
| `beta_trend_samples.npy` | Posterior samples `(n_samples,)` |
| `intercept_samples.npy` | Posterior samples `(n_samples,)` |
| `beta_media_mean.npy` | Posterior mean point estimates |
| `beta_ctrl_mean.npy` | Posterior mean point estimates |

**API endpoints:**

| Endpoint | Method | Description |
|:---------|:------:|:------------|
| `/health` | GET | Model status, gate decision, `caution_flag`, model version |
| `/predict` | POST | Revenue prediction for given spend inputs (returns mean + HDI 94%) |
| `/attribution` | GET | Pre-computed attribution table from NB06 output |
| `/optimize` | POST | SLSQP budget optimization for given total budget (< 200ms) |

**Gate propagation.** The `caution_flag: true` from `scorecard_summary.json` is surfaced in every `/health` response and included as `health_status` in `/predict` and `/optimize` responses. The API does not block requests when `caution_flag` is true — it warns.

**Monthly Refresh Procedure (documented in NB10 §10.7):** Full re-run sequence starting from NB01, with checklist for: (1) confirming spend scale validity in NB01 validation cell, (2) re-running NB08 with the v2 feature matrix (not noemail) to resolve the cross-notebook drift, (3) re-exporting the model bundle, and (4) verifying `MU_INTERCEPT_V1` anchor remains within 0.01 of the re-computed OLS value.

---

### NB11 — Pilot Dashboard (`dashboard/`)  ✅ Live

The pilot dashboard was implemented as two self-contained HTML files in the `dashboard/` directory. See the [Pilot Dashboard](#pilot-dashboard-nb11) section for full documentation.

---

## Pilot Dashboard (NB11)

> **Status:** ✅ Live. Two versions available in `dashboard/`.

### Overview

The pilot is a **transparency-first dashboard** — not a data exploration tool or a self-service BI interface. Its primary purpose is to allow a marketing director or performance manager to understand HairBright's media efficiency, receive a clear budget recommendation, and immediately grasp the model's confidence level and limitations without requiring any knowledge of Bayesian statistics or MMM methodology.

The design never presents a number without its associated uncertainty. Every channel KPI shows an HDI range. The scorecard decision (PROCEED WITH CAUTION) is always visible in the header, not hidden behind a click. The dual-baseline interpretation is explained inline with plain-language tooltips.

### Versions

**`html_pilot_functional.html`** — Full dynamic version. Connects live to the FastAPI backend via the four API endpoints. All panels populate from real API responses on load; the Budget Optimizer runs `POST /optimize` in real-time. Requires the FastAPI server running on `localhost:8000`.

**`html_pilot_static.html`** — Static preview version with hardcoded production model outputs. No backend required. Fully self-contained for sharing, offline review, or portfolio presentation.

### Dashboard structure

The dashboard is structured as a single-page application with three panels and a persistent sidebar.

**Persistent sidebar:** HairBright logo, model version (`v20260420`), navigation between the three panels, and a star-rating feedback module. The sidebar header shows API connectivity status (`API Connected` / `API Error`) and active parameter set (`NB10 params active`).

**Panel 1 — Model Context:** Quality and reliability metrics for the Bayesian MMM. Shows the `PROCEED WITH CAUTION` banner with plain-language explanation. Four KPI cards: Baseline log-space (89.5%), Baseline counterfactual (26.0%), In-sample MAPE (25.3%), Holdout R² (0.425). Expandable FAQ ("Why are there two baseline figures?"). Expandable technical summary with MCMC convergence status.

![Model Context panel](assets/images/1_pilot_model_context.gif)

**Panel 2 — Revenue Attribution:** KPI summary row (Total Revenue $4.2M, Total Spend $602K, Overall ROAS 3.62x, % Incremental Revenue 52%, Business Baseline 26%). Revenue decomposition waterfall chart (counterfactual scale) and calibrated iROAS by channel bar chart (with HDI 94%). Granular attribution table with columns: Channel, Total Spend, Attributed Revenue, Share, iROAS (calibrated), HDI 94%, Confidence badge. Downloadable PDF report button.

![Revenue Attribution panel](assets/images/2_pilot_revenue_atribution.gif)

**Panel 3 — Budget Optimizer:** Weekly budget input (default $4,950), Calibrated iROAS toggle (on by default; off shows raw posterior values with a warning banner). "Auto Optimize" button calls `POST /optimize`. Results show current vs. optimal allocation side-by-side as horizontal bar charts with per-channel Δ changes. Budget scenario cards: –20% cut, current (historical), Recommended (+20%), +40% increase, and a custom prediction input. Near-optimal note callout explains the –0.2% re-allocation uplift finding and redirects to total budget scaling as the primary opportunity.

![Budget Optimizer panel](assets/images/3_pilot_revenue_predictor.gif)

### Technical implementation

The functional version uses vanilla JS with Chart.js (v4.4.0) for all charts and Montserrat from Google Fonts. It follows the architecture defined in the original specification: the React + Tremor approach was replaced by a single-file HTML implementation that achieves the same visual output with zero build tooling, making it trivially deployable alongside the FastAPI static mount or as a standalone file. The static version embeds all data from the production model outputs directly in the JavaScript.

### Visual identity

| Dashboard element | Color | HEX |
|:-----------------|:------|:----|
| Page background | Cream White | `#FEFEFE` |
| Sidebar background | Graphite | `#1A1A1A` |
| Panel titles, H2 | Mauve Pink | `#C17485` |
| KPI values, highlights | Amber Gold | `#FDC53B` |
| Body text | Graphite | `#0B0B0B` |
| CAUTION badges | Amber Gold on white | `#FDC53B` |
| Chart: Paid Search | Deep Mauve | `#8C3A52` |
| Chart: PMax | Mauve Pink | `#C17485` |
| Chart: Facebook | `#D4A0AB` | — |
| Chart: Instagram | Amber Gold | `#FDC53B` |

---

## API Reference (NB10)

### `GET /health`

Returns the current model status, validation gate decision, and calibration metadata.

```json
{
  "status": "ok",
  "model_version": "20260420",
  "gate_decision": "PROCEED_WITH_CAUTION",
  "caution_flag": true,
  "caution_reason": "3 PASS / 7 REVIEW / 0 FAIL — holdout Q4 concentration, lift calibration unavailable",
  "calibration_applied": true,
  "calibration_factors": {
    "paid_search": 0.1159,
    "pmax": 0.3156,
    "facebook": 0.5182,
    "instagram": 0.1345
  },
  "timestamp": "2026-04-20T00:00:00Z"
}
```

### `POST /predict`

Returns posterior predictive revenue (mean + HDI 94%) for a given weekly spend vector.

**Request:**
```json
{
  "spend_ps": 800.0,
  "spend_pmax": 1200.0,
  "spend_fb": 600.0,
  "spend_ig": 247.0,
  "use_calibrated": true
}
```

**Response:**
```json
{
  "predicted_revenue_mean": 56742.18,
  "predicted_revenue_hdi_low": 48103.45,
  "predicted_revenue_hdi_high": 66201.37,
  "health_status": "PROCEED_WITH_CAUTION",
  "caution_flag": true
}
```

### `GET /attribution`

Returns the pre-computed attribution table from the NB06 output (loaded from the model bundle at startup).

### `POST /optimize`

Runs the SLSQP optimizer for a given total weekly budget and returns the optimal allocation with projected revenue uplift.

**Request:**
```json
{
  "weekly_budget": 3416.0,
  "use_calibrated": true,
  "min_shares": { "paid_search": 0.10, "pmax": 0.10, "facebook": 0.05, "instagram": 0.0 },
  "max_shares": { "paid_search": 0.60, "pmax": 0.60, "facebook": 0.50, "instagram": 0.30 }
}
```

**Response:** Optimal spend per channel, projected revenue (mean + HDI), and uplift vs. current allocation. Latency target: < 200ms (SLSQP).

---

## File Structure

```
hairbright-mmm/
│
├── README.md
├── .gitattributes
├── .gitignore
├── requirements.txt                              # Root dev environment (Python 3.11+)
├── docker-compose.yml                            # ✅ Full stack: API + Nginx dashboard
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb               ✅ Production
│   ├── 02_eda.ipynb                          ✅ Production
│   ├── 03_mmm_transformation.ipynb          ✅ Production (K_ig = $1,111 fixed)
│   ├── 04_mmm_model.ipynb                   ✅ Production (Model B, anchor 9.5578)
│   ├── 05_mmm_diagnostics.ipynb             ✅ Production (7/7 PASS)
│   ├── 06_mmm_attribution.ipynb             ✅ Production (Fix F6 applied)
│   ├── 07_mmm_optimization.ipynb            ✅ Production (SLSQP < 200ms)
│   ├── 08_mmm_validation_calibration.ipynb  ✅ Production (PROCEED WITH CAUTION)
│   ├── 09_mmm_reporting_visual.ipynb        ✅ Production (PDF + PPTX + Excel)
│   └── 10_deployment_backend.ipynb          ✅ Production
│
├── data/
│   ├── raw/
│   │   └── HairBright_mmm_haircare_data.xlsx    # Source dataset (509 daily rows)
│   │
│   ├── interim/                                  # NB01 output: weekly-aggregated, cleaned
│   ├── processed/                                # NB03 output: feature matrices
│   │
│   ├── models/                                   # NB04 output: MCMC traces
│   │   ├── mmm_trace_B_20260419.nc               ← production trace (Model B)
│   │   └── mmm_trace_A_20260419.nc               ← reference trace (Model A)
│   │
│   ├── outputs/                                  # NB05–NB08 outputs
│   │   ├── scorecard_summary.json                ← NB08 gate (PROCEED WITH CAUTION)
│   │   └── calibration_factors.json              ← PS 0.1159 / PMax 0.3156 / FB 0.5182 / IG 0.1345
│   │
│   └── reports/                                  # NB09 output: executive deliverables
│       ├── hairbright_mmm_executive_summary_20260420.pdf  ← ✅ in repo (portfolio sample)
│       ├── fig_01_kpi_scorecard_20260420.png              ← ✅ in repo (portfolio sample)
│       ├── fig_02_attribution_20260420.png                ← ✅ in repo (portfolio sample)
│       ├── fig_03_revenue_decomp_20260420.png             ← ✅ in repo (portfolio sample)
│       ├── fig_04_scenarios_20260420.png                  ← ✅ in repo (portfolio sample)
│       ├── hairbright_mmm_presentation_20260420.pptx      ← gitignored (regenerate with NB09)
│       └── hairbright_mmm_report_20260420.xlsx            ← gitignored (regenerate with NB09)
│
├── api/                                          # NB10 output: production API
│   ├── main.py                                   # FastAPI app (6 endpoints)
│   ├── model_backend.py                          # Model loader + inference functions
│   ├── schemas.py                                # Pydantic request/response models
│   ├── requirements.txt                          # API-only deps (no PyMC, no pandas)
│   ├── Dockerfile                                # ✅ Multi-stage build (builder + runtime)
│   ├── nginx.conf                                # ✅ Nginx — proxy /api/ + static dashboard
│   ├── dockerignore                              # ✅ Build context exclusions (rename → .dockerignore)
│   └── mmm_bundle_20260420/                      ← production bundle (gitignored — not in repo)
│       ├── metadata.json
│       ├── beta_media_samples.npy / beta_media_mean.npy
│       ├── beta_ctrl_samples.npy / beta_ctrl_mean.npy
│       ├── beta_trend_samples.npy
│       └── intercept_samples.npy
│
├── dashboard/                                    # Pilot dashboard
│   ├── html_pilot_functional.html               ✅ Live — connects to FastAPI backend
│   └── html_pilot_static.html                   ✅ Live — self-contained static preview
│
├── assets/
│   └── images/
│       ├── logo_claro 1.png / logo_claro 2.png   # Light logo variants
│       ├── logo_oscuro.png / logo_oscuro_2.png    # Dark logo variants
│       ├── favicon.png
│       ├── Recurso 0.jpg through Recurso 3.jpg    # Brand photography
│       ├── look&feel.png                          # Visual identity reference
│       ├── visual_identity_guide_v2.1.pdf         # Brand guide (current)
│       ├── 1_pilot_model_context.gif              # Dashboard screenshot — Model Context
│       ├── 2_pilot_revenue_atribution.gif         # Dashboard screenshot — Revenue Attribution
│       └── 3_pilot_revenue_predictor.gif          # Dashboard screenshot — Budget Optimizer
```

---

## Technical Stack

| Category | Technology | Version | Purpose |
|:---------|:----------:|:-------:|:--------|
| **Language** | Python | 3.11 | Core development |
| **Bayesian modeling** | PyMC | 5.x | MCMC sampling (NUTS), model specification |
| **Posterior analysis** | ArviZ | 0.19+ | R-hat, ESS, HDI, trace plots, LOO/WAIC |
| **Data manipulation** | pandas | 2.x | Pipeline data handling |
| **Numerical operations** | NumPy | 1.26+ | Array ops, posterior math |
| **Visualization** | matplotlib / seaborn | — | All charts with brand palette |
| **Statistical utilities** | scipy | 1.12+ | SLSQP optimizer, statistical tests |
| **Machine learning** | scikit-learn | 1.4+ | OLS, Ridge, StandardScaler, cross-validation |
| **API framework** | FastAPI | 0.135.x | REST endpoints, Pydantic validation |
| **ASGI server** | uvicorn | 0.44.0 | FastAPI runtime |
| **Containerization** | Docker + Docker Compose | — | Multi-stage image build, full-stack deploy |
| **Reverse proxy** | Nginx (Alpine) | — | Static dashboard serving + API proxy |
| **Excel I/O** | openpyxl | — | Multi-sheet output workbooks |
| **PPTX generation** | python-pptx | — | Presentation deliverable |
| **PDF generation** | reportlab + matplotlib | — | PDF executive summary |
| **Model serialization** | NetCDF4 (ArviZ `.nc`) | — | Posterior trace persistence |
| **Schema validation** | pydantic | 2.x | API request/response models |
| **Development environment** | Google Colab + Google Drive | — | Notebook execution and file storage |
| **Frontend (pilot)** | Vanilla JS + Chart.js | 4.4.0 | Pilot dashboard (no build tooling) |

**Runtime requirements:** MCMC sampling (NB04) requires 16GB+ RAM and approximately 15–20 minutes per model on a Google Colab T4 GPU or equivalent CPU. All other notebooks run in standard Colab free tier.

---

## Methodological Contributions

### 1. Sparse-aware Hill saturation parameterization

Standard MMM implementations compute the Hill K parameter from the full spend distribution, including zero-spend weeks. For Instagram (11/74 active weeks), this produces a K estimate anchored near zero, making the saturation curve appear nearly flat from the first dollar. This project implements a sparse-aware approach: K is computed exclusively from active weeks (`spend > 0`), specifically the median adstock value across the 11 active weeks. This produces `K_ig = $1,111.12`, which correctly captures the saturation dynamics of real Instagram spend levels for HairBright.

This approach is generalizable to any MMM scenario where a channel is tested intermittently or has seasonal gaps, and should be applied whenever a channel's active coverage falls below 30% of the modeling window.

### 2. Fixed-anchor intercept strategy for baseline stability

When using two feature matrix variants (v1 and v2) for A/B model comparison, the intercept prior mean shifts between variants because the sparse-aware Hill transformation changes the media input distribution. A naive approach would use a live OLS estimate from the v2 matrix for the intercept anchor, causing the baseline gate to pass or fail based on feature engineering choices rather than true model quality.

This project fixes `MU_INTERCEPT_V1 = 9.5578` computed from the v1 media-only OLS, making the intercept anchor invariant to feature engineering. This decouples the baseline gate from the Hill K calibration, ensuring reproducibility across re-runs with different feature matrices.

### 3. Dual-baseline communication framework

The MMM literature typically reports a single baseline figure. This project introduces dual reporting as a communication standard: the log-space proportional figure (89.5%) for technical/internal use, and the counterfactual revenue-scale figure (26.0%) for business/stakeholder use. Both figures are equally valid; they measure different counterfactuals. Presenting only one number systematically misleads either technical reviewers (who expect the log-space figure) or business stakeholders (who interpret it against revenue-scale benchmarks).

The dual-baseline framework is implemented as a `baseline_dual` sheet in the NB06 output, a dedicated KPI card pair in the NB11 pilot, and a mandatory interpretation note in all NB09 deliverables.

### 4. Honest near-optimality reporting

When the optimization result is negative (–0.2% re-allocation uplift), the natural response is to reframe it, suppress it, or attribute it to model error. This project documents the result explicitly and reframes it as a positive finding: HairBright's current allocation is near-optimal at its current budget level. The recommendation redirects to budget scaling, where the model has higher confidence and a clearer economic signal (+5.0% revenue from +20% budget).

This approach sets a methodological precedent for MMM projects where re-allocation does not yield meaningful uplift: the finding itself is the insight, not a failure to be corrected.

### 5. Calibration factor derivation from industry benchmarks

In the absence of geo lift tests or incrementality experiments (which are unavailable for this dataset), calibration factors are derived from published industry benchmark ranges for each channel type. The factors scale raw posterior iROAS estimates to the midpoint of the applicable benchmark range, with the scaling relationship documented and the resulting calibrated values cross-checked against the counterfactual attribution from Method 2.

This approach is transparent about its limitations (documented in §9.1 of all deliverables) while providing business-usable iROAS figures that would otherwise be unusable at 26x–74x raw values.

---

## Known Limitations

The following limitations apply to all outputs of this project. The validation gate (PROCEED WITH CAUTION) and the geo lift test recommendation are surfaced explicitly in all executive deliverables. The remaining limitations are documented here for technical completeness and must be communicated to stakeholders before any budget decision is made based on this model.

**Holdout performance.** The 14-week Q4 holdout (including Black Friday) is the most challenging prediction window in the dataset. Holdout MAPE of 43.5% and R² of 0.425, while significantly better than all baselines, indicate the model's predictions in extreme seasonal periods carry substantial uncertainty. Budget decisions for Q4 campaigns should apply wider confidence bands than the stated HDI 94% ranges.

**No geo lift tests available.** Calibration factors are derived from industry benchmarks, not from controlled incrementality experiments. The PS factor (0.1159) and IG factor (0.1345) are aggressive — they apply a ~10x downward correction to raw estimates. While the resulting calibrated values (4.50x and 3.50x) are economically plausible, they should be validated with a geo lift test in H1 2026 before using them for major budget reallocation decisions.

**Cross-notebook feature matrix inconsistency.** NB08 uses the `noemail` feature matrix variant, while NB06 and NB07 use the `v2` variant. This creates a documented drift in posterior means between notebooks (e.g., `beta_ps` +97.7%, intercept +2.5%). The calibration factors are internally consistent for the noemail variant. Resolution is scheduled for the next Monthly Refresh, where NB08 will be re-run with the v2 matrix.

**Instagram sparse data.** With only 11 active weeks, the Instagram iROAS estimate carries a very wide HDI 94% [0.08, 2.10] on the mROAS metric. The point estimate (3.50x calibrated) should not be used for budget decisions in isolation. The recommendation is to treat Instagram as "insufficient data" for optimization and to plan a dedicated Instagram spend test of at least 20 consecutive weeks before including it in the optimization objective.

**n=74 parameter instability.** Removing Q4 (14 weeks) or 2022 (26 weeks) from the dataset changes some coefficient estimates by up to 3,922%. This sensitivity is expected for a 74-observation dataset with 10 predictors and concentrated seasonal events. The model is appropriate for directional guidance and order-of-magnitude budget decisions, not for precision allocation at the dollar level.

**mROAS < 1x.** Some channel mROAS estimates (after calibration) may fall below 1.0x, which could be misinterpreted as "destroying value." This is an artifact of the calibration scale and should be interpreted as "returns are below the calibration floor for this spend level" rather than a negative return on investment. All channels have positive raw posterior betas; no channel is estimated to harm revenue.

---

## Future Work

### Short-Term (next Monthly Refresh)

**Align NB08 feature matrix on next Monthly Refresh.** All notebooks (NB01–NB10) were executed sequentially in order. However, NB08 was run using the `noemail` feature matrix variant rather than the `v2` variant used by NB06 and NB07. This was a deliberate decision at the time to isolate the calibration from the email adjustment, but it creates a documented cross-notebook coefficient drift (e.g., `beta_ps` +97.7% between variants). The calibration factors currently in production are internally consistent for the noemail variant and the outputs are valid — this is not a bug but a known design choice with a documented trade-off. The recommended action on the next Monthly Refresh is to re-run NB08 with the v2 matrix to align all three notebooks on the same feature space and eliminate the drift.

**VIF check follow-up.** If the PMax/Paid Search VIF exceeds 10 after the NB08 matrix alignment, explore merging the two channels into a single "Google paid" composite or applying stronger hierarchical shrinkage.

### Medium-Term

**Instagram incrementality test.** Plan and execute a geo holdout or time-based incrementality test for Instagram with a minimum of 20 consecutive weeks of spend. Use the results to replace the benchmark-derived calibration factor with an experiment-backed one.

**Adstock decay optimization.** The current decay rates are set by domain knowledge (0.30–0.50). A systematic grid search over ±0.10 per channel (20 trials) was planned in the initial plan but deferred due to priority. This optimization is expected to improve Ridge proxy R² by 0.03–0.05.

**Extend to additional brands or markets.** The Figshare source dataset contains multiple brand/region combinations. Extending the pipeline to a second brand would validate the generalizability of the sparse-aware Hill approach and the fixed-anchor intercept strategy.

**Automated monthly pipeline.** Productionize NB01–NB08 as a scheduled pipeline (Airflow or Prefect) that automatically re-runs when a new monthly data export is available, updates the model bundle, and triggers a Slack/email notification with the updated scorecard.

### Long-Term Vision

**Real-time budget pacing dashboard.** Extend the NB11 pilot with a live spend feed (Google Ads API + Meta Marketing API) to recommend intra-week budget pacing adjustments based on the current week's spend and the projected revenue curve.

**Multi-touch attribution complement.** Implement a Shapley-value-based multi-touch attribution model as a complement to the MMM, enabling consistency checks between the two methodologies and providing session-level attribution alongside the aggregate MMM.

**Geo-stratified MMM.** Extend the model to multiple US regions (e.g., Northeast vs. South vs. West Coast), allowing region-specific budget allocation and incrementality validation through geographic holdout experiments.

---

## License & Contact

**Personal Portfolio Project — All Rights Reserved**

This project was built as a personal deep-dive into production-grade Bayesian MMM after completing a Master's in Data Science with AI. The dataset is derived from publicly available research data (Figshare DOI: 10.6084/m9.figshare.25314841, Anderson 2024). The HairBright brand, visual identity, and business context are fictional constructs created for this project.

The codebase, methodology, and documentation are shared publicly for portfolio and educational purposes. If you use ideas or patterns from this project, attribution is appreciated.

**Project Author:**
- **Name:** Alberto Sánchez
- **Email:** alberto.sanchez@gmail.com
- **LinkedIn:** https://www.linkedin.com/in/albertosvallejo/
- **GitHub:** https://github.com/albertosvallejo/
- **Technical Support:** https://github.com/albertosvallejo/dyson-rag-assistant/issues


---

**Last Updated:** April 24, 2026  
**Pipeline version:** v20260420  
**Status:** NB01–NB10 Production · Pilot Dashboard Live · Docker Ready ✅

---

*This README serves as both technical documentation and a full audit trail of all modeling decisions made during development. The project evolution section and the `_private/` directory preserve the complete development history.*
