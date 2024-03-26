""" Streamlit page to edit building profiles. Session state handeling remains on the level of the interface class."""
import streamlit as st
from utils import page_components as page
from utils import logger
from adapters.ui.building_profile_interface import StreamlitBuildingProfileInterface
from app import load_service
from core import domain

logger = logger.get_logger(__name__)
page.set_page_title("Pas gebouwprofiel aand")
load_service()

session = st.session_state
interface = StreamlitBuildingProfileInterface(session.service)

col1, col2 = st.columns(2)
with col1:
    interface.edit_profile()
with col2:
    interface.pretty_display(domain.Resource.BuildingProfileSummary)
