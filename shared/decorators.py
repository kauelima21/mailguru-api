import json
from functools import wraps

from pydantic import ValidationError

from shared.errors import BaseError


def log_event(handler):
    @wraps(handler)
    def logging_decorator(*args, **kwargs):
        import logging

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.info(f"event -> {args[0]}")
        return handler(*args, **kwargs)

    return logging_decorator


def http_handler(content_type="application/json"):
    def decorator(handler):
        @wraps(handler)
        def transform_response(*args, **kwargs):
            response_dict = {
                "isBase64Encoded": False,
                "headers": {"Content-Type": content_type},
            }

            try:
                response = handler(*args, **kwargs)
            except BaseError as error:
                response = {"status_code": error.status_code, "body": error.to_dict()}
            except ValidationError as error:
                response = {
                    "status_code": 422,
                    "body": {"status_code": 422, "name": "ValidationError", "errors": error.errors()}}
            except Exception as error:
                import logging

                logger = logging.getLogger()
                logger.setLevel(logging.ERROR)
                logger.error(f"internal error -> {str(error)}")

                response = {
                    "status_code": 500,
                    "body": {
                        "status_code": 500,
                        "name": "InternalError",
                        "message": "Internal server error."
                    }
                }

            return {
                **response_dict,
                "statusCode": response["status_code"],
                "body": json.dumps(response.get("body")),
            }

        return transform_response

    return decorator
