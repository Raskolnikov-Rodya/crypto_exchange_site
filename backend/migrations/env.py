from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# IMPORTANT: Add project root to sys.path FIRST
import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# this is the Alembic Config object
config = context.config

# Load .env file (same as in main.py)
from dotenv import load_dotenv
load_dotenv()

# Override sqlalchemy.url with real value from .env
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)
else:
    raise ValueError("DATABASE_URL not found in .env")

# Override to sync driver for Alembic (replace +asyncpg with +psycopg2)
sync_db_url = db_url.replace("+asyncpg", "+psycopg2")
config.set_main_option("sqlalchemy.url", sync_db_url)

# Then continue with imports
from app.models.base import Base
from app.models.user import User
from app.models.balance import Balance
from app.models.transaction import Transaction

target_metadata = Base.metadata

# Debug print (keep or comment)
print("DEBUG Alembic env.py - Tables in target_metadata:")
print(list(Base.metadata.tables.keys()))  # Safer version, avoids sorting crash

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata
target_metadata = Base.metadata

# Optional debug print (add this temporarily to confirm)
print("DEBUG Alembic env.py - Tables in target_metadata:")
for table in target_metadata.sorted_tables:
    print(f"  - {table.name}")

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            render_as_batch=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# Uncomment these — Alembic needs them to run
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()