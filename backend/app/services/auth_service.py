import logging

from fastapi import (
    HTTPException,
    status,
)
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.models.user import User

logger = logging.getLogger(__name__)


class AuthService:
    """
    Handles user authentication and account management.
    """

    @staticmethod
    def register(
        db: Session,
        email: str,
        password: str,
        full_name: str,
        tenant_id: int = 1,
        role: str = "VIEWER",
    ) -> User:
        """
        Registers a new user.
        """

        existing_user = (
            db.query(User)
            .filter(
                User.email == email,
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )

        user = User(
            email=email,
            password_hash=hash_password(
                password,
            ),
            full_name=full_name,
            tenant_id=tenant_id,
            role=role,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(
            "Registered user | id=%d | email=%s",
            user.id,
            user.email,
        )

        return user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ) -> dict:
        """
        Authenticates a user and returns a JWT access token.
        """

        user = (
            db.query(User)
            .filter(
                User.email == email,
            )
            .first()
        )

        if (
            user is None
            or not verify_password(
                password,
                user.password_hash,
            )
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
            )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "tenant_id": user.tenant_id,
                "role": user.role,
            }
        )

        logger.info(
            "User login successful | id=%d",
            user.id,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    @staticmethod
    def get_current_user(
        db: Session,
        user_id: int,
    ) -> User | None:
        """
        Retrieves the current authenticated user.
        """

        return (
            db.query(User)
            .filter(
                User.id == user_id,
            )
            .first()
        )