from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..dependencies import verified_user
from ..models import Document, User, Unit
from ..schemas import AnswerResponse, AskRequest, Claim

router = APIRouter(prefix='/api/v1/ask', tags=['research'])

@router.post('', response_model=AnswerResponse)
async def ask(payload: AskRequest, user: User = Depends(verified_user), db: AsyncSession = Depends(get_db)):
    query = select(Unit, Document).join(Document, Unit.document_id == Document.id).where(Document.owner_id == user.id)
    if payload.document_id:
        query = query.where(Document.id == payload.document_id)
    rows = (await db.execute(query)).all()
    terms = {term.lower() for term in payload.question.split() if len(term) > 2}
    ranked = sorted(rows, key=lambda pair: sum(term in pair[0].content.lower() for term in terms), reverse=True)
    evidence = [pair for pair in ranked if any(term in pair[0].content.lower() for term in terms)][:5]
    if not evidence:
        return AnswerResponse(answer='not found in your papers', claims=[], found=False)
    claims = [Claim(text=unit.content[:500], unit_id=unit.id, page=unit.page, modality=unit.modality) for unit, _ in evidence]
    answer = 'Relevant evidence found in your papers:\n\n' + '\n\n'.join(f'[{index + 1}] {claim.text}' for index, claim in enumerate(claims))
    return AnswerResponse(answer=answer, claims=claims, found=True)
