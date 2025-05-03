from pydantic import BaseModel

class OpenAiCompletion(BaseModel):
    text: str