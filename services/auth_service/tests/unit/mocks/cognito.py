import os

from models.authentication import get_new_client, sign_up_user


def create_mock_cognito_client_pool():
    client = get_new_client()
    response = client.create_user_pool(PoolName="test-user-pool")

    user_pool_id = response["UserPool"]["Id"]
    response = client.create_user_pool_client(
        UserPoolId=user_pool_id,
        ClientName="test-client",
        GenerateSecret=False
    )

    client_id = response["UserPoolClient"]["ClientId"]
    os.environ["MAILGURU_COGNITO_CLIENT_ID"] = client_id
    os.environ["MAILGURU_COGNITO_POOL_ID"] = user_pool_id


def create_mock_cognito_user(user_data: dict, auto_confirm = True):
    create_mock_cognito_client_pool()

    sing_up_response = sign_up_user(user_data, {})

    if auto_confirm:
        client = get_new_client()
        client.admin_confirm_sign_up(
            UserPoolId=os.environ.get("MAILGURU_COGNITO_POOL_ID"),
            Username=user_data["email"]
        )

    return sing_up_response
