from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    country: str = Field(..., min_length=1)
    year: int = Field(..., ge=1900, le=2100)
    population: Optional[float] = Field(None, ge=0)
    gdp: Optional[float] = Field(None, ge=0)
    cement_co2: Optional[float] = Field(None, ge=0)
    coal_co2: Optional[float] = Field(None, ge=0)
    oil_co2: Optional[float] = Field(None, ge=0)
    gas_co2: Optional[float] = Field(None, ge=0)
    flaring_co2: Optional[float] = Field(None, ge=0)


class PredictionResponse(BaseModel):
    predicted_co2: float
    unit: str
    baseline_co2: Optional[float] = None
    comparison_vs_baseline_pct: Optional[float] = None
    recommendations: list[str]
