from jsonrpcserver import Error
from app.rpc import RpcErrors
from .refunds_dumper import AlreadyProcessed
# TODO: consider handling wms-related excpetions in separate utility?
# to aboid copying the same code
def wrap_exception(exc: Exception):
    """ An utility to wrap exceptions while
        dump refunds in JSONRPC error format """
    if isinstance(AuthenticationError):
        return Error(RpcErrors.NOT_AUTHORIZED)  # 403
    elif isinstance(UnexpectedApiResponse):
        return Error(RpcErrors.UNIMPLEMENTED)
    elif isinstance(WmsServerError):
        return Error(RpcErrors.UNAVAILABLE)
    elif isinstance(AlreadyProcessed):
        return Error(RpcErrors.FAILED_PRECONDITION)
