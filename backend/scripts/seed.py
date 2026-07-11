from app.db.session import SessionLocal
from app.models.tenant import Tenant
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()

try:
    # -------------------------------------------------
    # Default Tenant
    # -------------------------------------------------

    tenant = (
        db.query(Tenant)
        .filter(Tenant.slug == "default")
        .first()
    )

    if tenant is None:

        tenant = Tenant(
            name="Default Tenant",
            slug="default",
        )

        db.add(tenant)
        db.commit()
        db.refresh(tenant)

        print("Default tenant created.")

    # -------------------------------------------------
    # Admin User
    # -------------------------------------------------

    user = (
        db.query(User)
        .filter(User.email == "admin@test.com")
        .first()
    )

    if user is None:

        user = User(
            tenant_id=tenant.id,
            email="admin@test.com",
            password_hash=hash_password("password123"),
            full_name="Administrator",
            role="ADMIN",
        )

        db.add(user)
        db.commit()

        print("Admin user created.")

    else:

        print("Admin user already exists.")

finally:

    db.close()