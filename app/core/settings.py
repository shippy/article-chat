from pydantic import BaseSettings

class Settings(BaseSettings):
    check_expiration = True
    jwt_header_prefix = "Bearer"
    jwt_header_name = "Authorization"
    cognito_domain_url = "https://auth.journalarticle.chat/"
    cognito_client_id = "7acimbldoceq4psub3m6ks0koc"
    cognito_redirect_uri = "/redirect"
    userpools = {
        "eu": {
            "region": "eu-central-1",
            "userpool_id": "eu-central-1_VDEU9nMwP",
            # "userpool_id": "eu-central-1:637364745310",
            "app_client_id": ["7acimbldoceq4psub3m6ks0koc"]
        }
    }

settings = Settings()
cognito_jwks_url = f"https://cognito-idp.{settings.userpools['eu']['region']}.amazonaws.com/{settings.userpools['eu']['userpool_id']}/.well-known/jwks.json"

AUTH_URL = f"https://{settings.cognito_domain_url}/oauth2/authorize"
TOKEN_URL = f"https://{settings.cognito_domain_url}/oauth2/token"
LOGOUT_URL = f"https://{settings.cognito_domain_url}/logout"
