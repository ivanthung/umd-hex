import pathlib
import streamlit as st
from adapters.data import building_data_repository_xls
from core import service, domain
from utils import page_components as page
from adapters.ui.building_profile_interface import StreamlitBuildingProfileInterface

session = st.session_state

BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def load_service():
    """Loads the service in the session state."""
    if 'service' not in session:
        building_repository = building_data_repository_xls.BuildingDataRepositoryXls(
        [building_data_repository_xls.PersistedData(filepath = DATA_DIR / "gebouwprofielen.xlsx", resource = domain.Resource.BuildingProfile),
        building_data_repository_xls.PersistedData(filepath = DATA_DIR / "bag" / "bag-ams-zuidoost-platdak-buurt.shp", resource = domain.Resource.BuildingProject)
        ]
        )
        session.service = service.Service(building_repository)

if __name__ == "__main__":
    load_service()

    page.set_page_title("Building Profile Editor")
    st.write("Welcome to this wonderful app")
