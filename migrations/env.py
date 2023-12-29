from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Import your SQLAlchemy models
from lib.base import Base
from lib.doctor import Doctor
from lib.nurse import Nurse
from lib.patient import Patient
from lib.ward import Ward

# Load the Alembic configuration file
config = context.config

# Connect to the database using the URL from the Alembic configuration
database_url = config.get_main_option("sqlalchemy.url")
engine = engine_from_config(
    config.get_section(config.config_ini_section),
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)

# Attach the engine to the metadata of the models
with engine.connect() as connection:
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
    )

    # Run the auto migration to generate the necessary changes
    with context.begin_transaction():
        context.run_migrations()
