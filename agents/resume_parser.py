from pathlib import Path
from pypdf import PdfReader
import docx2txt


class ResumeParser:

    @staticmethod
    def extract_text(file_path: str) -> str:
        """
        Extract text from PDF or DOCX resume.
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(
                f"File not found: {file_path}"
            )

        extension = path.suffix.lower()

        if extension == ".pdf":
            return ResumeParser.read_pdf(file_path)

        elif extension == ".docx":
            return ResumeParser.read_docx(file_path)

        else:
            raise ValueError(
                "Only PDF and DOCX files are supported."
            )

    @staticmethod
    def read_pdf(file_path: str) -> str:

        reader = PdfReader(file_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text

    @staticmethod
    def read_docx(file_path: str) -> str:

        return docx2txt.process(file_path)