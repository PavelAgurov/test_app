"""
    LLM Core
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203,C0412

import logging
from typing import Any
import datetime
from PIL.Image import Image

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.callbacks import get_openai_callback
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from backend.llm_base_core import LLMBaseCore
from backend import prompts
from backend.classes.description_response import DescriptionResponse, DescriptionResponseData

logger : logging.Logger = logging.getLogger()

class LLMCore(LLMBaseCore):
    """
        LLM core class
    """
    
    __llm  : ChatOpenAI
    __embeddings : HuggingFaceEmbeddings

    def __init__(self, secrets : dict[str, Any]):

        LLMBaseCore.__init__(self, secrets)
        self.__llm = self.create_llm(4000, "gpt-4o-mini")
        self.__embeddings = None
        
    def get_openai_client(self) -> ChatOpenAI:
        """
            Get openai client
        """
        return self.__llm
       
    def create_description(self, text : str, bitmap : Image) -> DescriptionResponseData:
        """
            Create description
        """
        query_prompt : ChatPromptTemplate = ChatPromptTemplate.from_template(prompts.DESCRIPTION_PROMPT_TEMPLATE)

        structured_llm = self.__llm.with_structured_output(DescriptionResponse)
        structured_chain = query_prompt | structured_llm
        
        start_time = datetime.datetime.now()
        with get_openai_callback() as cb:
            response_data : DescriptionResponse = structured_chain.invoke(text=text, bitmap=bitmap)
            
        end_time = datetime.datetime.now()

        logger.info(response_data)
        logger.info(f"LLM Time ({self.__llm.model_name}): {end_time - start_time}")
        
        return DescriptionResponseData(response_data, cb.total_tokens, cb.total_cost, [])

