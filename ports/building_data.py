# ports/building_data_port.py
from abc import ABC, abstractmethod
from domain.building_profile import BuildingProfile
import pandas as pd


class BuildingDataPort(ABC):
    @abstractmethod
    def load_building_profiles(self) -> pd.DataFrame:
        """Save a list of building profiles."""
        pass

    @abstractmethod
    def save_building_profiles(self, building_profiles: pd.DataFrame):
        """Save a list of building profiles."""
        pass