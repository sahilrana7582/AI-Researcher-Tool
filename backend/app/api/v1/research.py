from fastapi import APIRouter

from app.api.dependencies import ResearchServiceDep
from app.schemas.error import ErrorResponse
from app.schemas.research import ResearchRequest, ResearchResponse

router = APIRouter(prefix="/research", tags=["research"])


@router.post(
    "",
    response_model=ResearchResponse,
    summary="Answer a research question",
    responses={502: {"model": ErrorResponse, "description": "LLM provider failed"}},
)
async def research(
    payload: ResearchRequest,
    service: ResearchServiceDep,
) -> ResearchResponse:
    answer = await service.research(payload.query)
    return ResearchResponse(answer=answer)
