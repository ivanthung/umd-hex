from abc import ABC, abstractmethod
from domain.building_project import BuildingProject

class ProjectDataPort(ABC):
    @abstractmethod
    def load_project_data(self) -> list[BuildingProject]:
        """Load project data."""
        pass

    @abstractmethod
    def save_to_cache(self, cache_name: str, project_data: list[BuildingProject]):
        """Save project data to cache."""
        pass
    
    @abstractmethod
    def save_project_data(self, project_data: list[BuildingProject]):
        """Save project data."""
        pass