from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.annotation import Annotation
from app.models.sentence import Sentence
from app.models.treebank import Treebank
from app.models.user import User
from app.models.wordline import WordLine
from app.schemas.search import SearchResponse, SearchResult

router = APIRouter(prefix="/search", tags=["search"])

# Searchable fields on WordLine
_WL_FIELDS = ("form", "lemma", "upos", "xpos", "feats", "head", "deprel", "deps", "misc")


def _apply_filters(stmt, filters, sent_id, text, treebank_title):
    """Apply search filters to a statement."""
    for field_name, value in filters.items():
        if value is not None:
            stmt = stmt.where(getattr(WordLine, field_name).ilike(f"%{value}%"))
    if sent_id is not None:
        stmt = stmt.where(Sentence.sent_id.ilike(f"%{sent_id}%"))
    if text is not None:
        stmt = stmt.where(Sentence.text.ilike(f"%{text}%"))
    if treebank_title is not None:
        stmt = stmt.where(Treebank.title.ilike(f"%{treebank_title}%"))
    return stmt


@router.get("", response_model=SearchResponse)
async def search(
    form: str | None = None,
    lemma: str | None = None,
    upos: str | None = None,
    xpos: str | None = None,
    feats: str | None = None,
    head: str | None = None,
    deprel: str | None = None,
    deps: str | None = None,
    misc: str | None = None,
    sent_id: str | None = None,
    text: str | None = None,
    treebank_title: str | None = None,
    limit: int = Query(50, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    filters = {
        "form": form,
        "lemma": lemma,
        "upos": upos,
        "xpos": xpos,
        "feats": feats,
        "head": head,
        "deprel": deprel,
        "deps": deps,
        "misc": misc,
    }

    def base_joins(s):
        return (
            s.join(Annotation, WordLine.annotation_id == Annotation.id)
            .join(Sentence, Annotation.sentence_id == Sentence.id)
            .join(Treebank, Sentence.treebank_id == Treebank.id)
            .join(User, Annotation.annotator_id == User.id)
        )

    # Count query
    count_stmt = base_joins(select(func.count(WordLine.id)))
    count_stmt = _apply_filters(count_stmt, filters, sent_id, text, treebank_title)
    total = (await db.execute(count_stmt)).scalar_one()

    # Data query
    stmt = base_joins(select(WordLine)).options(
        selectinload(WordLine.annotation)
        .selectinload(Annotation.sentence)
        .selectinload(Sentence.treebank),
        selectinload(WordLine.annotation).selectinload(Annotation.annotator),
    )
    stmt = _apply_filters(stmt, filters, sent_id, text, treebank_title)
    stmt = stmt.offset(offset).limit(limit)
    result = await db.execute(stmt)
    wordlines = result.scalars().all()

    return SearchResponse(
        total=total,
        results=[
            SearchResult(
                id=wl.id,
                annotation_id=wl.annotation_id,
                id_f=wl.id_f,
                form=wl.form,
                lemma=wl.lemma,
                upos=wl.upos,
                xpos=wl.xpos,
                feats=wl.feats,
                head=wl.head,
                deprel=wl.deprel,
                deps=wl.deps,
                misc=wl.misc,
                sentence_sent_id=wl.annotation.sentence.sent_id,
                sentence_text=wl.annotation.sentence.text,
                treebank_title=wl.annotation.sentence.treebank.title,
                annotator_username=wl.annotation.annotator.username,
            )
            for wl in wordlines
        ],
    )
