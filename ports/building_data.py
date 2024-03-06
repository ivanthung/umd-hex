# ports/building_data_port.py
from abc import ABC, abstractmethod
from domain.building_profile import BuildingProfile


class BuildingDataPort(ABC):
    @abstractmethod
    def load_building_profiles(self) -> list[BuildingProfile]:
        """Save a list of building profiles."""
        pass

    @abstractmethod
    def save_building_profiles(self, building_profiles: list[BuildingProfile]):
        """Save a list of building profiles."""
        pass


class MaterialDataPort(ABC):
    @abstractmethod
    def get_bill_of_materials(self, profile_name) -> dict:
        """Load a bill of materials."""
        pass

    @abstractmethod
    def get_product_composition(self, product_name) -> dict:
        """Get the composition of a construction product in terms of materials."""
        pass

    @abstractmethod
    def get_impact_factors(self, product_name) -> dict:
        """Get the impact factors for a product."""
        pass
