"""
    Backeend core class
"""

# pylint: disable=C0301,C0103,C0303,C0411,W1203,W0511

import logging
import pypdfium2 as pdfium
from PIL.Image import Image

from backend.llm_core import LLMCore
from backend.classes.description_response import DescriptionResponseListData, DescriptionResponseData

logger : logging.Logger = logging.getLogger()
   
class Core:
    """
        Backe-end core class
    """

    __secrets  : dict[str, any] = None
    __llm_core : LLMCore = None
   

    def __init__(self, secrets : dict[str, any]):
        """
            Constructor
        """
        self.__secrets = secrets

    def get_default_llm_core(self):
        """
            Return default llm core
        """
        if not self.__llm_core:
            self.__llm_core = LLMCore(self.__secrets)
        return self.__llm_core

    def get_page_text(self, pdf : pdfium.PdfDocument, page_index : int) -> str:
        """
            Get PDF page text
        """
        page = pdf[page_index]
        return page.get_textpage().get_text_bounded()

    def get_page_bitmap(self, pdf : pdfium.PdfDocument, page_index : int) -> Image:
        """
            Get PDF page bitmap
        """
        page = pdf[page_index]

        bitmap = page.render(
            scale    = 1, # 72dpi resolution
            rotation = 0, # no additional rotation
        )
        
        return bitmap.to_pil()

    def create_pdf_description(self, pdf_content : bytes) -> DescriptionResponseListData:
        """
            Create PDF description
        """
        pdf_document = pdfium.PdfDocument(pdf_content)
        page_count = len(pdf_document)
        logger.info(f"PDF document has {page_count} pages")
        
        text_list = []
        for page_index in range(page_count):
            text_list.append(self.get_page_text(pdf_document, page_index))
            
        bitmap_list : list[Image] = []
        for page_index in range(page_count):
            bitmap_list.append(self.get_page_bitmap(pdf_document, page_index))
            
        llm_core = self.get_default_llm_core()
            
        description_list : list[DescriptionResponseData] = []
        used_tokens      = 0
        used_cost        = 0.0
        errors           = []
        
        for (text, bitmap) in zip(text_list, bitmap_list):
            description : DescriptionResponseData = llm_core.create_description(text, bitmap)
            description_list.append(description.page_description)
            used_tokens += description.used_tokens
            used_cost += description.used_cost
            errors.extend(description.errors)
            
        return DescriptionResponseListData(description_list, used_tokens, used_cost, errors)
