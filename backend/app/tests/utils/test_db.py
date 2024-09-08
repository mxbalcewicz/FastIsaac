from app.core.settings import settings
from pydantic import PostgresDsn
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}/{settings.POSTGRES_DB}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
