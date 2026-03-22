from fastapi import APIRouter, Depends
from app.db.schema.user import UserInResponse, UserInSignup, UserInLogin, UserWithToken
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.service.userService import UserService

authRouter = APIRouter()

@authRouter.post("/login", status_code = 200, response_model=UserWithToken)
def login(loginDetails: UserInLogin, session: Session = Depends(get_db)):
    try: 
        return UserService(session).login(loginDetails)
    except Exception as e:
        raise e
@authRouter.post("/signup", status_code = 201, response_model=UserInResponse)
def signup(signupDetails: UserInSignup, session: Session = Depends(get_db)):
    try:
        return UserService(session).signup(signupDetails)
    except Exception as e:
        raise e
