from fastapi_cognito import CognitoAuth, CognitoSettings
from .settings import settings

cognito_eu = CognitoAuth(settings=CognitoSettings.from_global_settings(settings))
