from syllogism_processor import SyllogismProcessor
from syllogism_evaluator import SyllogismEvaluator

class SyllogismController:
    @staticmethod
    def process_syllogism_input(raw_input):
        print("Processing input:", raw_input)
        
        # Parse input and create syllogism
        syllogism = SyllogismProcessor.process_input_syllogism(raw_input)
        print("Created syllogism:\n", syllogism)
        
        # Generate region managers for each statement
        region_managers = SyllogismProcessor.generate_region_managers(syllogism)
        #print("Generated region managers\n")
        
        # Check the validity of the syllogism
        evaluation = SyllogismEvaluator.evaluate_syllogism(region_managers)
        print("Syllogism is:", evaluation['outputCode'])
        evaluation['premises'].print_regions()
        
        return evaluation