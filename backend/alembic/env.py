import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context

# -----------------------------------------------------
# Load Environment Variables
# -----------------------------------------------------

load_dotenv()

config = context.config

DATABASE_URL = os.getenv("ALEMBIC_DATABASE_URL")

if DATABASE_URL is None:
    raise RuntimeError("ALEMBIC_DATABASE_URL not found.")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

# -----------------------------------------------------
# Logging
# -----------------------------------------------------

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# -----------------------------------------------------
# Import Models
# -----------------------------------------------------

from app.models import Base

# Importing the ticket service models registers only the ticket schema
# with the shared Base metadata. Shared RBAC tables are intentionally
# excluded from Alembic's target metadata.
import app.models

# Metadata
# The service owns only the ticket-related tables in this shared database.
target_metadata = Base.metadata


def include_object(object, name, type_, reflected, compare_to):
    """Ignore shared RBAC tables during autogenerate comparisons."""
    if type_ == "table" and name in {
        "users",
        "roles",
        "permissions",
        "role_permissions",
        "audit_logs",
    }:
        return False
    return True


# -----------------------------------------------------
# Offline Migration
# -----------------------------------------------------

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        include_object=include_object,
        version_table="ticket_alembic_version",
    )

    with context.begin_transaction():
        context.run_migrations()


# -----------------------------------------------------
# Online Migration
# -----------------------------------------------------

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_object=include_object,
            version_table="ticket_alembic_version",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()