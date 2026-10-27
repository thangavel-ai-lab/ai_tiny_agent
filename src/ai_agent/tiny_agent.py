import json
import urllib.request

# preparing the request
json_data = json.dumps(
    {
        "model": "gemma4:e4b",
        "messages": [{
            "role": "user",
            "content": "How to create hello world program in python?, Give me step by step guide"}],
        "stream": False
    }
).encode("utf-8")

# post request
req = urllib.request.Request("http://localhost:11434/api/chat",
                             data=json_data,
                             headers={"Content-Type": "application/json"})

# parse response
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode("utf-8"))

print(data["message"]["content"])
