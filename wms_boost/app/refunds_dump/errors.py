from jsonrpcserver import Error


class AlreadyProcessed(Exception):
    _msg = "Refunds dump is already being processed"

    def __init__(self):
        super().__init__(self._msg)
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
