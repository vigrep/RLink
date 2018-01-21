"""
python alembic with environment variables
At my job we’re currently using alembic to manage our database migrations (i.e adding a new table / index etc.)

The tool is pretty mature and has been here for a while, so it covers a lot of advanced case (like handling several databases, having a tree of migrations etc.) while still being simple for simple case

The only not straighforward thing I found was that it’s not easy to integrate with 12Factor-apps, i.e my code is running in a lot of differents environments (vagrant+docker on my local machine, the QA environments, the pre-production, production etc.)

And of course I don’t want to have to maintain in the configuration file all the different combination, and even less do I want to write down my database password, so instead we’re relying on environment variables

In order to achieve this, once you’ve done your alembic init, take your migrations folder created by alembic, and in it modify the env.py file to look like this: (the important part is the get_url methods)

Of course you can adapt it to your need/database/driver, normally you just need to update that get_url method
"""
from __future__ import with_statement
from alembic import context
from sqlalchemy import engine_from_config, pool,create_engine
from logging.config import fileConfig

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# FIXME: need note
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "\\..\\")
print(sys.path)
from app import db, app
target_metadata = db.metadata
# FIXME =================

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# FIXME: need note
def get_url():
    return app.config['SQLALCHEMY_DATABASE_URI']
    # return "mysql+pymysql://%s:%s@%s/%s" % (
    #     os.getenv("DB_USER", "root"),
    #     os.getenv("DB_PASSWORD", "123456"),
    #     os.getenv("DB_HOST", "127.0.0.1"),
    #     os.getenv("DB_NAME", "rlink"),
    # )


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # FIXME: need note
    # url = config.get_main_option("sqlalchemy.url")
    url = get_url()

    context.configure(
        url=url, target_metadata=target_metadata, literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # FIXME: need note
    connectable = create_engine(get_url())
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section),
    #     prefix='sqlalchemy.',
    #     poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
