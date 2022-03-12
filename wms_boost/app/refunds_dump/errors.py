from jsonrpcserver import Error
from app.rpc import RpcErrors
from app.wms_api import AuthenticationError
from .refunds_dumper import AlreadyProcessed
# TODO: consider handling wms-related excpetions in separate utility?
# to aboid copying the same code
def wrap_exception(exc: Exception):
    """ An utility to wrap exceptions while
        dump refunds in JSONRPC error format """
    if isinstance(exc, AuthenticationError):
        return Error(RpcErrors.NOT_AUTHORIZED)  # 403
    elif isinstance(exc, UnexpectedApiResponse):
        return Error(RpcErrors.UNIMPLEMENTED)
    elif isinstance(exc, WmsServerError):
        return Error(RpcErrors.UNAVAILABLE)
    elif isinstance(exc, AlreadyProcessed):
        return Error(RpcErrors.FAILED_PRECONDITION)
    else:
        return Error(RpcErrors.INTERNAL)
