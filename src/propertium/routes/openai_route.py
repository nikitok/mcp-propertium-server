from fastapi import APIRouter

from propertium.schemas.openai_schemas import OpenAiCompletion
from propertium.services.openai_service import open_ai_completion

router = APIRouter()

@router.post("/text/")
def text(input: OpenAiCompletion):
    return open_ai_completion(input)
