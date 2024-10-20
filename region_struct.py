from enum import Enum

class Status(Enum):
    UNDEFINED = "Undefined"
    HABITABLE = "Habitable"
    UNINHABITABLE = "Uninhabitable"
    CONTAINS = "Contains"
    CONFLICT = "Conflict"

class Region:
    def __init__(self, in_a=False, in_b=False, in_c=False, status=Status.UNDEFINED):
        self.in_a = in_a
        self.in_b = in_b
        self.in_c = in_c
        self.status = status
    
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
    
    def set_status(self, status):
        self.status = status