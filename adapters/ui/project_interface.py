import streamlit as st
from ports.ui.building_project_interface import BuildingProjectInterface
from domain.building_project import BuildingProject

session = st.session_state

class StreamlitProjectInterface(BuildingProjectInterface):
    """Streamlit interface for building profiles.
    """
    def create_edit_interface(self, building_profiles: list[BuildingProject]):
        """Interface to edit building profiles."""
        pass

    def create_pretty_display(self, building_profiles: list[BuildingProject]):
        """Display building profiles."""
        for profile in building_profiles:
            st.write(profile.describe())
        pass
    
    def create_save_interface(self, building_profiles: list[BuildingProject], building_data_port: BuildingProject):
        """Interface to save building profiles to a data port."""
        pass

    def save_to_cache(self, cache_name: str, building_profiles: list[BuildingProject]):
        """Save building profiles to cache."""
        pass
