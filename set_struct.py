class SyllogismSet:
    def __init__(self, name, negation=False):
        self.name = name  # e.g., 'a', 'b', 'c'
        self.negation = negation

    def __str__(self):
        return f"¬{self.name}" if self.negation else self.name

    def negate(self):
        # Return a new SyllogismSet object with the negation flipped
        return SyllogismSet(self.name, not self.negation)

