import pandas as pd
from ports.building_data import BuildingDataPort
from domain.building_profile import BuildingProfile


class XLSBuildingProfileDataAdapter(BuildingDataPort):
    """ Adapter to load building profiles from an excel file with only very basic data."""
    
    def __init__(self, file_path):
        self.file_path = file_path

    def load_building_profiles(self) -> pd.DataFrame:
        """ Load data from an excel file and return a list of building profiles."
        Potentially add validatin here. """

        building_profiles = pd.read_excel(self.file_path)
        
        return building_profiles
    
    
    
    def save_building_profiles(self, building_profiles: pd.DataFrame):
        """ Save a list of building profiles to an excel file."""
        
        building_profiles.to_excel(self.file_path, index=False)

