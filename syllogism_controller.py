from syllogism_processor import SyllogismProcessor
from syllogism_evaluator import SyllogismEvaluator

class SyllogismController:
    @staticmethod
    def process_syllogism_input(raw_input, order=None):
        #print("Processing input:", raw_input)
        
        # Parse input and create syllogism
        syllogism = SyllogismProcessor.process_input_syllogism(raw_input, order)
        #print("Created syllogism:\n", syllogism)
        
        # Generate region managers for each statement
        region_managers = SyllogismProcessor.generate_region_managers(syllogism)
        #print("Generated region managers\n")
        
        # Check the validity of the syllogism
        evaluation = SyllogismEvaluator.evaluate_syllogism(region_managers)
        #print("Syllogism is:", evaluation['outputCode'])
        #evaluation['premises'].print_regions()
        
        #print("Combined region manager regions:")
        #evaluation['premises'].print_regions()
        
        return evaluation
    
    @staticmethod
    def process_venn_input(raw_syllogism, input_premises_manager, input_conclusion_manager):
        # Parse raw input and create mangers to evaluate venn input against
        evaluation = SyllogismController.process_syllogism_input(raw_syllogism)
        
        
        if evaluation['premises'].is_valid() == False:
            #throw error for conflicting premises
            raise ValueError("Conflicting premises cannot be evaluated")
        
        #set input managers statements to the syllogism statements
        for statement in evaluation['premises'].get_statements():
            input_premises_manager.add_statement(statement)
        for statement in evaluation['conclusion'].get_statements():
            input_conclusion_manager.add_statement(statement)
        
                        
        # Compare the input managers against the syllogism statements
        input_premises_manager = SyllogismEvaluator.check_manager_for_conflict(input_premises_manager, evaluation['conclusion'], evaluation['outputCode'])
        input_conclusion_manager = SyllogismEvaluator.check_manager_for_conflict(input_conclusion_manager, evaluation['premises'], evaluation['outputCode'])
        
        return input_premises_manager, input_conclusion_manager