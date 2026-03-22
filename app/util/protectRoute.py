from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union
from app.core.security.authHandler import AuthHandler
from app.service.userService import UserService
from app.core.database import get_db
from app.db.schema.user import UserInResponse

AUTH_PREFIX = 'Bearer '

def get_current_user(session: Session = Depends(get_db), authorization: Annotated[Union[str, None], Header()] = None) -> UserOutput:
    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Authentication Credentials")

    if not authorization: 
        raise auth_exception
    
    if not authorization.startswith(AUTH_PREFIX):
        raise auth_exception
    
    payload = AuthHandler.decode_jwt(authorization[len(AUTH_PREFIX):])

    if payload and payload["user_id"]: 
        user = UserService(session).get_user_by_id(payload["user_id"])
        if user:
            return UserInResponse(id= user.id, email=user.email, first_name=user.first_name, last_name=user.last_name)