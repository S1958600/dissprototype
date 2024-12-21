from region_struct import Region, Status

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
    
    def set_habitability(self, region_tuple, newStatus):
        if region_tuple in self.regions:
            if isinstance(newStatus, Status):
                self.regions[region_tuple].status = newStatus
            else:
                raise ValueError(f"Invalid habitability status: {newStatus}")
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
        
    def get_statements(self):
        return self.statements
    
    def set_validity(self, status):
        if isinstance(status, bool):
            self.valid = status
        else:
            raise ValueError(f"Invalid validity status: {status}")
    
    def is_valid(self):
        return self.valid
    
    def print_regions(self):
        for region_tuple, region in self.regions.items():
            sets = []
            sets.append('A' if region_tuple[0] else '')
            sets.append('B' if region_tuple[1] else '')
            sets.append('C' if region_tuple[2] else '')
            sets_str = ', '.join(sets)
            print(f"Region: ({sets_str}), Status: {region.status.name}")
            
    def print_statements(self):
        for statement in self.statements:
            print(statement)