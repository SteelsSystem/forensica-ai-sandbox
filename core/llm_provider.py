from __future__ import annotations
import abc, logging
from enum import Enum
from typing import Any
import httpx
from mistralai import Mistral
from config.settings import settings

logger = logging.getLogger(__name__)

class PipelinePhase(str, Enum):
    MIND1="mind1"; DEEP1="deep1"; DEFENSE="defense"; SANDBOX="sandbox"; ASSISTANT="assistant"

PHASE_CONFIGS: dict[PipelinePhase, dict[str, Any]] = {
    PipelinePhase.MIND1:     {"model": settings.mistral_model_fast, "temperature": 0.1,  "max_tokens": 4096},
    PipelinePhase.DEEP1:     {"model": settings.mistral_model_deep, "temperature": 0.3,  "max_tokens": 8192},
    PipelinePhase.DEFENSE:   {"model": settings.mistral_model_deep, "temperature": 0.3,  "max_tokens": 8192},
    PipelinePhase.SANDBOX:   {"model": settings.mistral_model_fast, "temperature": 0.0,  "max_tokens": 1024},
    PipelinePhase.ASSISTANT: {"model": settings.mistral_model_fast, "temperature": 0.7,  "max_tokens": 2048},
}

class LLMProvider(abc.ABC):
    @abc.abstractmethod
    async def complete(self, messages: list[dict], phase: PipelinePhase) -> str: ...

class MistralProvider(LLMProvider):
    def __init__(self): self._c = Mistral(api_key=settings.mistral_api_key)
    async def complete(self, messages, phase):
        cfg = PHASE_CONFIGS[phase]
        r = await self._c.chat.complete_async(model=cfg["model"], messages=messages,
            temperature=cfg["temperature"], max_tokens=cfg["max_tokens"])
        return r.choices[0].message.content or ""

class ScalewayProvider(LLMProvider):
    def __init__(self): self._ep=settings.scaleway_inference_endpoint; self._k=settings.scaleway_secret_key
    async def complete(self, messages, phase):
        cfg = PHASE_CONFIGS[phase]
        async with httpx.AsyncClient() as c:
            r = await c.post(f"{self._ep}/chat/completions",
                headers={"Authorization": f"Bearer {self._k}"},
                json={"model": cfg["model"], "messages": messages,
                      "temperature": cfg["temperature"], "max_tokens": cfg["max_tokens"]}, timeout=120)
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]

class ProviderRegistry:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._primary = MistralProvider()
            cls._instance._fallback = ScalewayProvider()
        return cls._instance
    async def complete(self, messages: list[dict], phase: PipelinePhase) -> str:
        try: return await self._primary.complete(messages, phase)
        except Exception as e:
            logger.warning("Primary LLM failed: %s", e)
            return await self._fallback.complete(messages, phase)
