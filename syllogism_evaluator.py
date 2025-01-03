from region_struct import Status, Region
from region_manager import RegionManager

from copy import deepcopy

class SyllogismEvaluator:
    
    @staticmethod
    def evaluate_syllogism(region_managers):
        # Determine region status for each statement
        major_premise_manager = SyllogismEvaluator.evaluate_status(region_managers['major_premise'])
        minor_premise_manager = SyllogismEvaluator.evaluate_status(region_managers['minor_premise'])
        conclusion_manager = SyllogismEvaluator.evaluate_status(region_managers['conclusion'])
            
        # Combine the statements from the major and minor premises and determine status
        combined_manager = RegionManager(major_premise_manager.get_statements())
        combined_manager.add_statement(minor_premise_manager.get_statements()[0])
        combined_manager = SyllogismEvaluator.evaluate_status(combined_manager)
               
        # Check if the conclusion fits into the combined premises
        valid_conclusion, replacement_premises_manager = SyllogismEvaluator.check_conclusion_validity(combined_manager, conclusion_manager.get_statements()[0])
        
        # Use the replacement premises manager if one is returned
        if replacement_premises_manager is not None:
            combined_manager = replacement_premises_manager
        
        return {
            'outputCode': valid_conclusion,
            'major_premise': major_premise_manager,
            'minor_premise': minor_premise_manager,
            'conclusion': conclusion_manager,
            'premises': combined_manager,
        }
    
    
    @staticmethod
    def evaluate_status(manager):
        # If there is only one statement, evaluate the status of each region based on that statement
        if len(manager.get_statements()) == 1:
            return_manager = SyllogismEvaluator.evaluate_one_statement(manager)
        # Otherwise, there are two statements, evaluate joint status of regions
        else:
            return_manager = SyllogismEvaluator.evaluate_two_statement(manager)
        return return_manager
        
    
    @staticmethod
    def evaluate_one_statement(manager):
        # Evaluate the status of each region in the manager based on one statement
        statement = manager.get_statements()[0]
        for region_tuple, region in manager.regions.items():
            if statement.entails:
                status = SyllogismEvaluator.determine_single_entails_status(statement, region)
            else:
                status = SyllogismEvaluator.determine_single_not_entails_status(statement, region)
            region.status = status
        return manager
            
        
    @staticmethod
    def determine_single_entails_status(statement, region):
        # if region is within antecedent 
        if region.is_in_set(statement.antecedent):
            if region.is_in_set(statement.consequent):
                # and in consequent then habitable
                return Status.HABITABLE
            else:
                # antecedant cannot habitate without consequent
                return Status.UNINHABITABLE
        else:
            return Status.UNDEFINED
            # if region is not antecedant then undefined bahaviour
        
        
    @staticmethod
    def determine_single_not_entails_status(statement, region):
        # if region is within antecedent and not in consequent
        if region.is_in_set(statement.antecedent) and not region.is_in_set(statement.consequent):
            # then something could exist
            return Status.CONTAINS
        return Status.UNDEFINED
    
    @staticmethod
    def evaluate_two_statement(manager):
        # Determine which method to use based on the statements
        statement1 = manager.get_statements()[0]
        statement2 = manager.get_statements()[1]
        
        for region_tuple, region in manager.regions.items():
            if statement1.entails and not statement2.entails:
                status = SyllogismEvaluator.evaluate_entails_and_not_entails(statement1, statement2, region)
            elif not statement1.entails and statement2.entails:
                status = SyllogismEvaluator.evaluate_entails_and_not_entails(statement2, statement1, region)
            elif not statement1.entails and not statement2.entails:
                status = SyllogismEvaluator.evaluate_two_not_entails(statement1, statement2, region)
            elif statement1.entails and statement2.entails:
                status = SyllogismEvaluator.evaluate_two_entails(statement1, statement2, region)
            region.status = status
        return manager
    
    @staticmethod
    def evaluate_two_entails(statement1, statement2, region):
        if region.is_in_set(statement1.antecedent) and region.is_in_set(statement2.antecedent):
            # if region is in both antecedents then must be in both consequents for habitable
            if region.is_in_set(statement1.consequent) and region.is_in_set(statement2.consequent):
                return Status.HABITABLE
            else:
                return Status.UNINHABITABLE
        
        # evaluate single entailment for each statement
        if region.is_in_set(statement1.antecedent):
            if region.is_in_set(statement1.consequent):
                return Status.HABITABLE
            else:
                return Status.UNINHABITABLE
        
        if region.is_in_set(statement2.antecedent):
            if region.is_in_set(statement2.consequent):
                return Status.HABITABLE
            else:
                return Status.UNINHABITABLE
        
        return Status.UNDEFINED
    
    @staticmethod
    def evaluate_entails_and_not_entails(entails_statement, not_entails_statement, region):
        #Check if region is in ditributed entails first
        if region.is_in_set(entails_statement.antecedent):
            if region.is_in_set(entails_statement.consequent):
                # Region is habitable but can also be contains
                if region.is_in_set(not_entails_statement.antecedent) and not region.is_in_set(not_entails_statement.consequent):
                    return Status.CONTAINS
                else:
                    return Status.HABITABLE
            else:
                # Edge case: entails blocks both contains regions causing a contradiction
                # Uninhabitable due to entails dominates not entails
                return Status.UNINHABITABLE
        
        # Check if region is in not entails alone
        
        
        if region.is_in_set(not_entails_statement.antecedent) and not region.is_in_set(not_entails_statement.consequent):
            return Status.CONTAINS
                    
        return Status.UNDEFINED
    
    @staticmethod
    def evaluate_two_not_entails(statement1, statement2, region):
        # no change in behaviour if in both antecedants - handle the same as two single not entails      
        if region.is_in_set(statement1.antecedent) and not region.is_in_set(statement1.consequent):
            return Status.CONTAINS
        if region.is_in_set(statement2.antecedent) and not region.is_in_set(statement2.consequent):
            return Status.CONTAINS
        return Status.UNDEFINED
    
    @staticmethod
    def check_conclusion_validity(combined_manager, conclusion_statement):
        valid_return = True  # Assume valid and search for counterexample
        replacement_premises_manager = None
        
        if conclusion_statement.entails:
            for region_tuple, region in combined_manager.get_all_regions().items():
                # Search for regions that break the entailment
                if region.is_in_set(conclusion_statement.antecedent):
                    if not region.is_in_set(conclusion_statement.consequent):
                        # Region must be uninhabitable if it is not in the consequent
                        if region.status != Status.UNINHABITABLE:
                            valid_return = False
                            break
                    #else: # If the region is in the consequent, it must be habitable
                    #    if region.status != Status.HABITABLE:
                    #        valid_return = False
        else:
            possible_managers = SyllogismEvaluator.generate_permutation_managers(combined_manager)
            for possible_manager in possible_managers:
                permutation_valid = False
                for region_tuple, region in possible_manager.get_all_regions().items():
                    if region.is_in_set(conclusion_statement.antecedent) and not region.is_in_set(conclusion_statement.consequent):
                            if region.status == Status.CONTAINS:
                                # Found an example where conclusion is still true - skip to next manager
                                permutation_valid = True
                                break   
                if not permutation_valid:
                    valid_return = False
                    replacement_premises_manager = possible_manager
                    break
        return valid_return, replacement_premises_manager
    
    def generate_permutation_managers(combined_manager):
        # generates all region managers that are valid combinations of contains under the statement(s)
        return_permutation_managers = [combined_manager]

        for region_tuple, region in combined_manager.get_all_regions().items():
            if region.status == Status.CONTAINS:
                new_manager = deepcopy(combined_manager)
                new_manager.regions[region_tuple].status = Status.UNDEFINED
                if SyllogismEvaluator.check_permutation_validity(new_manager):
                    return_permutation_managers.extend(SyllogismEvaluator.generate_permutation_managers(deepcopy(new_manager)))
                new_manager.regions[region_tuple].status = Status.CONTAINS
        return return_permutation_managers
                
    def check_permutation_validity(manager):
        # Check if the manager is valid - only checks not entails statements
        for statement in manager.get_statements():
            if not statement.entails:
                for region_tuple, region in manager.regions.items():
                    if region.is_in_set(statement.antecedent):
                        if not region.is_in_set(statement.consequent):
                            if region.status == Status.CONTAINS:
                                return True
        return False
    
    
    #Check for conflicts in an input manager. Needs manager from other diagram to see which contains regions are needed
    def check_manager_for_conflict(input_manager, other_manager, evaluation_true):
        #For each statement check for any regions that conflict with the statements
        for statement in input_manager.get_statements():
            if statement.entails:
                output_manager = SyllogismEvaluator.check_for_entails_conflict(input_manager, statement)
            else:
                #if there are more than one statements then the other statement is needed to see if it blocks contains regions
                if len(input_manager.get_statements()) > 1:
                    other_statement = input_manager.get_other_statement(statement)
                else:
                    other_statement = None
                
                # Not entails statements are more complicated to mark - see code
                output_manager = SyllogismEvaluator.check_for_not_entails_conflict(input_manager, statement, other_manager, evaluation_true, other_statement)
        
        return output_manager
    
    def check_for_entails_conflict(input_manager, statement):
        for region_tuple, region in input_manager.regions.items():
            if region.is_in_set(statement.antecedent):
                if not region.is_in_set(statement.consequent):
                    if region.status != Status.UNINHABITABLE:
                        region.set_status(Status.CONFLICT)
                        input_manager.set_validity(False)
        
        return input_manager
    
    def check_for_not_entails_conflict(input_manager, statement, other_manager, evaluation_true, other_statement):
        # If the syllogsim is true then at least one contains region from the other manager must be contains in the input manager
        if evaluation_true:
            # Tuples of regions that are contains in the other manager
            other_contains = SyllogismEvaluator.find_other_contains(other_manager)
            #If any region shared between the input manager and contains list is contains then input manager is unconflicted
            contains_found = False
            for region_tuple, region in input_manager.regions.items():
                if region_tuple in other_contains:
                    if region.status == Status.CONTAINS:
                        contains_found = True
                        break
            if not contains_found:
                #If no shared regions are contains, mark all shared regions as conflicts
                for region_tuple, region in input_manager.regions.items():
                    if region_tuple in other_contains and region.is_in_set(statement.antecedent) and not region.is_in_set(statement.consequent):
                        region.set_status(Status.CONFLICT)
                        input_manager.set_validity(False)
        else:
            # If evaluation returned false, any region that could be contains should be contains
            for region_tuple, region in input_manager.regions.items():
                
                #if there is another entails statement in the same manager
                if other_statement is not None and other_statement.entails:
                    other_status = SyllogismEvaluator.determine_single_entails_status(other_statement, region)
                    if other_status == Status.UNINHABITABLE:
                        continue  # uninhabitable region cant possible be contains
                
                if region.is_in_set(statement.antecedent) and not region.is_in_set(statement.consequent):
                    if region.status != Status.CONTAINS:
                        region.set_status(Status.CONFLICT)
                        input_manager.set_validity(False)
        
        return input_manager

    def find_other_contains(other_manager):
        # Finds all of the contains regions from the other manager
        other_contains = []
        for region_tuple, region in other_manager.regions.items():
            if region.status == Status.CONTAINS:
                other_contains.append(region_tuple)
        return other_contains