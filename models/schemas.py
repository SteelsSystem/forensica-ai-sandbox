from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class UniversalAnalysisInput(BaseModel):
    input_a: str = Field(..., description="Institutional/authority text or Dataset A")
    input_b: str = Field(..., description="Subject/respondent text or Dataset B")
    domain: str = Field("forensic-legal", description="Domain ID from DomainRegistry")
    language: str = Field("en", description="ISO 639-1 language code")
    case_id: Optional[str] = Field(default_factory=lambda: f"CASE-{uuid.uuid4().hex[:8].upper()}")
    raw_data: Optional[str] = Field(None, description="Raw data blob for raw-data domain")
    enable_pii_redaction: bool = True
    thinking_level: str = Field("HIGH", pattern="^(LOW|MEDIUM|HIGH)$")

class AnalysisPhaseResult(BaseModel):
    phase: str; findings: list[str] = []; axioms_triggered: list[str] = []
    confidence: float = 0.0; raw_output: str = ""

class AnalysisResponse(BaseModel):
    case_id: str; domain: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    mind1: AnalysisPhaseResult; deep1: AnalysisPhaseResult
    loopcycle: dict[str, Any] = {}; defense: AnalysisPhaseResult
    risk_score: float = 0.0; flagged_axioms: list[str] = []; pii_redacted: bool = False

class SandboxClassifyInput(BaseModel):
    payload: str; context: Optional[str] = None

class SandboxClassifyResponse(BaseModel):
    allowed: bool; threat_score: float; threat_type: Optional[str]
    blocking_layer: Optional[int]; reason: str

class ParaframeDecodeInput(BaseModel): text: str

class ParaframeDecodeResponse(BaseModel):
    phrases_detected: list[dict[str, str]]; decoded_intent: str; manipulation_score: float

class DomainRegisterInput(BaseModel):
    id: str; label: str; description: str = ""; axiom_set: list[str] = []; prompt_extra: str = ""

class HealthResponse(BaseModel):
    status: str; version: str = "2.0.0"; providers: dict[str, str] = {}; domains_loaded: int = 0
