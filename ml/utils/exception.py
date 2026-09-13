import sys


def error_message_detail(
    error: Exception,
    error_detail
) -> str:

    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is None:
        return f"{type(error).__name__}: {error}"

    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    error_message = (
        f"Error occurred in python script: "
        f"[{file_name}] "
        f"at line number [{line_number}]: "
        f"{str(error)}"
    )

    return error_message


class MyException(Exception):

    def __init__(
        self,
        error_message: str,
        error_detail=sys
    ):
        self.error_message = error_message_detail(
            error_message,
            error_detail
        )

        super().__init__(self.error_message)

    def __str__(self) -> str:
        return self.error_message