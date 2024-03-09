from domain.building_profile import BuildingProfile
from numpy import NaN
from enum import Enum, auto

class BuildingProject:
    def __init__(self, init_data: dict):
        self.location = init_data.get("location", (0, 0))
        self.current_building_use = init_data.get("current_type", BuildingProfile)
        self.current_profile_type = init_data.get("current_profile", BuildingProfile)
        self.future_profile_type = init_data.get("future_profile", BuildingProfile)
        self.address = init_data.get("address", "Unknown")
        self.image_url = init_data.get("image_url", "No URL found")
        self.transformation = init_data.get("transformation", "Unknown")
        self.age = init_data.get("age", NaN)
        self.geometry = init_data.get("geometry", NaN)
    
    def __str__(self):
        return f"Building project at {self.address} with current type {self.current_profile_type} and future type {self.future_profile_type}."
    
    def describe(self):
        return f"Building project at {self.address} with current type {self.current_profile_type} and future type {self.future_profile_type}."
    
    def update_profile_type(self, new_profile_type):
        """Updates the building type of the building project."""
        new_profile_type
      
    def update_location(self, new_location: tuple):
        """Updates the location of the building project."""
        self.location = new_location
    
    def update_transformation(self, new_transformation: str):
        """Updates the transformation of the building project"""
        self.transformation = new_transformation

class Resource(Enum):
    BuildingProject = auto()
    BuildingProfile = auto()
