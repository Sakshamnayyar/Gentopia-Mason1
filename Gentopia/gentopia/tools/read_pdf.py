from typing import AnyStr
from gentopia.tools.basetool import *
import urllib.request
import PyPDF2
import io

class PDFReaderParameters(BaseModel):
    pdf_url: str = Field(..., description="URL link to the PDF document")

# class for PDF Reading functionality
class PDFReader(BaseTool):
    """Tool for reading text from PDF"""
    name = "read_pdf"
    description = "A tool for reading PDF documents from URLs that accepts a PDF URL as input."

    args_schema: Optional[Type[BaseModel]] = PDFReaderParameters

    # Method to read text from a PDF
    def _run(self, pdf_url: AnyStr) -> str:
        # creating a request object 
        request = urllib.request.Request(pdf_url, headers={'User-Agent': "Magic Browser"})
        # opening the URL to read the content
        pdf_content = urllib.request.urlopen(request).read()
        # converting the content to a byte stream
        pdf_stream = io.BytesIO(pdf_content)
        pdf_document = PyPDF2.PdfReader(pdf_stream)
        # extracting text from each page
        text_output = "\n\n".join(page.extract_text() for page in pdf_document.pages)
        return text_output

    # abstract method for asynchronous run
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError("Asynchronous execution not implemented.")


if __name__ == "__main__":
    # example pdf link
    pdf_url = "https://arxiv.org/pdf/2308.04030.pdf"  # Example PDF URL
    # creating an instance of PDFReader
    reader = PDFReader()
    # using the instance to read text from the example PDF
    extracted_text = reader._run(pdf_url)
    # printing the PDF text
    print(extracted_text)
