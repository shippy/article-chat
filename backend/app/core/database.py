from dotenv import load_dotenv
import json
import os
from sqlmodel import Session, create_engine
from typing import Dict, Generator

_ = load_dotenv()

# credentials: Dict[str, str] = json.loads(os.environ.get("PGVECTOR_CREDENTIALS", '"{}"'))
# try:
#     POSTGRES_USER = credentials["username"]
#     POSTGRES_PASSWORD = credentials["password"]
# except KeyError as e:
#     raise KeyError(
#         "Please set the environment variable PGVECTOR_CREDENTIALS to a JSON object "
#         "with keys 'username' and 'password'"
#     ) from e

connection_string = (
    f"postgresql://{os.environ.get('POSTGRES_USER')}"
    f":{os.environ.get('POSTGRES_PASSWORD')}"
    f"@{os.environ.get('POSTGRES_URL', 'database')}"
    f":{os.environ.get('POSTGRES_PORT', '5432')}"
    f"/{os.environ.get('POSTGRES_DB', 'postgres')}"
)
engine = create_engine(connection_string, echo=True)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
