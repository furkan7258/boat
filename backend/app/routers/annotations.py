from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.annotation import Annotation
from app.models.sentence import Sentence
from app.models.user import User
from app.models.wordline import WordLine
from app.schemas.annotation import (
    AnnotationCreate,
    AnnotationDetail,
    AnnotationRead,
    AnnotationUpdate,
)

router = APIRouter(prefix="/annotations", tags=["annotations"])


@router.post("", response_model=AnnotationRead, status_code=status.HTTP_201_CREATED)
async def create_annotation(
    body: AnnotationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify sentence exists
    result = await db.execute(select(Sentence).where(Sentence.id == body.sentence_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Sentence not found")

    annotation = Annotation(
        annotator_id=current_user.id,
        sentence_id=body.sentence_id,
        notes=body.notes,
        status=body.status,
        is_template=body.is_template,
    )
    db.add(annotation)

    # Copy wordlines from template annotation if one exists
    template_result = await db.execute(
        select(Annotation)
        .where(
            Annotation.sentence_id == body.sentence_id,
            Annotation.is_template.is_(True),
        )
        .options(selectinload(Annotation.wordlines))
        .limit(1)
    )
    template = template_result.scalar_one_or_none()
    await db.flush()

    if template and template.wordlines:
        for wl in template.wordlines:
            new_wl = WordLine(
                annotation_id=annotation.id,
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
            )
            new_wl.populate_parsed_fields()
            db.add(new_wl)

    await db.commit()
    await db.refresh(annotation)
    return annotation


@router.get(
    "/by-position/",
    response_model=AnnotationDetail,
)
async def get_annotation_by_position(
    treebank_id: int,
    order: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get (or create) the current user's annotation for a sentence at a given order."""
    # Find the sentence
    result = await db.execute(
        select(Sentence).where(
            Sentence.treebank_id == treebank_id,
            Sentence.order == order,
        )
    )
    sentence = result.scalar_one_or_none()
    if not sentence:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Sentence not found at this position")

    # Find user's annotation for this sentence
    result = await db.execute(
        select(Annotation)
        .where(
            Annotation.sentence_id == sentence.id,
            Annotation.annotator_id == current_user.id,
            Annotation.is_template.is_(False),
        )
        .options(
            selectinload(Annotation.wordlines),
            selectinload(Annotation.annotator),
            selectinload(Annotation.sentence).selectinload(Sentence.treebank),
        )
        .limit(1)
    )
    annotation = result.scalar_one_or_none()

    if not annotation:
        # Auto-create from template
        annotation = Annotation(
            annotator_id=current_user.id,
            sentence_id=sentence.id,
            status=0,
        )
        db.add(annotation)

        # Copy wordlines from template
        tmpl_result = await db.execute(
            select(Annotation)
            .where(
                Annotation.sentence_id == sentence.id,
                Annotation.is_template.is_(True),
            )
            .options(selectinload(Annotation.wordlines))
            .limit(1)
        )
        template = tmpl_result.scalar_one_or_none()
        await db.flush()

        if template and template.wordlines:
            for wl in template.wordlines:
                new_wl = WordLine(
                    annotation_id=annotation.id,
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
                )
                new_wl.populate_parsed_fields()
                db.add(new_wl)

        await db.commit()

        # Reload with relationships
        result = await db.execute(
            select(Annotation)
            .where(Annotation.id == annotation.id)
            .options(
                selectinload(Annotation.wordlines),
                selectinload(Annotation.annotator),
                selectinload(Annotation.sentence).selectinload(Sentence.treebank),
            )
        )
        annotation = result.scalar_one()

    return _build_annotation_detail(annotation)


@router.get("/{annotation_id}", response_model=AnnotationDetail)
async def get_annotation(
    annotation_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Annotation)
        .where(Annotation.id == annotation_id)
        .options(
            selectinload(Annotation.wordlines),
            selectinload(Annotation.annotator),
            selectinload(Annotation.sentence).selectinload(Sentence.treebank),
        )
    )
    annotation = result.scalar_one_or_none()
    if not annotation:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Annotation not found")

    return _build_annotation_detail(annotation)


@router.patch("/{annotation_id}", response_model=AnnotationRead)
async def update_annotation(
    annotation_id: int,
    body: AnnotationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Annotation).where(Annotation.id == annotation_id))
    annotation = result.scalar_one_or_none()
    if not annotation:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Annotation not found")
    if annotation.annotator_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your annotation")

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(annotation, field, value)
    await db.commit()
    await db.refresh(annotation)
    return annotation


@router.delete("/{annotation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_annotation(
    annotation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Annotation).where(Annotation.id == annotation_id))
    annotation = result.scalar_one_or_none()
    if not annotation:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Annotation not found")
    if annotation.annotator_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your annotation")
    await db.delete(annotation)
    await db.commit()


@router.get("/mine/", response_model=list[AnnotationDetail])
async def my_annotations(
    annotation_status: int | None = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stmt = (
        select(Annotation)
        .where(Annotation.annotator_id == current_user.id, Annotation.is_template.is_(False))
        .options(
            selectinload(Annotation.wordlines),
            selectinload(Annotation.annotator),
            selectinload(Annotation.sentence).selectinload(Sentence.treebank),
        )
        .order_by(Annotation.created_at.desc())
    )
    if annotation_status is not None:
        stmt = stmt.where(Annotation.status == annotation_status)

    result = await db.execute(stmt)
    annotations = result.scalars().all()

    return [_build_annotation_detail(a) for a in annotations]


def _build_annotation_detail(a: Annotation) -> AnnotationDetail:
    """Build an AnnotationDetail from a loaded Annotation with relationships."""
    return AnnotationDetail(
        id=a.id,
        annotator_id=a.annotator_id,
        sentence_id=a.sentence_id,
        notes=a.notes,
        status=a.status,
        is_template=a.is_template,
        is_gold=a.is_gold,
        created_at=a.created_at,
        wordlines=[
            {
                "id": wl.id,
                "annotation_id": wl.annotation_id,
                "id_f": wl.id_f,
                "form": wl.form,
                "lemma": wl.lemma,
                "upos": wl.upos,
                "xpos": wl.xpos,
                "feats": wl.feats,
                "head": wl.head,
                "deprel": wl.deprel,
                "deps": wl.deps,
                "misc": wl.misc,
                "feats_parsed": wl.feats_parsed,
                "misc_parsed": wl.misc_parsed,
            }
            for wl in a.wordlines
        ],
        annotator_username=a.annotator.username,
        sentence_sent_id=a.sentence.sent_id,
        sentence_text=a.sentence.text,
        sentence_comments=a.sentence.comments,
        treebank_title=a.sentence.treebank.title,
    )
