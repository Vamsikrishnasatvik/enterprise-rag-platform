from fastapi import (
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        email: str,
        password: str,
        full_name: str,
        tenant_id: int = 1,
        role: str = "VIEWER",
    ):
        existing_user = (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Email already exists",
            )

        user = User(
            email=email,
            password_hash=hash_password(
                password
            ),
            full_name=full_name,
            tenant_id=tenant_id,
            role=role,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str,
    ):
        user = (
            db.query(User)
            .filter(
                User.email == email
            )
            .first()
        )

        if (
            not user
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

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    @staticmethod
    def get_current_user(
        db: Session,
        user_id: int,
    ):
        return (
            db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )