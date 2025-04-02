"""
    Base class for LLM Core
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203,C0412,C0413

import logging
import os
import torch

# fix bug with torch
torch.classes.__path__ = []

from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain.globals import set_llm_cache, get_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_openai import AzureOpenAIEmbeddings

logger : logging.Logger = logging.getLogger()

class LLMBaseCore:
    """
        Base class for LLM Core
    """

    openai_api_type : str
    openai_api_deployment : str
    secrets : dict[str, any]

    def __init__(self, secrets : dict[str, any]):
        """
            Constructor
        """

        # save settings
        self.secrets = secrets

        # Init cache
        os.makedirs(".langchain-cache", exist_ok=True)
        set_llm_cache(SQLiteCache(database_path=".langchain-cache\\.langchain.db"))
        
        # init env
        self.init_llm_environment(secrets)

    def init_llm_environment(self, all_secrets : dict[str, any]):
        """
            Init OpenAI or Azure environment
        """

        self.openai_api_type = 'openai'
        self.openai_api_deployment = None
        if not all_secrets:
            return
 
        # read from secrets
        self.openai_api_type = all_secrets.get('OPENAI_API_TYPE')

        if self.openai_api_type == 'openai':
            openai_secrets = all_secrets.get('open_api_openai')
            if openai_secrets:
                if openai_secrets.get('OPENAI_API_KEY'):
                    os.environ["OPENAI_API_KEY"] = openai_secrets.get('OPENAI_API_KEY')
                    logger.info(f'Run with OpenAI from config file [{len(os.environ["OPENAI_API_KEY"])}]')
                else:
                    logger.info(f'Run with OpenAI from environment [{len(os.environ["OPENAI_API_KEY"])}]')
            else:
                logger.error('open_api_openai section is required')
            return

        if self.openai_api_type == 'azure':
            azure_secrets = all_secrets.get('open_api_azure')
            if azure_secrets:
                if azure_secrets.get('AZURE_OPENAI_API_KEY'):
                    os.environ["AZURE_OPENAI_API_KEY"] = azure_secrets.get('AZURE_OPENAI_API_KEY')
                    logger.info(f'Run with Azure OpenAI from config file [{len(os.environ["AZURE_OPENAI_API_KEY"])}]')
                else:
                    logger.info(f'Run with Azure OpenAI from environment [{len(os.environ["AZURE_OPENAI_API_KEY"])}]')
                os.environ["OPENAI_API_TYPE"] = "azure"
                os.environ["OPENAI_API_VERSION"] = azure_secrets.get('OPENAI_API_VERSION')
                os.environ["AZURE_OPENAI_ENDPOINT"] = azure_secrets.get('AZURE_OPENAI_ENDPOINT')
                self.openai_api_deployment = azure_secrets.get('OPENAI_API_DEPLOYMENT')
                logger.info('Run with Azure OpenAI config file')
            else:
                logger.error('open_api_azure section is required')
            return
        
        logger.error(f'init_llm_environment: unsupported OPENAI_API_TYPE: {self.openai_api_type}')

    def create_llm(self, max_tokens : int, model_name : str) -> ChatOpenAI:
        """
            Create LLM
        """

        if self.openai_api_type == 'openai':
            return ChatOpenAI(
                model_name     = model_name,
                max_tokens     = max_tokens,
                temperature    = 0,
                verbose        = False,
                seed = 1234
            )
        
        if self.openai_api_type == 'azure':
            return AzureChatOpenAI(
                deployment_name= self.openai_api_deployment,
                model          = model_name,
                max_tokens     = max_tokens,
                temperature    = 0,
                verbose        = False,
                seed = 1234
            )
        
        logger.error(f'create_llm: unsupported OPENAI_API_TYPE: {self.openai_api_type}')
        return None

    def create_openai_embeddings(self) -> Embeddings:
        """
            Create OpenAI Embeddings
        """

        if self.openai_api_type == 'openai':
            return OpenAIEmbeddings()
        
        if self.openai_api_type == 'azure':
            return AzureOpenAIEmbeddings()
        
        logger.error(f'create_openai_embeddings: unsupported OPENAI_API_TYPE: {self.openai_api_type}')
        return None

    def extract_llm_xml_string(self, sql_xml : str) -> str:
        """
        Extract LLM generated XML string
        """
        sql_xml = sql_xml.strip()
            
        xml_begin = "```xml"
        if sql_xml.startswith(xml_begin):
            sql_xml = sql_xml[len(xml_begin):]

        xml_end = "```"
        if sql_xml.endswith(xml_end):
            sql_xml = sql_xml[:-len(xml_end)]
            
        sql_xml = sql_xml.strip()

        return sql_xml
    
    def get_fixed_json(self, text : str) -> str:
        """
            Extract JSON from text
        """
        text = text.replace(", ]", "]").replace(",]", "]").replace(",\n]", "]")
        
        # check if JSON is in code block
        if '```json' in text:
            open_bracket = text.find('```json')
            close_bracket = text.rfind('```')
            if open_bracket != -1 and close_bracket != -1:
                return text[open_bracket+7:close_bracket].strip()
        
        # check if JSON is in brackets
        tmp_text = text.replace("{", "[").replace("}", "]")
        open_bracket = tmp_text.find('[')
        if open_bracket == -1:
            return text
                
        close_bracket = tmp_text.rfind(']')
        if close_bracket == -1:
            return text
        
        return text[open_bracket:close_bracket+1]

    def clear_cache(self):
        """
            Clear cache
        """
        llm_cache = get_llm_cache()
        if llm_cache:
            llm_cache.clear()
        
    
