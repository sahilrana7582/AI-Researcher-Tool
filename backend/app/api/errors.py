import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.ai.exceptions import LLMError
from app.schemas.error import ErrorResponse

logger = logging.getLogger(__name__)

LLM_FAILURE_MESSAGE = "The language model provider failed. Please try again later."


def log_llm_error(request: Request, exc: LLMError) -> None:
    # The only place an LLMError is logged. The traceback includes the original
    # provider exception via `raise ... from`, but the client never sees it.
    logger.error(
        "LLM provider failure on %s %s",
        request.method,
        request.url.path,
        exc_info=exc,
    )


async def llm_error_handler(request: Request, exc: LLMError) -> JSONResponse:
    log_llm_error(request, exc)
    return JSONResponse(
        status_code=502,
        content=ErrorResponse(detail=LLM_FAILURE_MESSAGE).model_dump(),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(LLMError, llm_error_handler)
