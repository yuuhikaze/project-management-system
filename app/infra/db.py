import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DB_URL = os.getenv("DB_URL")

if DB_URL:
    engine = create_engine(DB_URL, future=True)
else:
    raise Exception("DB_URL env var not declared.")

SessionLocal = sessionmaker(bind=engine, future=True)


class Base(DeclarativeBase):
    pass
