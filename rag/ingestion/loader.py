from pathlib import Path

from pypdf import PdfReader

from ml.utils.exception import MyException
from ml.utils.logger import logger
import sys


class PDFLoader:

    def load(
        self,
        file_path: str | Path
    ) -> list[dict]:

        try:

            file_path = Path(file_path)

            if not file_path.exists():

                raise FileNotFoundError(
                    f"PDF not found: {file_path}"
                )

            reader = PdfReader(
                str(file_path)
            )

            documents = []

            for page_number, page in enumerate(
                reader.pages,
                start=1
            ):

                text = page.extract_text() or ""

                if not text.strip():
                    continue

                documents.append(
                    {
                        "text": text,
                        "metadata": {
                            "source": file_path.name,
                            "source_path": str(
                                file_path
                            ),
                            "page": page_number,
                        }
                    }
                )

            logger.info(
                f"Loaded PDF: "
                f"{file_path.name}, "
                f"pages={len(documents)}"
            )

            return documents

        except Exception as e:

            logger.exception(
                "Failed to load PDF"
            )

            raise MyException(
                e,
                sys
            ) from e