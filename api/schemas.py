"""Pydantic schemas for the HairBright MMM API."""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


# ── Shared spend model ─────────────────────────────────────────────────────────
class SpendInput(BaseModel):
    spend_ps:   float = Field(..., ge=0, description="Paid Search weekly spend (USD)")
    spend_pmax: float = Field(..., ge=0, description="Performance Max weekly spend (USD)")
    spend_fb:   float = Field(..., ge=0, description="Facebook weekly spend (USD)")
    spend_ig:   float = Field(..., ge=0, description="Instagram weekly spend (USD)")


# ── /predict ──────────────────────────────────────────────────────────────────
class PredictRequest(SpendInput):
    hdi_prob: Optional[float] = Field(0.94, ge=0.5, le=0.99, description="HDI probability (default 94%)")

class PredictResponse(BaseModel):
    revenue_mean:   float
    revenue_median: float
    revenue_ci_lo:  float
    revenue_ci_hi:  float
    ci_prob:        float
    total_spend:    float
    roas_mean:      float
    health_status:  str
    caution_flag:   bool
    warnings:       list[str]


# ── /attribution ─────────────────────────────────────────────────────────────
class AttributionRequest(SpendInput):
    pass

class ChannelAttribution(BaseModel):
    share_pct:        float
    rev_attr_usd:     float
    spend_usd:        float
    roas_raw:         float
    roas_calibrated:  float
    cal_factor:       float

class AttributionResponse(BaseModel):
    baseline_share_pct: float
    controls_share_pct: float
    channels:           dict[str, ChannelAttribution]
    total_spend:        float
    health_status:      str
    caution_flag:       bool


# ── /optimize ────────────────────────────────────────────────────────────────
class OptimizeRequest(BaseModel):
    total_budget:         float = Field(..., gt=0, description="Total weekly budget in USD")
    min_share:            Optional[float] = Field(0.05, ge=0.0, le=0.5)
    max_share:            Optional[float] = Field(0.60, ge=0.1, le=1.0)
    method:               Optional[str]   = Field("SLSQP", description="SLSQP or DE")
    hdi_prob:             Optional[float] = Field(0.94, ge=0.5, le=0.99)
    use_calibrated_iroas: Optional[bool]  = Field(True, description="Use calibrated iROAS for optimisation (True) or raw posterior (False)")

class ChannelAllocation(BaseModel):
    spend_usd: float
    share_pct: float

class OptimizeResponse(BaseModel):
    total_budget:           float
    method:                 str
    converged:              bool
    optimal_allocation:     dict[str, ChannelAllocation]
    revenue_optimal_mean:   float
    revenue_optimal_hdi_lo: float
    revenue_optimal_hdi_hi: float
    roas_optimal:           float
    revenue_equal_mean:     float
    uplift_vs_equal_pct:    float
    health_status:          str
    caution_flag:           bool


# ── /scenario ────────────────────────────────────────────────────────────────
class ScenarioItem(SpendInput):
    name: str = Field(..., description="Scenario label")

class ScenarioRequest(BaseModel):
    scenarios: list[ScenarioItem]
    hdi_prob:  Optional[float] = Field(0.94, ge=0.5, le=0.99)

class ScenarioResult(BaseModel):
    name:           str
    spend:          dict[str, float]
    total_spend:    float
    revenue_mean:   float
    revenue_ci_lo:  float
    revenue_ci_hi:  float
    roas_mean:      float

class ScenarioResponse(BaseModel):
    results:      list[ScenarioResult]
    health_status: str
    caution_flag:  bool
