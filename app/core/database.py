from dotenv import load_dotenv
import os
from sqlmodel import Session, create_engine
from typing import Generator

_ = load_dotenv()

# engine = create_engine("sqlite:///database.db", echo=True)
engine = create_engine(
    f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}"
    f"{os.environ.get('POSTGRES_DB')}@:5432/postgres",
    echo=True
)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session