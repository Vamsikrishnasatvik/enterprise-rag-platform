from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.orm import Session

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
)
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.core.dependencies import (
    get_db,
    get_current_user,
)
from app.models.user import User

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    user = AuthService.register(
        db=db,
        email=request.email,
        password=request.password,
        full_name=request.full_name,
    )

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    token = AuthService.login(
        db=db,
        email=request.email,
        password=request.password,
    )

    return token


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(
        get_current_user
    ),
):
    return current_user