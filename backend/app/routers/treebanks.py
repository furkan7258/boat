from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.expression import case

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.annotation import Annotation, AnnotationStatus
from app.models.sentence import Sentence
from app.models.treebank import Treebank
from app.models.user import User
from app.models.validation_profile import ValidationProfile
from app.models.wordline import WordLine
from app.schemas.sentence import SentenceBrief
from app.schemas.treebank import TreebankCreate, TreebankRead, TreebankWithProgress
from app.services.agreement import compute_annotation_agreement
from app.services.conllu import LANGUAGES, export_conllu, parse_text, validate_uploaded_text

router = APIRouter(prefix="/treebanks", tags=["treebanks"])


@router.get("", response_model=list[TreebankWithProgress])
async def list_treebanks(
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    # Compute progress stats in a single query
    stmt = (
        select(
            Treebank,
            func.count(func.distinct(Sentence.id)).label("sentence_count"),
            func.count(Annotation.id).label("annotation_count"),
            func.coalesce(
                func.sum(case((Annotation.status == AnnotationStatus.COMPLETE, 1), else_=0)),
                0,
            ).label("complete_count"),
        )
        .outerjoin(Sentence, Sentence.treebank_id == Treebank.id)
        .outerjoin(Annotation, Annotation.sentence_id == Sentence.id)
        .group_by(Treebank.id)
        .order_by(Treebank.created_at.desc())
    )
    result = await db.execute(stmt)
    rows = result.all()

    return [
        TreebankWithProgress(
            id=tb.id,
            title=tb.title,
            language=tb.language,
            created_at=tb.created_at,
            sentence_count=sent_count or 0,
            annotation_count=anno_count or 0,
            complete_count=comp_count or 0,
        )
        for tb, sent_count, anno_count, comp_count in rows
    ]


@router.post("", response_model=TreebankRead, status_code=status.HTTP_201_CREATED)
async def create_treebank(
    body: TreebankCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Treebank).where(Treebank.title == body.title))
    if result.scalar_one_or_none():
        raise HTTPException(status.HTTP_409_CONFLICT, "Treebank title already exists")
    treebank = Treebank(title=body.title, language=body.language)
    db.add(treebank)
    await db.flush()

    # Auto-create a validation profile with sensible MISC defaults
    profile = ValidationProfile(
        treebank_id=treebank.id,
        allowed_misc={
            "SpaceAfter": ["No"],
            "SpacesAfter": None,
            "Translit": None,
            "LTranslit": None,
            "Gloss": None,
        },
    )
    db.add(profile)
    await db.commit()
    await db.refresh(treebank)
    return treebank


@router.get("/languages")
async def list_languages(_current_user: User = Depends(get_current_user)):
    return LANGUAGES


@router.get("/by-title/{title}", response_model=TreebankRead)
async def get_treebank_by_title(
    title: str,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Treebank).where(Treebank.title == title))
    treebank = result.scalar_one_or_none()
    if not treebank:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Treebank not found")
    return treebank


@router.get("/{treebank_id}", response_model=TreebankRead)
async def get_treebank(
    treebank_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Treebank).where(Treebank.id == treebank_id))
    treebank = result.scalar_one_or_none()
    if not treebank:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Treebank not found")
    return treebank


@router.delete("/{treebank_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_treebank(
    treebank_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Treebank).where(Treebank.id == treebank_id))
    treebank = result.scalar_one_or_none()
    if not treebank:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Treebank not found")
    await db.delete(treebank)
    await db.commit()


@router.get("/{treebank_id}/sentences", response_model=list[SentenceBrief])
async def list_sentences(
    treebank_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Sentence).where(Sentence.treebank_id == treebank_id).order_by(Sentence.order)
    )
    return result.scalars().all()


