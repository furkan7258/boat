from datetime import datetime

from pydantic import BaseModel


class TreebankCreate(BaseModel):
    title: str
    language: str


class TreebankRead(BaseModel):
    id: int
    title: str
    language: str
    created_at: datetime

    model_config = {"from_attributes": True}


class TreebankWithProgress(TreebankRead):
    sentence_count: int = 0
    annotation_count: int = 0
    complete_count: int = 0
