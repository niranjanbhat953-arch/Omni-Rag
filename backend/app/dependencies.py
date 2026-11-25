from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .db import get_db
from .models import User
from .security import InvalidToken, decode_access_token

oauth2 = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')

async def current_user(token: Annotated[str, Depends(oauth2)], db: Annotated[AsyncSession, Depends(get_db)]) -> User:
    try:
        user_id = decode_access_token(token)
    except InvalidToken:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid authentication credentials')
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=401, detail='Invalid authentication credentials')
    return user

async def verified_user(user: Annotated[User, Depends(current_user)]) -> User:
    if not user.verified:
        raise HTTPException(status_code=403, detail='Email verification required')
    return user
