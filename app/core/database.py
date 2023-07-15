from dotenv import load_dotenv
import os
from sqlmodel import Session, create_engine
from typing import Generator

_ = load_dotenv()

# engine = create_engine("sqlite:///database.db", echo=True)
connection_string = (
    f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
    f"@database:5432/{os.environ.get('POSTGRES_DB')}"
)
engine = create_engine(connection_string, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
