class SyllogismStatement:
    def __init__(self, antecedent, consequent, entails=True):
        self.antecedent = antecedent
        self.consequent = consequent
        self.entails = entails

    def __str__(self):
        entailment_symbol = '⊨' if self.entails else '⊭'
        return f"{self.antecedent} {entailment_symbol} {self.consequent}"



