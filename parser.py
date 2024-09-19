class Parser:
    
    def parse_input_statement(self, statement):
        # Example of parsing logic to break down input statement into parts
        lhs, rhs = statement.split('⊨')
        # can also be ⊭
        negated = False
        if '¬' in rhs:
            negated = True
            rhs = rhs.replace('¬', '').strip()
        
        # Return parsed data as a dictionary (or custom data structure)
        return {
            'antecedent': lhs.strip(),
            'consequent': rhs.strip(),
            'negated': negated
        }
