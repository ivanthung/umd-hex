import streamlit as st
import pandas as pd
import geopandas as gpd
from copy import deepcopy
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
        building_profiles = self.service.get_building_data(domain.Resource.BuildingProfileSummary)

        # Expanders for each building type
        for building_type in building_profiles.building_type.unique():
            with st.expander(building_type):

                for  i, profile in building_profiles[building_profiles['building_type'] == building_type].iterrows():
                    building_profile = domain.BuildingProfileSummary(**profile.to_dict())
                    key = f"{i}-impact"
                    col1, col2 = st.columns((1,2))
                    col1.write(building_profile.building_sub_type)                                
                    building_profile.impact_m2 = col2.number_input("Impact m2", value=building_profile.impact_m2, key = key)
                    
                    if(self.service.validate_profile(building_profile)):
                        building_profiles.loc[i] = building_profile.to_dict()
                        self.service.save(domain.Resource.BuildingProfileSummary, building_profiles)
        
        if save_button.button("Save"):
            if(self.service.save(domain.Resource.BuildingProfileSummary, building_profiles, to_file=True)):
                save_button.success("Building profiles saved")

    def pretty_display(self, resource: domain.Resource) -> pd.DataFrame:
        """ Display building profiles."""
        
        local_data = self.service.get_building_data(resource)
        st.write(local_data.head())
    
    def editable_table(self, resource: domain.Resource, columns: domain.FieldsEditConfig):
        """ Editable table for profiles and projects.
        Include column config to determine which ones to show and which one to edit.
        """
        col1, col2 = st.columns(2)

        df = deepcopy(self.service.get_building_data(str(resource)))
        all_columns = columns.fixed+columns.variable

        match resource:
            case domain.Resource.BuildingProject:

                # Completely stupid implementation of the column config. ToDo: column_config generator.                
                # Also, doesn't work yet for the BuildingProfiles.
                
                profile_data = self.service.get_building_data(str(domain.Resource.BuildingProfileSummary))
                options = profile_data['building_type'].unique()
                column_config =  {
                    field: st.column_config.SelectboxColumn(
                        options= options,
                        required=False,
                    ) for field in columns.variable}
                       
        _df = st.data_editor(df[all_columns], column_config=column_config)
        df[all_columns] = _df

        if col1.button("Save changes to file"):
            if(self.service.save(resource, df, to_file=True)):
                col2.success(f"{resource} saved")

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
            
