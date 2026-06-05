from fastapi import APIRouter
from models.schemas import ParaframeDecodeInput, ParaframeDecodeResponse
from nlp.forensic_nlp import ForensicNLP

router = APIRouter()

@router.post("/paraframe/decode", response_model=ParaframeDecodeResponse)
async def decode(req: ParaframeDecodeInput):
    nlp = ForensicNLP()
    phrases = nlp.decode_paraframe(req.text)
    return ParaframeDecodeResponse(
        phrases_detected=phrases,
        decoded_intent="; ".join(p["decoded"] for p in phrases) if phrases else "No institutional encoding detected.",
        manipulation_score=nlp.manipulation_score(phrases))
