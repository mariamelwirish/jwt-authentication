from pydantic import EmailStr, BaseModel
from typing import Union

# what we expect to receive from the user when they sign up
class UserInSignup(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

# what we return to the user when they sign up or log in
class UserInResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

# what we expect to receive from the user when they log in
class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserInUpdate(BaseModel):
    id: int
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    
class UserWithToken(BaseModel):
    token: str