""" Streamlit page to edit building profiles. Session state handeling remains on the level of the interface class."""

import streamlit as st
from utils import page_components as page

page.set_page_title("Pas gebouwprofiel aan")
# Editing interface

col1, col2 = st.columns(2)
with col1:
    st.write("Placeholder")

with col2:
    st.write("Placeholder")
    
