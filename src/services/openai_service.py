import os
import hashlib
from typing import List
from pathlib import Path

from pydantic import BaseModel
import requests
from openai import OpenAI
from io import BytesIO
import base64
import httpx as _httpx
from schemas.openai_input import OpenAiPdfInput, OpenAiCompletion, OpenAiCompletionCustomCoT
import json

# Global variables
GPT4_VISION_MODEL = "gpt-4.1"


# Создаём свой класс исключений
class CustomHTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")

def getClient(key, proxy_url=None):
    proxy_url = os.getenv("PROXY_URL")
    print(f"Proxy URL: {proxy_url}")
    _http_client = _httpx.Client(proxy=proxy_url) if proxy_url else None
    client = OpenAI(
        api_key=key,
        http_client=_http_client
    )
    return client


def open_ai_completion(input: OpenAiCompletion):
    try:
        client = getClient(key=input.key)
        print("open_ai_completion")

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": input.text
                }
            ],
        )

        return {
            "text": response.output_text
        }

    except CustomHTTPException as custom_exc:
        print(f"An unexpected error occurred: {str(e)}")
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