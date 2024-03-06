""" Streamlit page to edit building profiles. Session state handeling remains on the level of the interface class."""

import streamlit as st
from utils import page_components as page
from utils.session_state_names import BUILDING_PROFILES
from adapters.ui.building_profile_interface import StreamlitBuildingProfileInterface
from app import load_service

page.set_page_title("Placeholder")
load_service()

session = st.session_state

interface = StreamlitBuildingProfileInterface(session.service)

col1, col2 = st.columns(2)
with col1:
    interface.create_edit_interface()
with col2:
    st.write("Placeholder")