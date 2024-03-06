import streamlit as st
import pandas as pd
from core import ports, domain

class StreamlitBuildingProfileInterface(ports.BuildingProfileInterface):
    """ Streamlit implementation of the building profile interface. Each method loads the building profiles from the cache if it exist."""
    def __init__(self, service: ports.Service):
        self.service = service

    def create_edit_interface(self) -> pd.DataFrame:
        
        def clear(key):
            """ Helper function to clear the session state."""
            st.session_state.pop(key, None)

        save_button = st.container()
        building_profiles = self.service.get_building_data(domain.Resource.BuildingProfile)

        # Expanders for each building type
        for building_type in building_profiles.building_type.unique():
            with st.expander(building_type):

                for  i, profile in building_profiles[building_profiles['building_type'] == building_type].iterrows():
                    building_profile = domain.BuildingProfile(**profile.to_dict())
                    key = f"{i}-impact"
                    col1, col2 = st.columns((1,2))
                    col1.write(building_profile.building_sub_type)
                    building_profile.impact_m2 = col2.number_input("Impact m2", value=building_profile.impact_m2, key = key, on_change=clear, args=(key,))
                    if(self.service.validate_profile(building_profile)):
                        building_profiles.loc[i] = building_profile.to_dict()
        
        if save_button.button("Save"):
            if(self.service.save(building_profiles)):
                save_button.success("Building profiles saved")

    def create_pretty_display(self, building_profiles: pd.DataFrame) -> pd.DataFrame:
        """ Display building profiles."""
        
        for i, profile in building_profiles.iterrows():
            building_profile = domain.BuildingProfile(**profile.to_dict())
            st.write(building_profile)
    
    def create_save_interface(self, building_profiles: pd.DataFrame):
        """ Interface to save building profiles to a data port."""
        
        if st.button("Save building profile"):
            """ Save building profiles to the repository."""