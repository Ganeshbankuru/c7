"""Ollama client module for local LLM inference.

To test this script, start Ollama locally and use the default local URL.
Typical local URL: http://localhost:11434
If Ollama is running on another host or port, update the URL accordingly.
"""
import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, url: str, model: str, timeout: int = 30) -> None:
        self.url = url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def generate_response(self, prompt: str) -> Optional[str]:
        payload = {"model": self.model, "prompt": prompt, "stream": False}
        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            if isinstance(data, dict):
                return data.get("response") or data.get("text") or ""
            return ""
        except Exception as error:
            logger.error("Ollama request failed: %s", error)
            return None


def main() -> None:
    # Replace the URL below with your Ollama server URL if needed.
    # Default local Ollama URL: http://localhost:11434
    # If you are running Ollama on a custom host/port, use that URL instead.
    client = OllamaClient(url="http://localhost:11434", model="gemma3:1b")
    prompt = "what is openclaw,claude code,opencode in ollama means,give the response in a short paragraph."
    response = client.generate_response(prompt)

    if response is None:
        print("Request failed. Check the Ollama server URL and logs.")
    elif response == "":
        print("No response returned from Ollama.")
    else:
        print("Generated response:")
        print(response)


if __name__ == "__main__":
    main()

