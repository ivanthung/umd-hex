""" Streamlit page to edit building profiles. Session state handeling remains on the level of the interface class."""
import streamlit as st
from app import load_service
from utils import page_components as page
from utils import project_config, logger
from core import domain
from adapters.ui.building_profile_interface import StreamlitBuildingProfileInterface

logger = logger.get_logger(__name__)


page.set_page_title("Laad project data", divider = False)
load_service()

session = st.session_state
interface = StreamlitBuildingProfileInterface(session.service)

# Improve this way of creating the MapConfig
edit_config = domain.FieldsEditConfig(**project_config.project_data["fields_edit"])

tab1, tab2 = st.tabs(["Individueel gebouw", "Gebouwenlijst"])


# The below is some code that still needs to be improved that will enable us to cycle through the buildings.
# This is not finished yet, needs another 1-2 hr of work.
# Change the display building data by map interaction to display the building data by building ID.
# Change the service so it gets the building lovation by building ID.
# Get the ID by map interaction data. 

if 'restore_default_map' not in session:
    session.restore_default_map = True
    session.map_config = domain.MapConfig(
    geo=domain.GeoConfig(**project_config.project_data["geo"]),
    fields_edit= edit_config)

if not session.restore_default_map:
    coordinates = session.service.get_centre_point_of_building(domain.Resource.BuildingProject, 0)
    map_config = domain.MapConfig(
        geo=domain.GeoConfig(location=coordinates, zoom=17, tiles="Cartodb Positron", popup_fields=["end_use"]),
        fields_edit= edit_config
    )


with tab1:
    col1, col2 = st.columns(2)
    with col1:
        map_interaction_data = interface.map(domain.Resource.BuildingProject, session.map_config)
    
    with col2:
        display_fields = ["bouwjaar", "gebruiksdo", "oppervlakt", "end_use"]
        interface.display_building_data_by_map_interaction(domain.Resource.BuildingProject, map_interaction_data, display_fields)
        if st.button("Next building"):
            st.write("Cycle to the next building")

with tab2:
    interface.editable_table(domain.Resource.BuildingProject, edit_config)
    
        


