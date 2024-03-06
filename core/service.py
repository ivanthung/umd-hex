from core import domain, ports
import pandas as pd

class Service(ports.Service):    
    def __init__(self, building_data_repository: ports.BuildingDataRepository):
        self.building_data_repository = building_data_repository
        
    def get_building_data(self, resource: domain.Resource) -> pd.DataFrame:
        """Get building data from the repository."""
        return self.building_data_repository.get_all(resource)
    
    def add_building_data(self, building_profile: domain.BuildingProfile):
        """Add a building profile to the list of building profiles."""
        self.building_data_repository.add_profile(building_profile)
    
    def validate_profile(self, building_profile: domain.BuildingProfile):
        """Validate a building profile."""
        return True
    
    def save(self, building_profiles: pd.DataFrame):
        """Save a list of building profiles."""
        return self.building_data_repository.save(domain.Resource.BuildingProfile, building_profiles)