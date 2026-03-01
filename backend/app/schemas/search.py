from pydantic import BaseModel

from app.schemas.wordline import WordLineRead


class SearchQuery(BaseModel):
    form: str | None = None
    lemma: str | None = None
    upos: str | None = None
    xpos: str | None = None
    feats: str | None = None
    head: str | None = None
    deprel: str | None = None
    deps: str | None = None
    misc: str | None = None
    sent_id: str | None = None
    text: str | None = None
    treebank_title: str | None = None


class SearchResult(WordLineRead):
    sentence_sent_id: str
    sentence_text: str
    treebank_title: str
    annotator_username: str
