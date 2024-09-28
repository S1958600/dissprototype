class Region:
    def __init__(self, in_a=False, in_b=False, in_c=False, habitable=None, populated=None):
        self.in_a = in_a
        self.in_b = in_b
        self.in_c = in_c
        self.habitable = habitable
        self.populated = populated
    
    def __repr__(self):
        return ''.join([f"{'' if in_set else '¬'}{set_name}" for in_set, set_name in zip([self.in_a, self.in_b, self.in_c], 'ABC')])
    
    def is_in_set(self, set_name):
        if set_name == 'A':
            return self.in_a
        elif set_name == 'B':
            return self.in_b
        elif set_name == 'C':
            return self.in_c
        else:
            raise ValueError("Invalid set name. Use 'A', 'B', or 'C'.")
    
    def get_sets_tuple(self):
        return (self.in_a, self.in_b, self.in_c)
    
    def __eq__(self, other):
        return (
            self.in_a == other.in_a and
            self.in_b == other.in_b and
            self.in_c == other.in_c
        )
    
    def intersects(self, other):
        return (
            (self.in_a and other.in_a) and
            (self.in_b and other.in_b) and
            (self.in_c and other.in_c)
        )
    
    def union(self, other):
        return Region(
            in_a=self.in_a or other.in_a,
            in_b=self.in_b or other.in_b,
            in_c=self.in_c or other.in_c
        )
    
    def difference(self, other):
        return Region(
            in_a=self.in_a and not other.in_a,
            in_b=self.in_b and not other.in_b,
            in_c=self.in_c and not other.in_c
        )

class RegionManager:
    def __init__(self):
        self.regions = self.generate_all_regions()
    
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
            self.regions[region_tuple].habitable = status
        else:
            raise ValueError(f"Unrecognised region: {region_tuple}")
    
    def get_habitability(self, region_tuple):
        if region_tuple in self.regions:
            return self.regions[region_tuple].habitable
        else:
            raise ValueError(f"Unrecognised region: {region_tuple}")
        
    def set_populated(self, region_tuple, status):
        if region_tuple in self.regions:
            self.regions[region_tuple].populated = status
        else:
            raise ValueError(f"Unrecognised region: {region_tuple}")
    
    def get_populated(self, region_tuple):
        if region_tuple in self.regions:
            return self.regions[region_tuple].populated
        else:
            raise ValueError(f"Unrecognised region: {region_tuple}")
    
    def get_all_regions(self):
        return self.regions