from fastapi import APIRouter, HTTPException
from ..models.schemas import AnalyzeRequest, AnalyzeResponse
from ..services.analyze_service import analyze_text

router = APIRouter()


@router.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest):
    if not (req.text or "").strip():
        raise HTTPException(status_code=400, detail="text is required")

    try:
        result = await analyze_text(req.text, req.action)
        return AnalyzeResponse(status="ok", result=result.strip())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
