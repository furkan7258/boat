from datetime import datetime

from pydantic import BaseModel

from app.schemas.wordline import WordLineRead


class AnnotationCreate(BaseModel):
    sentence_id: int
    notes: str = ""
    status: int = 0
    is_template: bool = False


class AnnotationUpdate(BaseModel):
    notes: str | None = None
    status: int | None = None
    is_gold: bool | None = None


class AnnotationRead(BaseModel):
    id: int
    annotator_id: int
    sentence_id: int
    notes: str
    status: int
    is_template: bool
    is_gold: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AnnotationDetail(AnnotationRead):
    wordlines: list[WordLineRead] = []
    annotator_username: str | None = None
    sentence_sent_id: str | None = None
    sentence_text: str | None = None
    sentence_comments: dict | None = None
    treebank_title: str | None = None
