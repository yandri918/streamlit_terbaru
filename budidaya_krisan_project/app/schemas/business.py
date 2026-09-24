"""Business analysis schemas"""
from pydantic import BaseModel
from typing import Optional


class BusinessSummary(BaseModel):
    total_batches: int
    total_revenue: int
    total_cost: int
    total_profit: int
    avg_roi_pct: float
    best_variety: Optional[str]
    best_roi_pct: float
