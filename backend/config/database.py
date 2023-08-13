import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

user = os.environ['USERNAME']
password = os.environ['PASSWORD'] 
host = os.environ['HOST']
port = os.environ['PORT']
database = os.environ['DATABASE']

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
