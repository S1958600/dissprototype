class Parser:
    def parse_input_syllogism(self, syllogism):
        # Split the syllogism into individual statements
        statements = syllogism.split(',')
        
        # Ensure there are exactly three statements
        if len(statements) != 3:
            raise ValueError("Invalid syllogism: Must contain exactly three statements.")
        
        # Parse each statement using the parse_input_statement method
        major_premise = self.parse_input_statement(statements[0])
        minor_premise = self.parse_input_statement(statements[1])
        conclusion = self.parse_input_statement(statements[2])
        
        # Return the parsed result as a dictionary
        return {
            'major_premise': major_premise,
            'minor_premise': minor_premise,
            'conclusion': conclusion
        }
    
    def parse_input_statement(self, statement):
        # Check for entailment symbol (⊨ or ⊭)
        if '⊨' in statement:
            entailment = True
            antecedent, consequent = statement.split('⊨')
        elif '⊭' in statement:
            entailment = False
            antecedent, consequent = statement.split('⊭')
        else:
            raise ValueError("Invalid statement: Missing entailment symbol.")
        
        # Parse antecedent and consequent as sets
        antecedent = self.parse_input_set(antecedent)
        consequent = self.parse_input_set(consequent)
        
        # Return the parsed result as a dictionary
        return {
            'antecedent': antecedent,
            'consequent': consequent,
            'entails': entailment
        }
    
    def parse_input_set(self, set):
        # Strip leading and trailing whitespace
        set = set.strip()
        
        # Check for negation symbol (¬)
        negation = False
        if set.startswith('¬'):
            negation = True
            # Remove the negation symbol
            set = set[1:].strip()
        
        # Return the parsed result as a dictionary
        return {
            'name': set,
            'negation': negation
        }