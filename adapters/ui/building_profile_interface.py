import streamlit as st

import pandas as pd
from ports.ui.building_profile_interface import BuildingProfileInterface
from ports.building_data import BuildingDataPort
from domain.building_profile import BuildingProfile
from utils.session_state_names import BUILDING_PROFILES

class StreamlitBuildingProfileInterface(BuildingProfileInterface):
    """ Streamlit implementation of the building profile interface. Each method loads the building profiles from the cache if it exist."""

    def create_edit_interface(self, building_profiles: pd.DataFrame) -> pd.DataFrame:
        building_profiles = self.load_from_cache(BUILDING_PROFILES, building_profiles)
        
        for  i, profile in building_profiles.iterrows():
            building_profile = BuildingProfile(profile.to_dict())

            with st.expander(building_profile.building_type + " " + building_profile.building_sub_type):
                building_profile.building_type = st.text_input("Building Type", building_profile.building_type, key = str(i)+"type")
                building_profile.building_sub_type = st.text_input("Building Sub Type", building_profile.building_sub_type, key = str(i)+"sub_type")
                building_profile.impact_m2['CO2'] = st.number_input("Impact m2", value=building_profile.impact_m2['CO2'], key = str(i)+"impact")
                # update the building profile in the dataframe here
                building_profiles.loc[i] = building_profile.to_dict()
        
        return building_profiles

    def create_pretty_display(self, building_profiles: pd.DataFrame) -> pd.DataFrame:
        """ Display building profiles."""
        building_profiles = self.load_from_cache(BUILDING_PROFILES, building_profiles)
        
        for i, profile in building_profiles.iterrows():
            building_profile = BuildingProfile(profile.to_dict())
            st.write(building_profile.describe())
    
    def create_save_interface(self, building_profiles: list[BuildingProfile], data_port: BuildingDataPort):
        """ Interface to save building profiles to a data port."""
        building_profiles = self.load_from_cache(BUILDING_PROFILES, building_profiles)
        
        if st.button("Save building profile"):
            data_port.save_building_profiles(building_profiles)
            st.write("Saved building profiles to xls")
            print(self.create_pretty_display(building_profiles))
    
    def save_to_cache(self, cache_name: str, building_profiles: list[BuildingProfile]):
        """ Save building profiles to cache."""
        st.session_state[cache_name] = building_profiles
        print("Saved profile to cache")
    
    def load_from_cache(self, cache_name: str, building_profiles: list[BuildingProfile]):
        """ Load building profiles from session state cache, if it exists."""
        if cache_name in st.session_state:
            return st.session_state[cache_name]
        else:
            return building_profiles