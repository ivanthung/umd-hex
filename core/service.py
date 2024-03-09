from dataclasses import fields
from typing import get_type_hints
import pandas as pd
import geopandas as gpd
from core import domain, ports

class Service(ports.Service):    
    def __init__(self, building_data_repository: ports.DataRepository):
        self.building_data_repository = building_data_repository
        
    def get_building_data(self, resource: domain.Resource) -> pd.DataFrame:
        """Get building data from the repository."""
        return self.building_data_repository.get_all(resource)
    
    def add_building_data(self, building_profile: domain.BuildingProfile):
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
            
            self.building_data_repository.save(resource, df, to_file=False)
        
    def validate_profile(self, building_profile: domain.BuildingProfile):
        """Validate a building profile."""
        return True
    
    def save(self, resource: domain.Resource, data: pd.DataFrame | gpd.GeoDataFrame, to_file = False):
        """Save a list of building profiles."""
        return self.building_data_repository.save(resource, data, to_file)