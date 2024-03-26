from dataclasses import fields
import pandas as pd
import geopandas as gpd
from core import domain, ports

class Service(ports.Service):    
    def __init__(self, building_data_repository: ports.DataRepository):
        self.building_data_repository = building_data_repository
        
    def get_building_data(self, resource: domain.Resource) -> pd.DataFrame:
        """Get building data from the repository."""
        return self.building_data_repository.get_all(resource)
    
    def add_building_data(self, building_profile: domain.BuildingProfileSummary):
        """Add a building profile to the list of building profiles."""
        self.building_data_repository.add_profile(building_profile)
    
    def add_missing_fields(self, resources: list[domain.Resource]):
        """Preprocess data by adding missing columns"""
        for resource in resources:
            selected_class = domain.Resource.get_class(resource)
            field_names = [field.name for field in fields(selected_class)]
            df = self.building_data_repository.get_all(resource)
            unique_columns = set((list(df.columns) + field_names))    
            df = df.reindex(columns=unique_columns, fill_value='')
            self.building_data_repository.save(resource, df, to_file=True)
    
    def get_centre_point_of_building(self, resource: domain.BuildingProject,
                                     building_row: str,
                                     target_crs ='EPSG:4326') -> tuple[float, float]:
        """Get the centre point of a building."""
        gdf = self.building_data_repository.get_all(resource)
        geometry = gdf.loc[building_row, 'geometry']
        temp_gdf = gpd.GeoDataFrame(geometry=[geometry], crs=gdf.crs)
        reprojected_gdf = temp_gdf.to_crs(target_crs)
        reprojected_geometry = reprojected_gdf.geometry[0]
        centroid = reprojected_geometry.centroid
        centroid_coords = (centroid.y, centroid.x)
    
        return centroid_coords
        
    def validate_profile(self, building_profile: domain.BuildingProfileSummary):
        """Validate a building profile."""
        return True
    
    def save(self, resource: domain.Resource, data: pd.DataFrame | gpd.GeoDataFrame, to_file = False):
        """Save a list of building profiles."""
        return self.building_data_repository.save(resource, data, to_file)