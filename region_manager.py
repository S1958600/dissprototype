from region_struct import Region
from region_struct import Habitability

class RegionManager:
    def __init__(self, statements):
        self.statements = statements
        self.regions = self.generate_all_regions()
        self.valid = True  # Initialise valid status to True
    
    def generate_all_regions(self):
        regions = {} # regions is a dictionary with keys as tuples of booleans and values as Region objects
        for in_a in [True, False]:
            for in_b in [True, False]:
                for in_c in [True, False]:
                    region = Region(in_a, in_b, in_c)
                    regions[region.get_sets_tuple()] = region # key is the region's tuple signature
        return regions
    
    def set_habitability(self, region_tuple, status):
        if region_tuple in self.regions:
            if isinstance(status, Habitability):
                self.regions[region_tuple].habitable = status
            else:
                raise ValueError(f"Invalid habitability status: {status}")
        else:
            raise ValueError(f"Unrecognised region: {region_tuple}")
    
    def get_habitability(self, region_tuple):
        if region_tuple in self.regions:
            return self.regions[region_tuple].habitable
        else:
            raise ValueError(f"Unrecognised region: {region_tuple}")
    
    def get_all_regions(self):
        return self.regions
    
    def add_statement(self, statement):
        self.statements.append(statement)
    
    def set_validity(self, status):
        if isinstance(status, bool):
            self.valid = status
        else:
            raise ValueError(f"Invalid validity status: {status}")
    
    def is_valid(self):
        return self.valid