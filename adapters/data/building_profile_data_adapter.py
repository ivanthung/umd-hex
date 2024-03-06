import pandas as pd
from ports.building_data import BuildingDataPort
from domain.building_profile import BuildingProfile


class XLSBuildingProfileDataAdapter(BuildingDataPort):
    """ Adapter to load building profiles from an excel file with only very basic data."""
    
    def __init__(self, file_path):
        self.file_path = file_path

    def load_building_profiles(self) -> list[BuildingProfile]:
        """ Load data from an excel file and return a list of building profiles."""
        building_profiles = []
        data = pd.read_excel(self.file_path)
        for i, row in data.iterrows():
            building_profiles.append(
                BuildingProfile(
                    {
                        "name": row["building_type"],
                        "building_type": row["building_type"],
                        "building_sub_type": row["building_sub_type"],
                        "impact_m2": int(row["impact_m2"]),
                    }
                )
            )
        
        return building_profiles
    
    def save_building_profiles(self, building_profiles: list[BuildingProfile]):
        """ Save a list of building profiles to an excel file."""
        building_profiles_df = pd.DataFrame(
            [
                {
                    "building_type": profile.building_type,
                    "building_sub_type": profile.building_sub_type,
                    "impact_m2": profile.impact_m2['CO2'],
                }
                for profile in building_profiles
            ]
        )
        print(building_profiles_df)
        building_profiles_df.to_excel(self.file_path, index=False)

