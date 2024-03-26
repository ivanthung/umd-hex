import pathlib
import pandas as pd
import streamlit as st
from adapters.data import building_data_repository_xls as bdr_xls
from core import service, domain
from utils import page_components, logger

session = st.session_state
BASE_DIR = pathlib.Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
BUILDING_DATA_DIR = DATA_DIR / "buildings"

def load_service():
    """Loads the service in the session state."""
    print("wut?")
    if "service" not in session:

        progress_bar = st.progress(0)
        status_text = st.empty()

        def update_progress(loaded_files, total_files, resource_name):
            progress = loaded_files / total_files
            progress_bar.progress(progress)
            status_text.text(f"Loaded {resource_name}...")
        
        building_repository = bdr_xls.BuildingDataRepositoryXls(
            [
                bdr_xls.PersistedData(
                    filepath=DATA_DIR / "gebouwprofielen.xlsx",
                    resource=domain.Resource.BuildingProfileSummary,
                ),
                bdr_xls.PersistedData(
                    filepath=DATA_DIR
                    / "bag"
                    / "jpk"
                    / "/Users/ivanthung/code/umd_mockup_hex/data/bag/jpk/jpk_bag_pand.shp",
                    resource=domain.Resource.BuildingProject,
                ),
                bdr_xls.PersistedData(
                    filepath= BUILDING_DATA_DIR
                    / "Urban Mining Model Future.xlsx", 
                    resource=domain.Resource.BuildingProfileFutureImpacts,
                ),
                bdr_xls.PersistedData(
                    filepath= BUILDING_DATA_DIR
                    / "Urban Mining Model Future Materials.xlsx", 
                    resource=domain.Resource.BuildingProfileFutureMaterials,
                ),
                bdr_xls.PersistedData(
                    filepath= BUILDING_DATA_DIR
                    / "Urban Mining Model Standard.xlsx", 
                    resource=domain.Resource.BuildingProfileStandardImpacts,
                ),
                bdr_xls.PersistedData(
                    filepath= BUILDING_DATA_DIR
                    / "Urban Mining Model Materials.xlsx", 
                    resource=domain.Resource.BuildingProfileStandardMaterials,
                )
            ],
            progress_callback=update_progress,
        )

        session.service = service.Service(building_repository)
        session.service.add_missing_fields(
            [domain.Resource.BuildingProject, domain.Resource.BuildingProfileSummary]
        )

        status_text.text("Data loaded successfully!")


if __name__ == "__main__":
    page_components.set_page_title("Building Profile Editor")
    logger = logger.get_logger(__name__)
    logger.info(f"Re-initialising service at {pd.Timestamp.now()}")
    load_service()
