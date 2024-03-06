import streamlit as st
from ports.ui.building_project_interface import BuildingProjectInterface
from domain.building_project import BuildingProject
from ports.project_data import ProjectDataPort

session = st.session_state

class StreamlitProjectInterface(BuildingProjectInterface):
    """Streamlit interface for building profiles.
    """
    def create_edit_interface(self, building_projects: list[BuildingProject]):
        """Interface to edit building profiles."""
        pass

    def create_pretty_display(self, building_projects: list[BuildingProject]):
        """Display building profiles."""
        for profile in building_projects:
            st.write(profile.describe())
        pass
    
    def create_save_interface(self, building_projects: list[BuildingProject], building_data_port: ProjectDataPort):
        """Interface to save building profiles to a data port."""
        pass
    
    def save_to_cache(self, cache_name: str, building_projects: list[BuildingProject]):
        """ Save building profiles to cache."""
        st.session_state[cache_name] = building_projects
        print("Saved profile to cache")
    
    def load_from_cache(self, cache_name: str, building_projects: list[BuildingProject]):
        """ Load building profiles from session state cache, if it exists."""
        if cache_name in st.session_state:
            return st.session_state[cache_name]
        else:
            return building_projects