"""
    App UI utils functions
"""
# pylint: disable=C0301,C0103,C0303,C0411,W1203

import streamlit as st
import logging

from backend.core import Core
from backend.classes.messages_result import MessagesResult

from utils.utils_streamlit import streamlit_hack_remove_top_space, streanlit_hide_main_menu

logger : logging.Logger = logging.getLogger(__name__)

USER = "user"
ASSISTANT = "assistant"
AI = "ai"

def init_core():
    """Init core"""

    if 'backend_core_init' not in st.session_state or st.session_state.backend_core_init != str(Core.__init__.__code__):
        if 'backend_core' in st.session_state:
            _tmp = st.session_state.backend_core
            del _tmp
        st.session_state.clear()
        
        all_secrets = {s[0]:s[1] for s in st.secrets.items()}
        st.session_state.backend_core = Core(all_secrets)
        st.session_state.backend_core_init = str(Core.__init__.__code__)

def set_page_header(page_header_str : str):
    """
        Set page header
    """
    header_str = f"{page_header_str}"
    st.set_page_config(page_title= header_str, layout="wide")
    #st.title(header_str)

    streamlit_hack_remove_top_space()
    streanlit_hide_main_menu()

def draw_side_bar():
    """
        Draw side bar
    """    
    if 'token_count_information' not in st.session_state:
        st.session_state.token_count_information = ""

    with st.sidebar:
        with st.container(border=True):
            st.markdown(st.session_state.token_count_information)
            
        if st.button("Clear cache", use_container_width=True):
            if st.session_state.backend_core:
                core : Core = st.session_state.backend_core
                core.clear_llm_cache()
                

def show_used_tokens(currently_used_tokens : int = -1, currently_used_tokens_cost : float = 0.0):
    """Show token counter"""
    if 'current_tokens' not in st.session_state:
        st.session_state.current_tokens = 0
    if 'tokens' not in st.session_state:
        st.session_state.tokens = 0
    if 'cost' not in st.session_state:
        st.session_state.cost = 0.00
    
    if currently_used_tokens > 0:
        st.session_state.current_tokens = currently_used_tokens
        st.session_state.tokens += currently_used_tokens
        st.session_state.cost   += currently_used_tokens_cost
        
    st.session_state.token_count_information = f'Used {st.session_state.current_tokens} tokens.\n\nTotal used {st.session_state.tokens} tokens.\n\nTotal cost ${st.session_state.cost:.4f}.'
    
def report_messages(message_list : MessagesResult, st_messages : any, st_debug_messages : any):
    """Report messages"""
    
    show_used_tokens(message_list.used_tokens, message_list.used_cost)
    
    if message_list.messages:
        for message in message_list.messages:
            st_messages.append([AI, message])
    if message_list.debugs:
        for debug in message_list.debugs:
            st_debug_messages.append(debug)
    if message_list.errors:
        for error in message_list.errors:
            st_debug_messages.append(error)

def convert_to_radio_buttons(topic_list : list[str]) -> list[str]:
    """Convert to radio buttons"""
    radio_buttons_list = []
    for topic_str in topic_list:
        topic_str_encoded = topic_str.replace("'", "&apos;")
        radio_buttons_list.append(f"<input type='radio' name='topic' value='{topic_str_encoded}'> {topic_str_encoded}")
    return radio_buttons_list
