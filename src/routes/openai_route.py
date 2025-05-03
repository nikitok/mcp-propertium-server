from fastapi import APIRouter

from schemas.openai_input import OpenAiCompletion
from services.openai_service import open_ai_completion

router = APIRouter()

@router.post("/text/")
def text(input: OpenAiCompletion):
    return open_ai_completion(input)
