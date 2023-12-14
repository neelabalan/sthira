import functools
from typing import Any
from typing import Callable


class InstanceCreationError(Exception):
    pass


class Constant(type):
    def __setattr__(self, key: str, value: Any):
        raise AttributeError("Cannot set or change the class attributes")

    def __str__(cls) -> str:
        return cls.__name__

    def __repr__(cls) -> str:
        return cls.__name__

    def __call__(cls, *args, **kwargs):
        raise InstanceCreationError(
            "Cannot instantiate a class with Constant as metaclass"
        )


def constant(cls) -> Constant:
    return Constant(cls.__name__, cls.__bases__, dict(cls.__dict__))


def dispatch(func: Callable) -> Callable:
    dispatch_map = {}

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = args[0]
        if key in dispatch_map:
            return dispatch_map[key](*args[1:], **kwargs)
        return func(*args, **kwargs)

    def register(key):
        def decorator(func_):
            dispatch_map[key] = func_
            return func_

        return decorator

    wrapper.register = register
    return wrapper
