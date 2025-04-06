import sys
from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field


class GreetingInput(BaseModel):
    message: str


class GreetingOutput(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    input_message: str
    greeting: str
    python_version: str = Field(default=sys.version)
    status: str = "success"
    error_message: Union[str, None] = None
