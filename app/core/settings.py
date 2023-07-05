from pydantic import BaseSettings

class Settings(BaseSettings):
    check_expiration = True
    jwt_header_prefix = "Bearer"
    jwt_header_name = "Authorization"
    userpools = {
        "eu": {
            "region": "eu-central-1",
            "userpool_id": "article_chat_userpool",
            "app_client_id": ["article_chat_web"]
        }
    }

settings = Settings()