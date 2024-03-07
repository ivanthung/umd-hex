import streamlit as st
import pandas as pd
import geopandas as gpd
from core import ports, domain
from utils import project_config
import folium
from streamlit_folium import st_folium

class StreamlitBuildingProfileInterface(ports.BuildingProfileInterface):
    """ Streamlit implementation of the building profile interface. Each method loads the building profiles from the cache if it exist."""
    def __init__(self, service: ports.Service):
        self.service = service

    def edit_profile(self, columns = {}) -> pd.DataFrame:
        """Edit data with a simple interface. Atm only edits impact m2.
        We could give it a dict to determine what columns to edit.
        Perhaps make this more general later"""
        
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
                    building_profile.impact_m2 = col2.number_input("Impact m2", value=building_profile.impact_m2, key = key)
                    
                    if(self.service.validate_profile(building_profile)):
                        building_profiles.loc[i] = building_profile.to_dict()
                        self.service.save(domain.Resource.BuildingProfile, building_profiles)
        
        if save_button.button("Save"):
            if(self.service.save(domain.Resource.BuildingProfile, building_profiles, to_file=True)):
                save_button.success("Building profiles saved")

    def pretty_display(self, resource: domain.Resource) -> pd.DataFrame:
        """ Display building profiles."""
        
        local_data = self.service.get_building_data(resource)
        st.write(local_data.head())
    
    @st.cache_data(experimental_allow_widgets=True)
    def map(_self, resource: domain.Resource, _map_config: domain.MapConfig):
        """ Shows map of project data"""
        
        match resource: 
            case domain.Resource.BuildingProject:
                gdf = _self.service.get_building_data(domain.Resource.BuildingProject)
                gdf = gdf.head(50)
                m = folium.Map(location = _map_config.geo.location,
                                zoom_start = _map_config.geo.zoom,
                                tiles = _map_config.geo.tiles)
                folium.GeoJson(
                    gdf,
                    popup=folium.GeoJsonPopup(
                        fields=_map_config.geo.popup_fields,
                    ),
                ).add_to(m)
                st_folium(m, use_container_width=True)
            
