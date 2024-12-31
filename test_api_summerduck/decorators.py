import logging
import json
import functools


def __status_logging(func):
    """
    Decorator to log the status code of the response.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logging.debug(f"---------------- {func.__name__} ----------------")
            response = func(*args, **kwargs)
            assert (
                response.status_code == 200
            ), f"Status code is incorrect - {response.status_code}"
            logging.debug(f"response.status_code: {response.status_code}")
        except Exception as error:
            logging.warning(f"{func.__name__} failed: {error}")

        return response

    return wrapper


def __response_logging(func):
    """
    Decorator to log the response json of the response.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            logging.debug(f"response.json: {json.dumps(response.json(), indent=4)}")
        except Exception as error:
            logging.warning(f"{func.__name__} failed: {error}")

        return response

    return wrapper


def apply_logging_decorators(cls):
    """
    Class decorator to apply response_logging and status_logging to all methods
    that start with "get_", "post_", "put_", "patch_", or "delete_".
    """
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and attr_name.startswith(("delete_")):
            setattr(
                cls,
                attr_name,
                __status_logging(attr_value),
            )
        if callable(attr_value) and attr_name.startswith(
            (
                "get_",
                "post_",
                "put_",
                "patch_",
            )
        ):
            setattr(
                cls,
                attr_name,
                __response_logging(__status_logging(attr_value)),
            )
    return cls
