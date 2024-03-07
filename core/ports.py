# ports/building_data_port.py
from abc import ABC, abstractmethod
from core import domain
import pandas as pd
import geopandas as gpd
from core import domain

class BuildingDataRepository(ABC):
    @abstractmethod
    def save(self, resource: domain.Resource, data: pd.DataFrame | gpd.GeoDataFrame) -> bool:
        """Save a list of building profiles."""
        
    @abstractmethod
    def get_all(self, resource: domain.Resource) -> pd.DataFrame | gpd.GeoDataFrame:
        """ Returns full dataframe"""

    @abstractmethod
    def add_profile(self, profile: pd.DataFrame | gpd.GeoDataFrame):
        """ Add a new profile to the repository"""
        pass

class ImpactDataRepository(ABC):
    @abstractmethod
    def save(self, resource: domain.Resource, data: pd.DataFrame | gpd.GeoDataFrame) -> bool:
        """Save a list of building profiles."""
        
    @abstractmethod
    def get_all(self, resource: domain.Resource) -> pd.DataFrame | gpd.GeoDataFrame:
        """ Returns full dataframe"""

class Service(ABC):
    @abstractmethod
    def add_building_data(self, building_profile: domain.BuildingProfile):
        """Add a building profile to the list of building profiles."""
    
    @abstractmethod
    def get_building_data(self, resource: domain.Resource) -> pd.DataFrame:
        """Get building data from the repository."""
    
    @abstractmethod
    def save(self, resource: domain.Resource, to_file: bool) -> bool:
        """Save a list of building profiles."""


class BuildingProfileInterface(ABC):
    """ Streamlit implementation of the building profile interface. Each method loads the building profiles from the cache if it exist."""

    @abstractmethod
    def edit_profile(self) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def pretty_display(self, resource: domain.Resource) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def map(self) -> None:
        """ Shows map of project data"""
    