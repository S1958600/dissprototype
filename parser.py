class Parser:
    @staticmethod
    def parse_input_syllogism(syllogism):
        # Split the syllogism into individual statements
        statements = syllogism.split(',')
        
        # Ensure there are exactly three statements
        if len(statements) != 3:
            raise ValueError("Invalid syllogism: Must contain exactly three statements.")
        
        # Parse each statement using the parse_input_statement method
        major_premise = Parser.parse_input_statement(statements[0])
        minor_premise = Parser.parse_input_statement(statements[1])
        conclusion = Parser.parse_input_statement(statements[2])
        
        # Return the parsed result as a dictionary
        return {
            'major_premise': major_premise,
            'minor_premise': minor_premise,
            'conclusion': conclusion
        }
    
    @staticmethod
    def parse_input_statement(statement):
        # Check for entailment symbol (⊨ or ⊭)
        if '⊨' in statement:
            entailment = True
            antecedent, consequent = statement.split('⊨')
        elif '⊭' in statement:
            entailment = False
            antecedent, consequent = statement.split('⊭')
        else:
            raise ValueError("Invalid statement: Missing entailment symbol.")
        
        # Return the parsed statement as a dictionary
        return {
            'entailment': entailment,
            'antecedent': antecedent.strip(),
            'consequent': consequent.strip()
        }