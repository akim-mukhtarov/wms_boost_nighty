from enum import Enum


RpcErrors = Enum('RpcErrors', [
    'NOT_FOUND',
    'ALREADY_EXISTS',
    'NOT_AUTHORIZED',
    'PERMISSION_DENIED',
    'FAILED_PRECONDITION',
    'UNIMPLEMENTED',
    'UNAVAILABLE',
    'INTERNAL'
])
