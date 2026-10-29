import json
import urllib.request
from src.ai_agent.response import Response


class LLM:
    def __init__(self,
        model: str,
        base_url: str = "http://localhost:11434/v1",
        api_key: str = "your-api-key",
        think: bool = False
    ):

        """Initialize the LLM with given model."""
        self.model = model
        self.base_url = base_url
        self.api_key = api_key
        self.think = think

    def generate(self, messages: list[dict], tools: list | None = None,) -> Response:

        """Generate a response from the LLM given a list of messages."""

        # Build the request body
        body = {
            "model": self.model,
            "messages": messages,
        }

        # tools and reasoning effort
        if tools:
            body["tools"] = tools
        if not self.think:
            body["reasoning_effort"] = "none"

        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
        )

        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read())

        #Extract the response from the data

        message = data["choices"][0]["message"]
        tool_calls = message.get("tool_calls")
        tool_call = tool_calls[0] if tool_calls else None
        meta_data = {
            "model": data["model"],
            "prompt_token": data["usage"]["prompt_tokens"],
            "completion_token": data["usage"]["completion_tokens"]
        }

        return Response(
            content=message.get("content"),
            reasoning=message.get("reasoning"),
            tool_call=tool_call,
            metadata=meta_data,
        )


if __name__ == "__main__":
    llm = LLM(model="gemma4:e4b")
    response = llm.generate(messages=[{"role": "user", "content": "tell me a joke?"}])
    print(response.content)
