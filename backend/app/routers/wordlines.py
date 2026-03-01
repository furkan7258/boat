from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.annotation import Annotation
from app.models.user import User
from app.models.wordline import WordLine
from app.schemas.wordline import WordLineBatchUpdate, WordLineRead

router = APIRouter(prefix="/wordlines", tags=["wordlines"])


@router.put(
    "/annotations/{annotation_id}",
    response_model=list[WordLineRead],
)
async def batch_update_wordlines(
    annotation_id: int,
    body: WordLineBatchUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Replace all wordlines for an annotation in a single request."""
    result = await db.execute(select(Annotation).where(Annotation.id == annotation_id))
    annotation = result.scalar_one_or_none()
    if not annotation:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Annotation not found")
    if annotation.annotator_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not your annotation")

    # Delete existing wordlines
    await db.execute(delete(WordLine).where(WordLine.annotation_id == annotation_id))

    # Create new wordlines
    new_wordlines = []
    for wl_data in body.wordlines:
        wl = WordLine(annotation_id=annotation_id, **wl_data.model_dump())
        wl.populate_parsed_fields()
        db.add(wl)
        new_wordlines.append(wl)

    await db.commit()

    # Refresh to get IDs
    for wl in new_wordlines:
        await db.refresh(wl)

    return new_wordlines


@router.get(
    "/annotations/{annotation_id}",
    response_model=list[WordLineRead],
)
async def list_wordlines(
    annotation_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(WordLine).where(WordLine.annotation_id == annotation_id))
    return result.scalars().all()
