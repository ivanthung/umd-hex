from dataclasses import dataclass
from enum import Enum, auto
from shapely.geometry import Polygon
from typing import Optional

class Resource(Enum):
    """Enum to hold all resources with names. Some resources can share the same class."""
    
    BuildingProject = auto()
    BuildingProfileStandardMaterials = auto()
    BuildingProfileStandardImpacts = auto()
    BuildingProfileFutureMaterials = auto()
    BuildingProfileFutureImpacts = auto()
    BuildingProfileSummary = auto()
    ConstructionProducts = auto()
    MaterialImpacts = auto()
    
    @staticmethod
    def get_class(resource):
        class_mapping = {
            Resource.BuildingProject: BuildingProject,
            Resource.BuildingProfileSummary: BuildingProfileSummary,
            Resource.BuildingProfileStandardMaterials: BuildingProfileMaterials,
            Resource.BuildingProfileStandardImpacts: BuildingProfileImpacts,
            Resource.BuildingProfileFutureMaterials: BuildingProfileMaterials,
            Resource.BuildingProfileFutureImpacts: BuildingProfileImpacts
        }
        return class_mapping[resource]

@dataclass
class BuildingProfileSummary:
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
    """ Data class to hold building project data. Needs to be all 10 chars or less to be able to save it back as a shapefile"""
    use_now: str
    prof_now: str
    prof_fut: str
    end_use: str
    location: tuple
    geometry: Polygon
    address: str
    im_url: str

    def __str__(self):
        return f"Building project with current type {self.current_profile_type} and future type {self.future_profile_type}."

@dataclass
class BuildingProfileMaterials:
    """ Building profile holding construction materials and their specific impacts."""
    building_type: str
    construction_type: str
    cohort: int
    productcode: str
    product_unit: str
    fase_a_gwp_per_m2: float
    fase_a_mki_per_m2: float

@dataclass
class BuildingProfileImpacts:
    """ Placeholders for construction products -> should be replaced with fields"""
    building_type: str
    construction_type: str
    cohort: int
    productcode: str
    product_unit: str
    genericmaterialname: str
    grouped_material: str
    kg_per_m2: float

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

