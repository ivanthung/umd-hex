""" Streamlit page to edit building profiles. Session state handeling remains on the level of the interface class."""

import streamlit as st

from utils import page_components as page
from adapters.data.building_profile_data_adapter import XLSBuildingProfileDataAdapter
from adapters.ui.building_profile_interface import StreamlitBuildingProfileInterface
from utils import page_components as page
from utils.session_state_names import BUILDING_PROFILES

xls_adapter = XLSBuildingProfileDataAdapter("data/gebouwprofielen.xlsx")
profile_interface = StreamlitBuildingProfileInterface()
building_profiles = xls_adapter.load_building_profiles()

page.set_page_title("Pas gebouwprofiel aan")
# Editing interface
col1, col2 = st.columns(2)
with col1:
    building_profiles = profile_interface.create_edit_interface(building_profiles)
    profile_interface.save_to_cache(BUILDING_PROFILES, building_profiles)
    profile_interface.create_pretty_display(building_profiles)

with col2:
    profile_interface.create_save_interface(building_profiles, xls_adapter)