from src.ai_agent.response import Response
from src.ai_agent.step import Step


class Trajectory:

    def __init__(self) -> None:
        self.runs: list[dict] = []

    def initialize(self, query: str) -> None:
        """register a new run with a given query"""
        self.runs.append({"query": query, "steps": []})

    def add(self, response: Response, obeservation: str | None = None) -> None:

        """record a step in the Response and optionally an observation"""
        step = Step(
            thought=response.reasoning or "",
            metadata=response.metadata,
        )

        if obeservation is not None:
            step.action = response.tool_call
            step.observation = obeservation
        else:
            step.answer = response.content

        self.runs[-1]["steps"].append(step)

