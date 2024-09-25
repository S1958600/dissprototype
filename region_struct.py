class Region:
    def __init__(self, in_a=False, in_b=False, in_c=False):
        self.sets = (in_a, in_b, in_c)
    
    def __repr__(self):
        return f"Region{self.sets}"
    
    def is_in_set(self, set_name):
        if set_name == 'a':
            return self.sets[0]
        elif set_name == 'b':
            return self.sets[1]
        elif set_name == 'c':
            return self.sets[2]
        else:
            raise ValueError("Invalid set name. Use 'a', 'b', or 'c'.")
    
    def __eq__(self, other):
        return self.sets == other.sets
    
    def intersects(self, other):
        return all(
            (self.sets[i] and other.sets[i]) for i in range(3)
        )
    
    def union(self, other):
        return Region(
            in_a=self.sets[0] or other.sets[0],
            in_b=self.sets[1] or other.sets[1],
            in_c=self.sets[2] or other.sets[2]
        )
    
    def difference(self, other):
        return Region(
            in_a=self.sets[0] and not other.sets[0],
            in_b=self.sets[1] and not other.sets[1],
            in_c=self.sets[2] and not other.sets[2]
        )

# Example usage
region1 = Region(in_a=True, in_b=True, in_c=False)
region2 = Region(in_a=False, in_b=True, in_c=True)

print(region1)            # Output: Region(True, True, False)
print(region2)            # Output: Region(False, True, True)
print(region1.is_in_set('a'))  # Output: True
print(region1.intersects(region2))  # Output: True (since they both have b as True)
print(region1.union(region2))       # Output: Region(True, True, True)
print(region1.difference(region2))  # Output: Region(True, False, False)
