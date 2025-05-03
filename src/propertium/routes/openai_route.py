from fastapi import APIRouter

from propertium.schemas.openai_schemas import OpenAiCompletion
from propertium.services.openai_service import completions

router = APIRouter()

@router.post("/text/")
def text(input: OpenAiCompletion):
    return completions(input)
