import streamlit as st
import geopandas as gpd
import numpy as np
from ports.project_data import ProjectDataPort
from domain.building_project import BuildingProject
from domain.building_profile import BuildingProfile
from utils.session_state_names import PROJECT_DATA

session = st.session_state

class BAGProjectAdapter(ProjectDataPort):
    """ Adapter to load project data from an excel file with only very basic data."""
    
    def __init__(self, file_path):
        self.file_path = file_path

    def load_project_data(self) -> gpd.GeoDataFrame:
        """ Load data from an excel file and return a list of building profiles."""
        try:
            gdf_bag = gpd.read_file(self.file_path)
            gdf_bag = gdf_bag.sample(n=200).reset_index(drop=True)
            print(gdf_bag.head())
            gdf_bag["transform"] = "Sloop"
            # create some random categories for the buildings.
            gdf_bag["use"] = np.random.choice(
                ["Apartment", "Office", "Low-Rise"], size=len(gdf_bag)
            )
            return gdf_bag

        except FileNotFoundError:
            print("File not found")

    def save_to_cache(self, cache_name: str, project_data: gpd.GeoDataFrame):
        """ Save building profiles to cache."""
        st.session_state[cache_name] = project_data
        print("Saved profile to cache")

    def save_project_data(self, project_data: gpd.GeoDataFrame):
        """ Save a list of building profiles to an excel file."""
        pass
        