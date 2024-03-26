import streamlit as st
import pandas as pd
from copy import deepcopy
from core import ports, domain
import folium
from streamlit_folium import st_folium
from utils import graphics

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

    def map(_self, resource: domain.Resource, _map_config: domain.MapConfig):
        """ Shows map of project data"""
        
        match resource: 
            case domain.Resource.BuildingProject:
                gdf = _self.service.get_building_data(domain.Resource.BuildingProject)
                m = folium.Map(location = _map_config.geo.location,
                                zoom_start = _map_config.geo.zoom,
                                tiles = _map_config.geo.tiles)
                folium.GeoJson(
                    gdf,
                    popup=folium.GeoJsonPopup(
                        fields=_map_config.geo.popup_fields,
                    ),
                ).add_to(m)
                return st_folium(m, use_container_width=True)
    
    def display_building_data_by_map_interaction(self, resource: domain.Resource, map_interaction_data: dict, display_fields = []):
        """ Display building data based on the map interaction data.
        Map interaction data is a dict with the last active drawing.
        Write the building data to the screen.
        Add a config to determine which fields to show.
        ToDo: add functionality to save it back to the database.
        """
        
        try:
            selected_point_id = (
                map_interaction_data.get("last_active_drawing", {})
                .get("properties", {})
                .get("fuuid")
            )
            coords = (
                map_interaction_data.get("last_active_drawing", {})
                .get("geometry", {})
                .get("coordinates")
            )
        
        except AttributeError:
            st.write("Select a building to continue.")
            return
        
        df = self.service.get_building_data(resource)        
        data = df.loc[df["fuuid"] == selected_point_id].copy()
        
        col1, col2 = st.columns(2)
        with col1:
            st.title(selected_point_id[0:8])
            for i in display_fields:
                st.write(i, data.iloc[0][i])
            
            end_use = st.selectbox("Kies de eindbestemming van dit gebouw.",
                         ['Behouden', 'Transformatie', 'Sloop'])
            
            current_profile = st.selectbox("Kies het gebouwprofiel dat het beste bij dit gebouw past.",
                         ['Gebouw a', 'Gebouw b', 'Gebouw c'])
            
            future_profile = st.selectbox("Kies de eindbestemming van dit gebouw.",
                         ['Gebouw a', 'Gebouw b', 'Gebouw c'])
            
            # Update the data.
            data["end_use"] = end_use
            data["prof_now"] = current_profile
            data["prof_fut"] = future_profile
            
            # Changw this to the following format: A value is trying to be set on a copy of a slice from a DataFrame.
            # Try using .loc[row_indexer,col_indexer] = value instead
            

        with col2:
            fig = graphics.create_project_shape_diagram(coords)
            st.pyplot(fig, use_container_width=False)
        
        button = st.button("Save changes")
        if button:
            df.loc[df["fuuid"] == selected_point_id] = data
            self.service.save(resource, df, to_file=True)
            st.success("Changes saved")


