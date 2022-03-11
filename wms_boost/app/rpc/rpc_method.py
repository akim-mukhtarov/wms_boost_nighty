from typing import Optional
from inspect import isclass
from pydantic import BaseModel, ValidationError
from jsonrpcserver import method, InvalidParams


def get_input_model(func) -> Optional[BaseModel]:
    """ Extract pydantic model from func' annotations """
    it = func.__annotations__.values()
    # BUG: jsonrpcserver return annotation is an instance, not a class
    cond = lambda x: isclass(x) and issubclass(x, BaseModel)
    res = next((x for x in it if cond(x)), None)
    return res


def rpc_method(func):
    """ Wrap jsonrpcserver' `@method`
        to use it with pydantic models """
    model = get_input_model(func)
    if model:
        rpc_params = model.__annotations__
    else:
        rpc_params = {}
    # will be called by rpc-method
    def wrapper(*args, **kwargs):
        # run pydantic validation
        if model:
            try:
                arg = model.parse_obj(kwargs)
            except ValidationError as e:
                return InvalidParams(str(e))
            else:
                return func(*args, arg)

        return func(*args, **kwargs)
    # thus, wrapper will be correctly called by `jsonrpcserver`
    wrapper.__annotations__ = rpc_params
    rpc_wrapped = method(wrapper, name=func.__name__)
    return rpc_wrapped
