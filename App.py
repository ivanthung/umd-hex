import pathlib
import pandas as pd
import streamlit as st
from adapters.data import building_data_repository_xls
from core import service, domain
from utils import page_components, logger

logger = logger.get_logger(__name__)


session = st.session_state
BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

def load_service():
    """Loads the service in the session state."""
    
    with st.spinner("Loading data..."):
        if 'service' not in session:
            logger.info(f"Re-initialising service at {pd.Timestamp.now()}")
            print("testing logger")
            
            building_repository = building_data_repository_xls.BuildingDataRepositoryXls(
            [building_data_repository_xls.PersistedData(filepath = DATA_DIR / "gebouwprofielen.xlsx", resource = domain.Resource.BuildingProfileSummary),
            building_data_repository_xls.PersistedData(filepath = DATA_DIR / "bag" / "bag-ams-zuidoost-platdak-buurt.shp", resource = domain.Resource.BuildingProject)
            ]
            )
            session.service = service.Service(building_repository)
            session.service.add_missing_fields([domain.Resource.BuildingProject, domain.Resource.BuildingProfileSummary])

if __name__ == "__main__":
    page_components.set_page_title("Building Profile Editor")
    load_service()
