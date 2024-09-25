class SyllogismStatement:
    def __init__(self, antecedent, consequent, entails=True):
        self.antecedent = antecedent
        self.consequent = consequent
        self.entails = entails

    def __str__(self):
        entailment_symbol = '⊨' if self.entails else '⊭'
        return f"{self.antecedent} {entailment_symbol} {self.consequent}"

# Example usage:
statement1 = SyllogismStatement('a', '¬b')
statement2 = SyllogismStatement('a', 'c')
statement3 = SyllogismStatement('c', 'b', entails=False)

print(statement1)  # Output: a ⊨ ¬b
print(statement2)  # Output: a ⊨ c
print(statement3)  # Output: c ⊭ b

