""" Streamlit page to edit building profiles. Session state handeling remains on the level of the interface class."""

import streamlit as st
from app import load_service
from utils import page_components as page
from utils import project_config
from core import domain
from adapters.ui.building_profile_interface import StreamlitBuildingProfileInterface


page.set_page_title("Laad project data")
load_service()
session = st.session_state
interface = StreamlitBuildingProfileInterface(session.service)

# Improve this way of creating the MapConfig
edit_config = domain.FieldsEditConfig(**project_config.project_data["fields_edit"])
map_config = domain.MapConfig(
    geo=domain.GeoConfig(**project_config.project_data["geo"]),
    fields_edit= edit_config
)

col1, col2 = st.columns(2)
with col1: 
    interface.map(domain.Resource.BuildingProject, map_config)
with col2:
    interface.editable_table(domain.Resource.BuildingProject, edit_config)
