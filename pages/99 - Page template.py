""" Streamlit page to edit building profiles. Session state handeling remains on the level of the interface class."""
import streamlit as st
from app import load_service
from utils import page_components as page
from utils import logger
from core import domain
from adapters.ui.building_profile_interface import StreamlitBuildingProfileInterface

logger = logger.get_logger(__name__)

page.set_page_title("Laad project data", divider = False)
load_service()

session = st.session_state
interface = StreamlitBuildingProfileInterface(session.service)

standard_impacts = session.service.get_building_data(domain.Resource.BuildingProfileStandardImpacts)
standard_materials = session.service.get_building_data(domain.Resource.BuildingProfileStandardMaterials)
future_impacts = session.service.get_building_data(domain.Resource.BuildingProfileFutureImpacts)
future_materials = session.service.get_building_data(domain.Resource.BuildingProfileFutureMaterials)

st.write(standard_impacts.head())
st.write(standard_materials.head())
st.write(future_impacts.head())
st.write(future_materials.head())