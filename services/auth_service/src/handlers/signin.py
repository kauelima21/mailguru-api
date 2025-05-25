import json

from botocore.exceptions import ClientError
from pydantic import BaseModel
from src.models.authentication import sign_in_user

from shared.decorators import http_handler, log_event
from shared.errors import UnauthorizedError


class SignInBody(BaseModel):
    email: str
    password: str


@log_event
@http_handler()
def handler(event, _):
    body = json.loads(event["body"])
    auth_data = SignInBody(**body)

    try:
        response = sign_in_user(auth_data.model_dump())["AuthenticationResult"]
    except ClientError as error:
        errcode = error.response["Error"]["Code"]
        error_message = "Credenciais inválidas."

        if str(errcode) == "UserNotConfirmedException":
            error_message = "Você precisa confirmar sua conta antes de realizar o login."

        raise UnauthorizedError(error_message)

    access_token_info = {
        "access_token": response["AccessToken"],
        "refresh_token": response["RefreshToken"],
        "expires_in": response["ExpiresIn"]
    }

    return {"status_code": 200, "body": access_token_info}
