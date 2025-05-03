import os
import hashlib
from typing import List
from pathlib import Path

from pydantic import BaseModel
import requests
from openai import OpenAI, AsyncOpenAI
from io import BytesIO
import base64
import httpx as _httpx
from propertium.schemas.openai_schemas import OpenAiCompletion
import json

from dotenv import load_dotenv

load_dotenv()

# Global variables
GPT4_VISION_MODEL = "gpt-4.1"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class CustomHTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


def getClient(key: str, proxy_url: str | None = None) -> AsyncOpenAI:
    proxy_url = os.getenv("PROXY_URL")
    print(f"Proxy URL: {proxy_url}")
    _http_client = _httpx.Client(proxy=proxy_url) if proxy_url else None
    client = AsyncOpenAI(
        api_key=key,
        http_client=_http_client
    )
    return client


async def completions(input: OpenAiCompletion) -> str:
    try:
        client = getClient(key=OPENAI_API_KEY)
        print("open_ai_completion")

        response = await client.chat.completions.create(
            model=GPT4_VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": input.text
                }
            ],
        )

        return response.outputs[0].text

    except CustomHTTPException as custom_exc:
        print(f"An unexpected error occurred: {str(custom_exc)}")
        return {
            "status_code": custom_exc.status_code,
            "detail": custom_exc.detail
        }
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return {
            "status_code": 500,
            "detail": f"An unexpected error occurred: {str(e)}"
        }
