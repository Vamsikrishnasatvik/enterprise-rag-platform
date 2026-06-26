from sqlalchemy import text

from app.db.session import engine


def check_db_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))