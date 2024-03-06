from abc import ABC, abstractmethod

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
