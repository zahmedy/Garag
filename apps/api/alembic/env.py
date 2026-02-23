from logging.config import fileConfig
from alembic import context
from sqlmodel import SQLModel
from app.core.config import settings
from app.db.session import engine

# import models so metadata is registered
from app.models.user import User  # noqa
from app.models.car import CarMake, CarModel, CarListing, CarMedia  # noqa

config = context.config
fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()