from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..dependencies import current_user
from ..models import User

router = APIRouter(prefix='/api/v1/users', tags=['users'])

@router.get('/me')
async def me(user: User = Depends(current_user)) -> dict[str, str | bool]:
    return {'id': user.id, 'name': user.name, 'email': user.email, 'verified': user.verified}
