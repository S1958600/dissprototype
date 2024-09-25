from set_struct import SyllogismSet
from statement_struct import SyllogismStatement
from syllogism_struct import Syllogism

class ObjectCreator:
    unique_sets = {}
    set_names = ['A', 'B', 'C']
    
    @staticmethod
    def create_syllogism_from_input(parsed_statements):
        # Reset unique sets for each new syllogism
        ObjectCreator.unique_sets = {}
        
        # Create statement objects directly from parsed statements
        major_premise = ObjectCreator.create_statement(parsed_statements['major_premise'])
        minor_premise = ObjectCreator.create_statement(parsed_statements['minor_premise'])
        conclusion = ObjectCreator.create_statement(parsed_statements['conclusion'])
        
        # Create syllogism object
        syllogism = Syllogism(
            major_premise=major_premise,
            minor_premise=minor_premise,
            conclusion=conclusion
        )
        
        return syllogism

    @staticmethod
    def create_statement(statement_data):
        # Create SyllogismSet objects for antecedent and consequent
        antecedent = ObjectCreator.create_set(statement_data['antecedent'])
        consequent = ObjectCreator.create_set(statement_data['consequent'])
        
        # Create and return SyllogismStatement object
        return SyllogismStatement(
            antecedent=antecedent,
            consequent=consequent,
            entails=statement_data['entails']
        )
    
    @staticmethod
    def create_set(set_data):
        # Strip any negation symbols and whitespace
        set_name = set_data['name'].strip().replace('¬', '')
        
        # Check if the set name is already mapped
        if set_name not in ObjectCreator.unique_sets:
            if len(ObjectCreator.unique_sets) >= 3:
                raise ValueError("More than 3 unique sets are not allowed.")
            # Assign the next available name (A, B, C)
            ObjectCreator.unique_sets[set_name] = ObjectCreator.set_names[len(ObjectCreator.unique_sets)]
        
        # Create and return SyllogismSet object with the mapped name
        return SyllogismSet(
            name=ObjectCreator.unique_sets[set_name],
            negation=set_data['negation']
        )