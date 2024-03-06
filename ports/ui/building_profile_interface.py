from abc import ABC, abstractmethod
from domain.building_profile import BuildingProfile
from ports.building_data import BuildingDataPort

class BuildingProfileInterface(ABC):
    
    @abstractmethod
    def create_edit_interface(self, building_profiles: list[BuildingProfile]):
        """Interface to edit building profiles."""
        pass

    @abstractmethod
    def create_pretty_display(self, building_profiles: list[BuildingProfile]):
        """Display building profiles."""
        pass
    
    @abstractmethod
    def create_save_interface(self, building_profiles: list[BuildingProfile], building_data_port: BuildingDataPort):
        """Interface to save building profiles to a data port."""
        pass

    @abstractmethod
    def save_to_cache(self, cache_name: str, building_profiles: list[BuildingProfile]):
        """Save building profiles to cache."""
        pass
