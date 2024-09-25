from parser import Parser
from syllogism_checker import SyllogismChecker
from object_creator import ObjectCreator

class SyllogismController:
    def __init__(self):
        self.parser = Parser()
        self.syllogism_checker = SyllogismChecker()
    
    def process_input(self, raw_input):
        print("Processing input:", raw_input)
        
        # Parse input using Parser
        parsed_statements = self.parser.parse_input_syllogism(raw_input)
        print("Parsed input:", parsed_statements)
        
        # Create syllogism using ObjectCreator
        syllogism = ObjectCreator.create_syllogism_from_input(parsed_statements)
        print("Created syllogism:\n",syllogism)
        
        is_valid = self.syllogism_checker.check_syllogism(syllogism)
        
        return is_valid