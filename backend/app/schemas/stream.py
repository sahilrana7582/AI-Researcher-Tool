from enum import StrEnum

from pydantic import BaseModel


class ResearchEvent(StrEnum):
    TOKEN = "token"
    DONE = "done"
    ERROR = "error"


class TokenEvent(BaseModel):
    text: str


class ErrorEvent(BaseModel):
    detail: str