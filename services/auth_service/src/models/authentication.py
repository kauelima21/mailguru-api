import os

import boto3
from botocore.exceptions import ClientError


def get_new_client():
    try:
        return boto3.client("cognito-idp", os.environ.get("REGION", "us-east-1"))
    except ClientError as error:
        raise Exception(error.response["Error"]["Code"])


def sign_in_user(auth_data: dict) -> dict:
    client = get_new_client()

    initiate_auth_params = {
        "ClientId": os.environ.get("MAILGURU_COGNITO_CLIENT_ID"),
        "AuthFlow": "USER_PASSWORD_AUTH",
        "AuthParameters": {
            "USERNAME": auth_data["email"],
            "PASSWORD": auth_data["password"]
        }
    }

    return client.initiate_auth(**initiate_auth_params)


def sign_up_user(auth_data: dict, user_attributes: dict) -> dict:
    client = get_new_client()
    parsed_user_attributes = [
        {"Name": key, "Value": value} for key, value in user_attributes.items()
    ]

    return client.sign_up(
        ClientId=os.environ.get("MAILGURU_COGNITO_CLIENT_ID"),
        Username=auth_data["email"],
        Password=auth_data["password"],
        UserAttributes=parsed_user_attributes,
    )
