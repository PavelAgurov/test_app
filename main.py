"""
    Main
"""
# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,W1203

import logging

import streamlit as st

from backend.core import Core
from streamlit_backend import app_utils
from utils.app_logger import init_streamlit_logger

init_streamlit_logger()

# ------------------------------- Core
app_utils.init_core()

logger : logging.Logger = logging.getLogger()
core   : Core = st.session_state.backend_core

# ------------------------------- UI

app_utils.set_page_header("PDF Description")
app_utils.draw_side_bar()
app_utils.show_used_tokens()

if st.button("Test connection"):
    core.test_connection()
    st.success("Connection successful")

with st.form("my-form", clear_on_submit=True, border=True):
    document = st.file_uploader(
        "Drag PDF documents here (PDF format)",
        type=["pdf"],
        accept_multiple_files=False,
    )
    is_upload_triggered = st.form_submit_button("Upload selected documents")

if is_upload_triggered:
    if not document:
        st.warning("No document selected for upload")
        st.stop()

if not document:
    st.stop()

pdf_content = document.read()

if st.button("Analyze PDF"):
    pdf_description = core.create_pdf_description(pdf_content)
    st.markdown(pdf_description)