@router.post("/{treebank_id}/upload", status_code=status.HTTP_201_CREATED)
async def upload_conllu(
    treebank_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Treebank).where(Treebank.id == treebank_id))
    treebank = result.scalar_one_or_none()
    if not treebank:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Treebank not found")

    max_size = 10 * 1024 * 1024  # 10 MB
    raw = await file.read()
    if len(raw) > max_size:
        raise HTTPException(
            status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            f"File too large ({len(raw) / 1024 / 1024:.1f} MB). Maximum is 10 MB.",
        )
    content = raw.decode("utf-8").replace("\r\n", "\n")
    if not content.endswith("\n"):
        content += "\n"
    if not validate_uploaded_text(content):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, "Invalid CoNLL-U file")

    sentences = parse_text(content)

    # Get current max order
    max_order_result = await db.execute(
        select(func.max(Sentence.order)).where(Sentence.treebank_id == treebank_id)
    )
    current_max = max_order_result.scalar() or 0

    created_count = 0
    for i, sent_data in enumerate(sentences, start=current_max + 1):
        sent_id = sent_data.get("sent_id", f"{treebank.title}-{i}")
        text = sent_data.get("text", "")
        metadata = sent_data.get("metadata")

        sentence = Sentence(
            order=i,
            treebank_id=treebank_id,
            sent_id=sent_id,
            text=text,
            metadata_=metadata,
        )
        db.add(sentence)
        await db.flush()

        # Create template annotation with wordlines
        annotation = Annotation(
            annotator_id=current_user.id,
            sentence_id=sentence.id,
            is_template=True,
            status=0,
        )
        db.add(annotation)
        await db.flush()

        # Create wordlines from parsed data
        for word_id, fields in sent_data.items():
            if word_id in ("sent_id", "text", "metadata"):
                continue
            wordline = WordLine(
                annotation_id=annotation.id,
                id_f=word_id,
                form=fields.get("form", "_"),
                lemma=fields.get("lemma", "_"),
                upos=fields.get("upos", "_"),
                xpos=fields.get("xpos", "_"),
                feats=fields.get("feats", "_"),
                head=fields.get("head", "_"),
                deprel=fields.get("deprel", "_"),
                deps=fields.get("deps", "_"),
                misc=fields.get("misc", "_"),
            )
            wordline.populate_parsed_fields()
            db.add(wordline)
        created_count += 1

    await db.commit()
    return {"sentences_created": created_count}


@router.get("/{treebank_id}/export")
async def export_treebank_conllu(
    treebank_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Treebank).where(Treebank.id == treebank_id))
    treebank = result.scalar_one_or_none()
    if not treebank:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Treebank not found")

    # Fetch sentences with user's annotations and wordlines
    stmt = (
        select(Sentence)
        .where(Sentence.treebank_id == treebank_id)
        .options(selectinload(Sentence.annotations).selectinload(Annotation.wordlines))
        .order_by(Sentence.order)
    )
    result = await db.execute(stmt)
    sentences = result.scalars().all()

    export_data: list[dict] = []
    for sent in sentences:
        user_annos = [a for a in sent.annotations if a.annotator_id == current_user.id]
        for anno in user_annos:
            if not anno.wordlines:
                continue
            export_data.append(
                {
                    "sent_id": sent.sent_id,
                    "text": sent.text,
                    "metadata": sent.metadata_,
                    "wordlines": [
                        {
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
                        }
                        for wl in anno.wordlines
                    ],
                }
            )

    conllu_text = export_conllu(export_data)
    from fastapi.responses import PlainTextResponse

    return PlainTextResponse(
        content=conllu_text,
        media_type="text/plain",
        headers={"Content-Disposition": f'attachment; filename="{treebank.title}.conllu"'},
    )


@router.get("/{treebank_id}/agreement")
async def treebank_agreement(
    treebank_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    # Fetch all sentences with annotations and wordlines
    stmt = (
        select(Sentence)
        .where(Sentence.treebank_id == treebank_id)
        .options(selectinload(Sentence.annotations).selectinload(Annotation.wordlines))
    )
    result = await db.execute(stmt)
    sentences = result.scalars().all()

    agreement_sum = 0.0
    scored_count = 0

    for sent in sentences:
        # Only consider non-template annotations
        annos = [a for a in sent.annotations if not a.is_template]
        if len(annos) < 2:
            continue

        wordline_lists = [
            [
                {
                    "id_f": wl.id_f,
                    "form": wl.form,
                    "lemma": wl.lemma,
                    "upos": wl.upos,
                    "feats": wl.feats,
                    "head": wl.head,
                    "deprel": wl.deprel,
                }
                for wl in anno.wordlines
            ]
            for anno in annos
        ]

        score = compute_annotation_agreement(wordline_lists)
        if score == -1:
            continue
        agreement_sum += score
        scored_count += 1

    return {
        "treebank_id": treebank_id,
        "agreement": agreement_sum / scored_count if scored_count else 0,
        "sentences_scored": scored_count,
    }
