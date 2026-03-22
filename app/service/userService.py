from app.db.repository.userRepo import UserRepository
from app.db.schema.user import *
from app.core.security.hashHelper import HashHelper
from app.core.security.authHandler import AuthHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException

class UserService:
    def __init__(self, session: Session):
        self.__userRepository = UserRepository(session=session)

    def signup(self, user_data: UserInSignup) -> UserInResponse:
        if self.__userRepository.user_exist_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists. Please login instead.")
        
        hashed_password = HashHelper.hash_password(user_data.password)

        user_data.password = hashed_password

        return self.__userRepository.create_user(user_data)
    
    def login(self, user_data: UserInLogin) -> str:
        user = self.__userRepository.get_user_by_email(user_data.email)
        if user is None:
            raise HTTPException(status_code=400, detail="Invalid email or password.")
        
        if not HashHelper.verify_password(user_data.password, user.password):
            raise HTTPException(status_code=400, detail="Invalid email or password.")
        
        token = AuthHandler.sign_jwt(user.id)

        if token: 
            return UserWithToken(token=token)
        raise HTTPException(status_code=500, detail="Unable to generate token. Please try again later.")

    def get_user_by_id(self, user_id: int):
        user = self.__userRepository.get_user_by_id(user_id)
        if user:
            return UserInResponse(id=user.id, email=user.email, first_name=user.first_name, last_name=user.last_name)
        raise HTTPException(status_code=400, detail="User is not available")