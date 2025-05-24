import json

import pytest
from dotenv import load_dotenv
from moto import mock_aws

from services.auth_service.src.handlers.signin import handler
from services.auth_service.tests.unit.mocks.cognito import create_mock_cognito_user

load_dotenv()


@mock_aws()
class TestV1SignIn:
    @pytest.mark.describe("Anonymous user")
    class TestAnonymousUser:
        @pytest.mark.it("with invalid body")
        def test_invalid_body(self):
            event = {
                "body": json.dumps({"email": "invalid@email.com", "name": "Invalid Guy"})
            }
            response = handler(event, None)
            assert response["statusCode"] == 422

        @pytest.mark.it("with invalid credentials")
        def test_invalid_credentials(self):
            event = {
                "body": json.dumps({"email": "invalid@email.com", "password": "Invalid@123"})
            }
            response = handler(event, None)
            assert response["statusCode"] == 401

        @pytest.mark.it("with valid credentials")
        def test_valid_credentials(self):
            event = {
                "body": json.dumps({"email": "kaueslim@gmail.com", "password": "ValidPass@123"})
            }

            create_mock_cognito_user(json.loads(event["body"]))

            response = handler(event, None)
            assert response["statusCode"] == 200
