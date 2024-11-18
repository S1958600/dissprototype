from region_struct import Status, Region
from region_manager import RegionManager

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
        valid_conclusion = SyllogismEvaluator.check_conclusion_validity(combined_manager, conclusion_manager.get_statements()[0])
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
        if conclusion_statement.entails:
            valid_return = True  # Assume valid and search for counterexample
            for region_tuple, region in combined_manager.get_all_regions().items():
                # Search for regions that break the entailment
                if region.is_in_set(conclusion_statement.antecedent):
                    if not region.is_in_set(conclusion_statement.consequent):
                        # Only invalid if the region is explicitly habitable or contains
                        if region.status == Status.HABITABLE or region.status == Status.CONTAINS:
                            valid_return = False
                            break
        else:
            valid_return = False  # Assume invalid and search for proof of validity
            for region_tuple, region in combined_manager.get_all_regions().items():
                if region.is_in_set(conclusion_statement.antecedent):
                    if not region.is_in_set(conclusion_statement.consequent):
                        # Only valid if the region is explicitly contains
                        if region.status == Status.CONTAINS:
                            valid_return = True
                            break
        
        return valid_return