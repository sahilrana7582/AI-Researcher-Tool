from collections.abc import AsyncIterable

from fastapi import APIRouter, Request
from fastapi.sse import EventSourceResponse, ServerSentEvent

from app.ai.exceptions import LLMError
from app.api.dependencies import ResearchServiceDep
from app.api.errors import LLM_FAILURE_MESSAGE, log_llm_error
from app.schemas.error import ErrorResponse
from app.schemas.research import ResearchRequest, ResearchResponse
from app.schemas.stream import ErrorEvent, ResearchEvent, TokenEvent

router = APIRouter(prefix="/research", tags=["research"])


@router.post(
    "",
    response_model=ResearchResponse,
    summary="Answer a research question",
    responses={
        502: {
            "model": ErrorResponse,
            "description": "LLM provider failed",
        }
    },
)
async def research(
    payload: ResearchRequest,
    service: ResearchServiceDep,
) -> ResearchResponse:
    answer = await service.research(payload.query)
    return ResearchResponse(answer=answer)


@router.post(
    "/stream",
    response_class=EventSourceResponse,
    summary="Stream an answer to a research question",
)
async def research_stream(
    request: Request,
    payload: ResearchRequest,
    service: ResearchServiceDep,
) -> AsyncIterable[ServerSentEvent]:
    # This function must itself be the generator (it contains `yield`):
    # FastAPI iterates its result to produce the event stream.
    # Once streaming starts the HTTP status is already 200, so provider
    # failures are reported in-band as an `error` event.
    try:
        async for chunk in service.research_stream(payload.query):
            yield ServerSentEvent(
                event=ResearchEvent.TOKEN,
                data=TokenEvent(text=chunk),
            )
    except LLMError as exc:
        log_llm_error(request, exc)
        yield ServerSentEvent(
            event=ResearchEvent.ERROR,
            data=ErrorEvent(detail=LLM_FAILURE_MESSAGE),
        )
        return

    yield ServerSentEvent(event=ResearchEvent.DONE, data={})
