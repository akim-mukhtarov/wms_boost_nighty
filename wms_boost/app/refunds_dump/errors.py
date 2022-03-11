from jsonrpcserver import Error
# TODO: consider handling wms-related excpetions in separate utility?
# to aboid copying the same code
def wrap_exception(exc: Exception):
    """ An utility to wrap exceptions while
        dump refunds in JSONRPC error format """
    if isinstance(AuthenticationError):
        return Error()  # 403
    elif isinstance(UnexpectedApiResponse):
        return Error()  # 501
    elif isinstance(WmsServerError):
        return Error()  # 503
    elif isinstance(AlreadyProcessed):
        return Error() # precondition is false
