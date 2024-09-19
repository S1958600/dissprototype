import parser
import syllogismChecker

class SyllogismController:
    def __init__(self):
        self.parser = parser() # Will handle the logic to parse the input
        self.syllogism_checker = syllogismChecker()  # Will handle the logic to check correctness
    
    def process_input(self, raw_input):
        syllogism = self.parser.parse_input_statement(raw_input)
        
        is_valid = self.syllogism_checker.check_syllogism(syllogism)
        
        return is_valid
