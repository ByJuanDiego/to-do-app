from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import declarative_base

secrets = dotenv_values("./config/.env")

user = secrets['USERNAME']
password = secrets['PASSWORD']
host = secrets['HOST']
port = secrets['PORT']
database = secrets['DATABASE']

database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()


def get_db() -> Session:
    db = Session()
    try:
        yield db
    finally:
        db.close()


def create_data_base_models() -> None:
    Base.metadata.create_all(bind=engine)
