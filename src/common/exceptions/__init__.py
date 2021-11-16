from enum import Enum


class APIException(Exception):
    def __init__(self, err_code: Enum, **kwargs) -> None:
        self.error = err_code
        self._extra = kwargs
        super().__init__(err_code.value[1])
