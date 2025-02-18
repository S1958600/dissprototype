from set_struct import SyllogismSet
from statement_struct import SyllogismStatement
from syllogism_struct import Syllogism
from region_manager import RegionManager

class SyllogismProcessor:
    unique_sets = {}
    set_names = ['A', 'B', 'C']
    
    @staticmethod
    def process_input_syllogism(syllogism, order=None):
        # Reset unique sets for each new syllogism
        SyllogismProcessor.unique_sets = {}
        
        #if order is provided then map set names accordingly
        if order:
            if len(order) != 3:
                raise ValueError("Invalid order: Must contain exactly three set names.")
            for i, set_name in enumerate(order):
                SyllogismProcessor.unique_sets[set_name] = SyllogismProcessor.set_names[i]
        
        # Split the syllogism into individual statements
        statements = syllogism.split(',')
        
        # Ensure there are exactly three statements
        if len(statements) != 3:
            raise ValueError("Invalid syllogism: Must contain exactly three statements.")
        
        # Parse each statement using the parse_input_statement method
        major_premise = SyllogismProcessor.parse_input_statement(statements[0])
        minor_premise = SyllogismProcessor.parse_input_statement(statements[1])
        conclusion = SyllogismProcessor.parse_input_statement(statements[2])
        
        # Create syllogism object
        syllogism = Syllogism(
            major_premise=major_premise,
            minor_premise=minor_premise,
            conclusion=conclusion
        )
        
        return syllogism

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
        
        # Create SyllogismSet objects for antecedent and consequent
        antecedent = SyllogismProcessor.create_set(antecedent.strip())
        consequent = SyllogismProcessor.create_set(consequent.strip())
        
        # Create and return SyllogismStatement object
        return SyllogismStatement(
            antecedent=antecedent,
            consequent=consequent,
            entails=entailment
        )
    
    @staticmethod
    def create_set(set_data):
        # Check for negation symbol and strip it
        negation = '¬' in set_data
        set_name = set_data.replace('¬', '').strip()
        
        # Check if the set name is already mapped
        if set_name not in SyllogismProcessor.unique_sets:
            if len(SyllogismProcessor.unique_sets) >= 3:
                raise ValueError("More than 3 unique sets are not allowed.")
            # Assign the next available name (A, B, C)
            SyllogismProcessor.unique_sets[set_name] = SyllogismProcessor.set_names[len(SyllogismProcessor.unique_sets)]
        
        # Create and return SyllogismSet object with the mapped name
        return SyllogismSet(
            name=SyllogismProcessor.unique_sets[set_name],
            negation=negation
        )
    
    @staticmethod
    def generate_region_managers(syllogism):
        # Generate a RegionManager for each statement in the syllogism
        region_managers = {
            'major_premise': RegionManager([syllogism.major_premise]),
            'minor_premise': RegionManager([syllogism.minor_premise]),
            'conclusion': RegionManager([syllogism.conclusion])
        }
        return region_managers