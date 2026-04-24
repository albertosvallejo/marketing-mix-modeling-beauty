"""
main.py
HairBright MMM — FastAPI application.

Run locally:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

Endpoints:
    GET  /health           → API liveness + model gate status (caution_flag)
    GET  /model/info       → Model metadata (includes calibration factors)
    POST /predict          → Revenue prediction with 94% HDI
    POST /attribution      → Channel attribution (raw + calibrated iROAS)
    POST /optimize         → Budget allocation optimisation (SLSQP / DE)
    POST /scenario         → What-if scenario simulation
"""
from __future__ import annotations
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import (
    PredictRequest, PredictResponse,
    AttributionRequest, AttributionResponse,
    OptimizeRequest, OptimizeResponse,
    ScenarioRequest, ScenarioResponse, ScenarioResult,
)
import model_backend as backend

# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(
    title       = "HairBright MMM API",
    description = (
        "Marketing Mix Modelling — revenue prediction, attribution, "
        "optimisation and scenario simulation. "
        "All inference responses include health_status and caution_flag "
        "reflecting the nb08 validation decision."
    ),
    version     = "1.0.0",
    docs_url    = "/docs",
    redoc_url   = "/redoc",
)

# ── CORS ─────────────────────────────────────────────────────────────────────
# "null" is required when the HTML is opened as a local file (file://)
# because browsers send Origin: null in that case.
app.add_middleware(
    CORSMiddleware,
    allow_origins     = ["*", "null"],
    allow_credentials = False,
    allow_methods     = ["*"],
    allow_headers     = ["*"],
)


# ── GET /health ───────────────────────────────────────────────────────────────
@app.get("/health", tags=["monitoring"])
def health():
    """
    Liveness check — returns API status, bundle info and model gate decision.

    `caution_flag: true` means the model was deployed with PROCEED WITH CAUTION
    status from nb08 validation. All inference endpoints remain fully operational;
    consumers should display this flag in any UI or dashboard context.
    """
    return {
        "status"        : "ok",
        "model"         : backend.META["model_name"],
        "bundle_date"   : backend.META["export_date"],
        "n_samples"     : int(backend.bm_bundle.shape[0]),
        "health_status" : backend.GATE_DECISION,
        "caution_flag"  : backend.CAUTION_FLAG,
        "warnings"      : backend.GATE_WARNINGS,
    }


# ── GET /model/info ───────────────────────────────────────────────────────────
@app.get("/model/info", tags=["monitoring"])
def model_info():
    """Return full model metadata from the bundle, including calibration factors."""
    return backend.META


# ── POST /predict ─────────────────────────────────────────────────────────────
@app.post("/predict", response_model=PredictResponse, tags=["inference"])
def predict(req: PredictRequest):
    """
    Predict weekly revenue (USD) for a given media spend allocation.

    Returns posterior mean, median, 94% HDI, ROAS and model gate status.
    """
    try:
        spend = {"spend_ps": req.spend_ps, "spend_pmax": req.spend_pmax,
                 "spend_fb": req.spend_fb, "spend_ig":   req.spend_ig}
        return backend.predict_revenue(spend, ci_prob=req.hdi_prob)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── POST /attribution ─────────────────────────────────────────────────────────
@app.post("/attribution", response_model=AttributionResponse, tags=["inference"])
def attribution_endpoint(req: AttributionRequest):
    """
    Decompose predicted revenue into channel contributions (proportional log-linear).

    Returns baseline, controls and per-channel share (%), attributed revenue (USD),
    raw iROAS, calibrated iROAS and the calibration factor applied.
    """
    try:
        spend = {"spend_ps": req.spend_ps, "spend_pmax": req.spend_pmax,
                 "spend_fb": req.spend_fb, "spend_ig":   req.spend_ig}
        return backend.attribution(spend)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── POST /optimize ────────────────────────────────────────────────────────────
@app.post("/optimize", response_model=OptimizeResponse, tags=["inference"])
def optimize_endpoint(req: OptimizeRequest):
    """
    Find the budget allocation that maximises predicted revenue
    given a total weekly spend.

    Supports SLSQP (fast, ~50 ms) and DE (global search, ~500 ms).
    At the historical budget of ~$4,382/week the current mix is already
    near the mROAS optimum; the +20% budget scenario (+5% revenue) is the
    recommended path to meaningful uplift.
    """
    try:
        return backend.optimize_budget(
            total_budget         =req.total_budget,
            method               =req.method,
            min_share            =req.min_share,
            max_share            =req.max_share,
            hdi_prob             =req.hdi_prob,
            use_calibrated_iroas =req.use_calibrated_iroas,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── POST /scenario ────────────────────────────────────────────────────────────
@app.post("/scenario", response_model=ScenarioResponse, tags=["inference"])
def scenario_endpoint(req: ScenarioRequest):
    """
    Simulate multiple spend scenarios and return predicted revenue for each.

    Useful for comparing the historical mix, the SLSQP optimum and the
    +20% budget scenario side-by-side.
    """
    try:
        sc_list = [s.model_dump() for s in req.scenarios]
        results = backend.scenario(sc_list, hdi_prob=req.hdi_prob)
        return ScenarioResponse(
            results      =[ScenarioResult(**r) for r in results],
            health_status=backend.GATE_DECISION,
            caution_flag =backend.CAUTION_FLAG,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
