import hashlib
import os
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import fitz
from ..db import get_db
from ..dependencies import verified_user
from ..models import Document, User, Unit
from ..settings import get_settings

router = APIRouter(prefix='/api/v1/documents', tags=['documents'])
settings = get_settings()
ALLOWED = {'application/pdf'}

@router.post('/upload', status_code=202)
async def upload_document(file: UploadFile = File(...), user: User = Depends(verified_user), db: AsyncSession = Depends(get_db)) -> dict[str, str | int]:
    if file.content_type not in ALLOWED:
        raise HTTPException(415, 'Only PDF files are currently supported')
    data = await file.read()
    if len(data) > settings.max_file_size_mb * 1024 * 1024:
        raise HTTPException(413, 'File exceeds the configured size limit')
    digest = hashlib.sha256(data).hexdigest()
    existing = await db.scalar(select(Document).where(Document.owner_id == user.id, Document.sha256 == digest))
    if existing:
        raise HTTPException(409, 'This document already exists in your library')
    try:
        pdf = fitz.open(stream=data, filetype='pdf')
        pages = len(pdf)
        if pages > settings.max_pdf_pages:
            raise HTTPException(413, 'PDF exceeds the configured page limit')
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(400, 'Invalid PDF file') from exc
    document_id = str(uuid4())
    root = Path(settings.storage_root) / user.id
    root.mkdir(parents=True, exist_ok=True)
    file_path = root / f'{document_id}.pdf'
    file_path.write_bytes(data)
    document = Document(id=document_id, owner_id=user.id, filename=file.filename or 'document.pdf', file_path=str(file_path), sha256=digest, status='indexed', pages=pages, title=(pdf.metadata.get('title') or file.filename))
    for page_number, page in enumerate(pdf, start=1):
        text = page.get_text('text').strip()
        if not text:
            continue
        document.units.append(Unit(document_id=document_id, page=page_number, modality='text', content=text, quality='good'))
    db.add(document)
    await db.commit()
    return {'document_id': document_id, 'status': document.status, 'pages': pages}

@router.get('')
async def list_documents(user: User = Depends(verified_user), db: AsyncSession = Depends(get_db)):
    rows = (await db.scalars(select(Document).where(Document.owner_id == user.id).order_by(Document.created_at.desc()))).all()
    return [{'id': row.id, 'filename': row.filename, 'title': row.title, 'status': row.status, 'pages': row.pages} for row in rows]
