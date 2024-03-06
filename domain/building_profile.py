import math
from ports.material_data import MaterialDataPort

""" Hosts the model of the building profiles, including self-updating methods."""


class BuildingProfile:
    material_data_port = None 

    @classmethod
    def set_material_data_port(cls, port: MaterialDataPort):
        cls.material_data_port = port
    
    def __init__(self, init_data):
        self.name = init_data.get("name", "no_name")
        self.building_type = init_data.get("building_type", "no_building_type")
        self.building_sub_type = init_data.get(
            "building_sub_type", "no_building_sub_type"
        )
        self.split = init_data.get("split", {})
        self.min_m2 = init_data.get("min_m2", 0)
        self.description = init_data.get("description", "no_description")
        self.bill_of_materials = init_data.get("bill_of_materials", {})
        self.bill_of_products = init_data.get("bill_of_products", {})
        self.impact_m2 = dict(CO2=init_data.get("impact_m2", 0))

    def describe(self):
        return f"{self.building_type}: {self.impact_m2['CO2']}"

    def initiate_material_data_port(self, material_data_port: MaterialDataPort):
        """Initializes the material data port for the building profile."""
        self.material_data_port = material_data_port

    def update_bill_of_materials(self):
        """Creates a new bill of materials for the building profile based on the bill of products.
        Uses an external database to find the materials for products and their properties"""
        if BuildingProfile.material_data_port:
            self.bill_of_materials = BuildingProfile.material_data_port.get_bill_of_materials(
                self.name
            )
        pass

    def update_impact_m2(self):
        """Creates a new bill of materials for the building profile based on the bill of products.
        Uses an external database to find the materials for products and their properties"""
        if BuildingProfile.material_data_port and self.bill_of_materials:
            impact_table = BuildingProfile.material_data_port.get_impact_table()
            print("Updating impact m2 here with external data")
        pass

    def update_split(self, new_split: dict):
        """Updates the split of the building use (e.g. office, woningen, etc.
        in the building profile. The split should be a dictionary with the building uses as keys and the percentage
        of the building that should be used for that purpose as values.
        """
        sum_new_values = sum(new_split.values())
        if math.isclose(sum_new_values, 1, abs_tol=0.0001):
            self.split = new_split
            return True
        print("Sum of new values is not 1")
        return False
