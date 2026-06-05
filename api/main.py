from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings
from core.llm_provider import ProviderRegistry
from domains.registry import DomainRegistry
from pipeline.engine import UniversalAnalysisEngine
from sandbox.security_engine import SandboxSecurityEngine
from nlp.forensic_nlp import ForensicNLP
from api.routers import analyze, domains, sandbox, paraframe, admin, health

@asynccontextmanager
async def lifespan(app: FastAPI):
    ProviderRegistry()          # S1
    DomainRegistry()            # S2
    UniversalAnalysisEngine()   # S3
    SandboxSecurityEngine()     # S4
    ForensicNLP()               # S5
    yield

app = FastAPI(title="Forensica AI Sandbox", version="2.0.0",
    description="Modular AI Debugging Sandbox — 9 built-in domains, EU-sovereign LLM.",
    lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(analyze.router, prefix="/api/v1", tags=["Analysis"])
app.include_router(domains.router, prefix="/api/v1", tags=["Domains"])
app.include_router(sandbox.router, prefix="/api/v1", tags=["Sandbox"])
app.include_router(paraframe.router, prefix="/api/v1", tags=["PARAFRAME"])
app.include_router(admin.router, prefix="/api/v1/admin", tags=["Admin"])
