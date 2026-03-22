from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.util.init_db import create_tables
from app.routers.auth import authRouter
from app.util.protectRoute import get_current_user
from app.db.schema.user import UserInResponse
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database tables at start
    create_tables()
    yield # separation point
    # Perform any cleanup if necessary at shutdown

app = FastAPI(lifespan=lifespan)
app.include_router(authRouter, prefix="/auth", tags=["auth"])

@app.get("/health")
def health_check():
    return {"status": "Running..."}

@app.get("/protected")
def protected_route(user: UserInResponse = Depends(get_current_user)):
    return {"message": f"Hello, {user.first_name} {user.last_name}! This is a protected route."}
