from abc import ABC, abstractmethod
import geopandas as gpd
import pandas as pd

class ProjectDataPort(ABC):
    @abstractmethod
    def load_project_data(self) -> gpd.GeoDataFrame:
        """Load project data."""
        pass

    @abstractmethod
    def save_to_cache(self, cache_name: str, project_data: gpd.GeoDataFrame):
        """Save project data to cache."""
        pass
    
    @abstractmethod
    def save_project_data(self, project_data: gpd.GeoDataFrame):
        """Save project data."""
        pass