<div align="center">
<img loading="lazy" style="width:700px" src="./docs/banner.png">
<h1 align="center">FastAPI Blog With Authentication App</h1>
<h3 align="center">Sample Project to use fast api with base usage and deployment</h3>
</div>
<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://fastapi.tiangolo.com/" target="_blank"> <img src="https://styles.redditmedia.com/t5_22y58b/styles/communityIcon_r5ax236rfw961.png" alt="fastapi" width="40" height="40"/> </a>
<a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.postgresql.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a>
<a href="https://git-scm.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a>
</p>

# Guideline
- [Guideline](#guideline)
- [Goal](#goal)
- [Development usage](#development-usage)
  - [Clone the repo](#clone-the-repo)
  - [Enviroment Varibales](#enviroment-varibales)
  - [Build everything](#build-everything)
- [Database Design](#database-design)
  - [what is alembic?](#what-is-alembic)
  - [how to use alembic?](#how-to-use-alembic)
- [Testing Usage](#testing-usage)
  - [running all tests](#running-all-tests)
- [License](#license)
- [Bugs](#bugs)

# Goal
This project main goal is to show you how we can use fast api to create a base blog app with authentications and all base needs.


# Development usage
You'll need to have [Docker installed](https://docs.docker.com/get-docker/).
It's available on Windows, macOS and most distros of Linux. 

If you're using Windows, it will be expected that you're following along inside
of [WSL or WSL
2](https://nickjanetakis.com/blog/a-linux-dev-environment-on-windows-with-wsl-2-docker-desktop-and-more).

That's because we're going to be running shell commands. You can always modify
these commands for PowerShell if you want.


## Clone the repo
Clone this repo anywhere you want and move into the directory:
```bash
git clone https://github.com/AliBigdeli/FastApi-Blog-Authentication-App.git
```

## Enviroment Varibales
environment variables are included in docker-compose.yml file for debugging mode and you are free to change commands inside:

```yaml
version: "3.9"
   
services:
  postgresdb:
    container_name: postgresdb
    image: postgres:15-alpine
    volumes:      
      - ./postgres/data:/var/lib/postgresql/data
    expose:
      - "5432"
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_DB=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - DB_VENDOR=postgres
      - PGDATA=/var/lib/postgresql/data
    restart: always
  
  # mongodb:
  #   image: mongo:latest
  #   expose:
  #     - '27017'
  #   volumes:
  #     - ./mongodb/data:/data/db
  #     - ./mongodb/config:/data/configdb
  #   environment:
  #     - MONGO_INITDB_DATABASE=mongo
  #     - MONGO_INITDB_ROOT_USERNAME=mongo
  #     - MONGO_INITDB_ROOT_PASSWORD=mongo
  #   restart: unless-stopped


  backend:
    build: 
      context: .
      dockerfile: dockerfiles/dev/fastapi/Dockerfile
    container_name: backend
    command: sh -c "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
    volumes:
      - ./core:/usr/src/app
    # env_file:
    # - envs/dev/fastapi/.env
    ports:
      - "8000:8000"
    environment:
      - PGDB_PORT=5432
      - PGDB_PASSWORD=postgres
      - PGDB_USERNAME=postgres
      - PGDB_DBNAME=postgres
      - PGDB_HOSTNAME=postgresdb
      - DATABASE_URL=postgresql://postgres:postgres@postgresdb:5432/postgres
      - ENABLE_SENTRY=False
      - SENTRY_DSN=None
      # - MGDB_PORT=27017
      # - MGDB_PASSWORD=mongo
      # - MGDB_USERNAME=mongo
      # - MGDB_DBNAME=mongo
      # - MGDB_HOSTNAME=mongodb
    restart: always

      
    depends_on:
      - postgresdb
      # - mongodb

  smtp4dev:
    image: rnwood/smtp4dev:v3
    restart: always
    ports:
      # Change the number before : to the port the web interface should be accessible on
      - '5000:80'
      # Change the number before : to the port the SMTP server should be accessible on
      - '25:25'
      # Change the number before : to the port the IMAP server should be accessible on
      - '143:143'
    volumes:
      # This is where smtp4dev stores the database..
      - smtp4dev-data:/smtp4dev
    environment:
      - ServerOptions__HostName=smtp4dev

volumes:
  smtp4dev-data:
```

## Build everything

*The first time you run this it's going to take 5-10 minutes depending on your
internet connection speed and computer's hardware specs. That's because it's
going to download a few Docker images and build the Python + requirements dependencies.*

```bash
docker compose up --build
```

Now that everything is built and running we can treat it like any other FastAPI
app. Visit <http://localhost:8000/swagger> in your favorite browser.

**Note:** If you receive an error about a port being in use? Chances are it's because
something on your machine is already running on port 8000. then you have to change the docker-compose.yml file according to your needs.

# Database Design
As simple as this project can be i am using alembic to control database changes and keep the migrations.

## what is alembic? 

Alembic is a database migrations tool written by the author of SQLAlchemy. A migrations tool offers the following functionality:

Can emit ALTER statements to a database in order to change the structure of tables and other constructs

Provides a system whereby “migration scripts” may be constructed; each script indicates a particular series of steps that can “upgrade” a target database to a new version, and optionally a series of steps that can “downgrade” similarly, doing the same steps in reverse.

Allows the scripts to execute in some sequential manner.

## how to use alembic?
first step of using alembic is to install it:

```shell
pip install sqlalchemy alembic

```

after installation you need to declare the models you want to use in the project such as the post models:
```python
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Boolean
from core.database import Base
from sqlalchemy.orm import relationship
from fastapi.encoders import jsonable_encoder
from datetime import datetime


class PostModel(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    modified_at = Column(DateTime, default=datetime.utcnow,
                         onupdate=datetime.utcnow)
    is_published = Column(Boolean,default=False)
    
    users = relationship("UserModel", back_populates='posts')

    created_date = Column(default=datetime)

```
after that in the first time of the usage you need to initiate the alembic to trace the changes in the project you can be achieved by doing the following command in the root of the project:

```shell
alembic init alembic
```

now your gonna need the configurations for the alembic to connect to the project and to the database which is provided for you in the env.py inside the alembic directory:

```python
from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
# target_metadata = None

from core.database import Base
from accounts.models import UserModel
from blog.models import PostModel
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )
    database_url = os.getenv('DATABASE_URL')
    
    connectable = engine_from_config(
        {"url": database_url},
        prefix="",
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

Once you have configured Alembic, you can create a new migration script using the alembic revision --autogenerate command. This will generate a new migration script based on the changes you have made to your SQLAlchemy model.

```shell
alembic revision --autogenerate -m "add post table"
```

After generating the migration script, you can apply the changes to your database using the alembic upgrade command.

```shell
alembic upgrade head
```


# Testing Usage
## running all tests
```bash
docker compose run --rm backend sh -c "pytest ." -v core:/usr/src/app
```
or
```bash
docker compose exec backend sh -c sh -c "pytest ." 
```

# License
MIT.


# Bugs
Feel free to let me know if something needs to be fixed. or even any features seems to be needed in this repo.
