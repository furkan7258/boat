from datetime import datetime

from pydantic import BaseModel, Field


class SentenceCreate(BaseModel):
    sent_id: str
    text: str
    metadata: dict | None = None


class SentenceRead(BaseModel):
    id: int
    order: int
    treebank_id: int
    sent_id: str
    text: str
    metadata: dict | None = Field(default=None, validation_alias="metadata_")
    created_at: datetime

    model_config = {"from_attributes": True}


class SentenceBrief(BaseModel):
    id: int
    order: int
    sent_id: str
    text: str
    metadata: dict | None = Field(default=None, validation_alias="metadata_")

    model_config = {"from_attributes": True}
