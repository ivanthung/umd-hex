from dataclasses import dataclass
import pathlib
import pandas as pd
import geopandas as gpd


from core import ports
from core import domain


@dataclass
class PersistedData:
    filepath: pathlib.Path
    resource: domain.Resource

class BuildingDataRepositoryXls(ports.BuildingDataRepository):
    """ Adapter to load building profiles from an excel file with only very basic data."""
    
    def __init__(self, local_data: list[PersistedData]):
        cached_data: dict[str, pd.DataFrame | gpd.GeoDataFrame] = dict()
        self.filepath = { str(data.resource): data.filepath for data in local_data }
        
        for data in local_data:
            match data.resource:
                case domain.Resource.BuildingProject:
                    cached_data[str(data.resource)] = gpd.read_file(data.filepath)
                
                case domain.Resource.BuildingProfile:
                    cached_data[str(data.resource)] = pd.read_excel(data.filepath)
        
        self.cached_data = cached_data

    def get_all(self, resource: domain.Resource.BuildingProject):
        """ Returns dataframe of the resource"""
        return self.cached_data[str(resource)]
    
    def add_profile(self, profile: pd.DataFrame):
        """ Add a new profile to the repository. Check if this works"""
        _temp = pd.concat([self.cached_data[str(domain.Resource.BuildingProfile)], profile])
        self.save(domain.Resource.BuildingProfile, _temp)


    def save(self, resource: domain.Resource, data: pd.DataFrame | gpd.GeoDataFrame, to_file: bool):
        """ Save a list of building profiles to an excel file."""
        if to_file:
            try:
                match resource:
                    case domain.Resource.BuildingProject:
                        data.to_file(self.filepath[str(resource)], index=False)
                    
                    case domain.Resource.BuildingProfile:
                        data.to_excel(self.filepath[str(resource)], index=False)
            
            except FileNotFoundError:
                print("File not found")
                return False
            
            except Exception as e:
                print(e)
                return False
            print("Saved to: ", self.filepath[str(resource)])
        
        self.cached_data[str(resource)] = data
        return True
