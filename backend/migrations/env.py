from logging.config import fileConfig
import os
import sys

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

config = context.config

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL not found in .env")

sync_db_url = db_url.replace("+asyncpg", "+psycopg")
config.set_main_option("sqlalchemy.url", sync_db_url)

from App.models import Base  # noqa: E402
from App.models.balance import Balance  # noqa: F401,E402
from App.models.order import Order  # noqa: F401,E402
from App.models.queue import WithdrawalQueue  # noqa: F401,E402
from App.models.transaction import Transaction  # noqa: F401,E402
from App.models.user import User  # noqa: F401,E402
from App.models.wallet import Wallet  # noqa: F401,E402

target_metadata = Base.metadata

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
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


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
