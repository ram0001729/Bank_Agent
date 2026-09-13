from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["Auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    token: str
    username: str
    role: str


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    role = "customer"
    if "admin" in request.username.lower():
        role = "admin"
    elif "emp" in request.username.lower():
        role = "employee"

    return LoginResponse(
        token=f"token-{role}-{request.username}",
        username=request.username,
        role=role
    )


@router.get("/me")
def get_current_user_profile():
    return {
        "username": "customer_demo",
        "email": "demo@bankagent.ai",
        "role": "customer"
    }
