# backend/tests/utils/alembic_runner.py

import os

from alembic import command
from alembic.config import Config


def run_migrations(target_db_url: str):
    """Run Alembic migrations against the specified database URL."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", target_db_url)
    command.upgrade(alembic_cfg, "head")
