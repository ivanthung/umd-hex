from dataclasses import dataclass
from enum import Enum, auto
from shapely.geometry import Polygon
from typing import Optional

class Resource(Enum):
    BuildingProject = auto()
    BuildingProfile = auto()
    ConstructionProducts = auto()
    MaterialImpacts = auto()

@dataclass
class BuildingProfile:
    """Data class to hold building profile data."""
    building_type: str
    building_sub_type: str
    impact_m2: float
    impact_all: Optional[dict] = None

    def __str__(self):
        return f"{self.building_type}: {self.impact_m2}"
    
    def to_dict(self):
        return {
            "building_type": self.building_type,
            "building_sub_type": self.building_sub_type,
            "impact_m2": self.impact_m2
        }

    
@dataclass
class BuildingProject:
    current_building_use: str
    current_profile_type: str
    location: tuple
    geometry: Polygon
    future_profile_type: str
    address: str
    image_url: str

    def __str__(self):
        return f"Building project with current type {self.current_profile_type} and future type {self.future_profile_type}."

@dataclass
class ConstructionProducts:
    """ Placeholders for construction products -> should be replaced with fields"""
    impact_m2: dict
    impact_all: dict

@dataclass
class MaterialImpacts:
    """ Placeholders for construction products -> should be replaced with fields"""
    impact_m2: dict
    impact_all: dict


@dataclass
class GeoConfig:
    location: tuple[float, float]
    zoom: int
    tiles: str
    popup_fields: list[str]

@dataclass
class FieldsEditConfig:
    fixed: list[str]
    variable: list[str]

@dataclass
class MapConfig:
    geo: GeoConfig
    fields_edit: FieldsEditConfig

