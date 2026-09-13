import re
import sys

from ml.utils.exception import MyException
from ml.utils.logger import logger


class DocumentCleaner:

    def clean(
        self,
        text: str
    ) -> str:

        try:

            text = text.replace(
                "\x00",
                ""
            )

            text = re.sub(
                r"[ \t]+",
                " ",
                text
            )

            text = re.sub(
                r"\n{3,}",
                "\n\n",
                text
            )

            return text.strip()

        except Exception as e:

            logger.exception(
                "Document cleaning failed"
            )

            raise MyException(
                e,
                sys
            ) from e