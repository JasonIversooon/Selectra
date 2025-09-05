from enum import Enum
from pydantic import BaseModel


class Action(str, Enum):
    summarize = "summarize"
    explain_layman = "explain_layman"
    explain_detailed = "explain_detailed"
    sentiment = "sentiment"
    find_sources = "find_sources"


class AnalyzeRequest(BaseModel):
    text: str
    action: Action


class AnalyzeResponse(BaseModel):
    status: str
    result: str
