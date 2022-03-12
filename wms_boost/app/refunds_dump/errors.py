from jsonrpcserver import Error
from app.rpc import RpcErrors
from app.wms_api import (
    AuthenticationError,
    UnexpectedApiResponse,
    WmsServerError
)

from .refunds_dumper import AlreadyProcessed
# TODO: consider handling wms-related excpetions in separate utility?
# to aboid copying the same code

# TODO: finally add some RpcError constructor to not shitpost this everywhere!
def wrap_exception(exc: Exception):
    """ An utility to wrap exceptions while
        dump refunds in JSONRPC error format """
    if isinstance(exc, AuthenticationError):
        return Error(
                RpcErrors.NOT_AUTHORIZED,
                "Not authorized")

    elif isinstance(exc, UnexpectedApiResponse):
        return Error(
                RpcErrors.UNIMPLEMENTED,
                "Side API returned unsupported response")

    elif isinstance(exc, WmsServerError):
        return Error(
                RpcErrors.UNAVAILABLE,
                "Side API is unavailable")

    elif isinstance(exc, AlreadyProcessed):
        return Error(
                RpcErrors.FAILED_PRECONDITION,
                "Precondition failed")

    else:
        return Error(RpcErrors.INTERNAL, "Internal error")
