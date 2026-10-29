from dataclasses import dataclass

@dataclass
class Response:

    """The response from LLM calls."""

    content: str = ""
    reasoning : str | None = None
    tool_call: dict | None = None
    metadata: dict | None = None