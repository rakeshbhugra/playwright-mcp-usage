from pydantic import BaseModel
from typing import Optional, Any
from langgraph.config import StreamWriter
from mcp import ClientSession

class State(BaseModel):
    messages: list[Any]
    session: Optional[ClientSession] = None
    writer: Optional[StreamWriter] = None
    openai_tool: Optional[Any] = None
    openai_tools: Optional[list[Any]] = None  # Support for multiple tool calls
    next_node: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True