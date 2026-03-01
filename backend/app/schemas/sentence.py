from datetime import datetime

from pydantic import BaseModel


class SentenceCreate(BaseModel):
    sent_id: str
    text: str
    comments: dict | None = None


class SentenceRead(BaseModel):
    id: int
    order: int
    treebank_id: int
    sent_id: str
    text: str
    comments: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


class SentenceBrief(BaseModel):
    id: int
    order: int
    sent_id: str
    text: str

    model_config = {"from_attributes": True}
