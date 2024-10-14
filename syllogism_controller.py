from parser import Parser
from syllogism_evaluator import SyllogismEvaluator
from object_creator import ObjectCreator

class SyllogismController:
    def __init__(self):
        self.parser = Parser()
        self.syllogism_checker = SyllogismEvaluator()
    
    def process_input(self, raw_input):
        is_valid = False
        print("Processing input:", raw_input)
        
        # Parse input and create syllogism
        syllogism = self.create_syllogism_from_input(raw_input)
        print("Created syllogism:\n", syllogism)
        
        # Generate blank region manager for each statement
        region_managers = ObjectCreator.generate_region_managers(syllogism)
        
        
        
        print("Valid regions:\n", region_managers)
        
        # Check the validity of the syllogism

        
        return is_valid
    
    def create_syllogism_from_input(self, raw_input):
        parsed_statements = self.parser.parse_input_syllogism(raw_input) # Parse input
        syllogism = ObjectCreator.create_syllogism_from_input(parsed_statements) # Create syllogism object
        return syllogism