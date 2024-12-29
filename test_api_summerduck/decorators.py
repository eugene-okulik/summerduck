import logging
import json
import functools


def status_logging(func):
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
        finally:
            return response

    return wrapper


def response_logging(func):
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
        finally:
            return response

    return wrapper


def apply_decorators_to_methods(cls):
    """
    Class decorator to apply response_logging and status_logging to all methods
    that start with "get_", "post_", "put_", "patch_", or "delete_".
    """
    for attr_name, attr_value in cls.__dict__.items():
        if callable(attr_value) and attr_name.startswith(("delete_")):
            setattr(
                cls,
                attr_name,
                status_logging(attr_value),
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
                response_logging(status_logging(attr_value)),
            )
    return cls


def log_test_details(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        test_name = func.__name__
        logging.info(f"STARTING TEST: {test_name}")
        logging.info(f"PARAMETERS: {args}, {kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"PASSED: {test_name}")
            return result
        except AssertionError as e:
            logging.error(f"FAILED: {test_name} - {str(e)}")
            raise
        except Exception as e:
            logging.error(f"ERROR: {test_name} - {str(e)}")
            raise

    return wrapper


def apply_decorator_to_all_tests(decorator):
    def class_decorator(cls):
        for attr in dir(cls):
            if callable(getattr(cls, attr)) and attr.startswith("test_"):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return class_decorator
