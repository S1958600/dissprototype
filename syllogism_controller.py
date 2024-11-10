from parser import Parser
from syllogism_evaluator import SyllogismEvaluator
from object_creator import ObjectCreator
from region_manager import RegionManager

class SyllogismController:
    
    def process_input(self, raw_input):
        print("Processing input:", raw_input)
        
        # Parse input and create syllogism
        syllogism = self.create_syllogism_from_input(raw_input)
        print("Created syllogism:\n", syllogism)
        
        # Generate region managers for each statement
        region_managers = ObjectCreator.generate_region_managers(syllogism)
        #print("Region managers:\n", region_managers)
        
        evaluation_output = SyllogismEvaluator.evaluate_syllogism(region_managers)
        
        print("Evaluation output:\n", evaluation_output['outputCode'])
    
    def create_syllogism_from_input(self, raw_input):
        parsed_statements = Parser.parse_input_syllogism(raw_input) # Parse input syllogism
        syllogism = ObjectCreator.create_syllogism_from_input(parsed_statements) # Create syllogism object
        return syllogism