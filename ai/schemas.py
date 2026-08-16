from typing import Literal
from pydantic import BaseModel, Field


class CropAnalysis(BaseModel):
    crop_name: str = Field(description="Apparent crop name, or 'Unknown'")
    image_quality: Literal["good", "fair", "poor"] = "good"
    assessment_status: Literal[
        "healthy_looking",
        "possible_issue",
        "significant_symptoms",
        "insufficient_evidence",
        "not_a_plant",
    ]
    possible_issue: str = Field(description="Most likely visible issue, or 'No obvious issue detected'")
    confidence: int = Field(ge=0, le=100)
    severity: Literal["low", "moderate", "high", "not_assessable"]
    observed_symptoms: list[str] = Field(default_factory=list)
    immediate_actions: list[str] = Field(default_factory=list)
    prevention_steps: list[str] = Field(default_factory=list)
    expert_help_recommended: bool = False
    expert_help_reason: str = ""
    farmer_summary: str = ""
    farmer_summary_hindi: str = ""
    immediate_actions_hindi: list[str] = Field(default_factory=list)
    prevention_steps_hindi: list[str] = Field(default_factory=list)
    demo_mode: bool = False
