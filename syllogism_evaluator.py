from region_struct import RegionManager, Status

class SyllogismEvaluator:
    
    
    @staticmethod
    def evaluate_status(manager):
        # Evaluate the status of each region in the manager based on all statements
        for statement in manager.statements:
            SyllogismEvaluator.evaluate_statement(manager, statement)
        
        # Update the validity status if there is conflict
        if Status.CONFLICT in [region.status for region in manager.get_all_regions().values()]:
            manager.set_validity(False)
        
        return manager
    
    @staticmethod
    def evaluate_statement(manager, statement):
        # Evaluate the status of each region in the manager based on one statement
        for region_tuple, region in manager.get_all_regions().items():
            current_status = region.status
            new_status = SyllogismEvaluator.determine_status(statement, region)
            region.status = SyllogismEvaluator.combine_status(current_status, new_status)
    
    @staticmethod
    def determine_status(statement, region):
        # gives the status of the region based on the statement
        if statement.entails:
            return SyllogismEvaluator.determine_entails_status(statement, region)
        else:
            return SyllogismEvaluator.determine_not_entails_status(statement, region)
            
        
    @staticmethod
    def determine_entails_status(statement, region):
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
    def determine_not_entails_status(statement, region):
        # if region is within antecedent and not in consequent
        if region.is_in_set(statement.antecedent) and not region.is_in_set(statement.consequent):
            # then there something should exist
            return Status.CONTAINS
        return Status.UNDEFINED
    
    @staticmethod
    def combine_status(status1, status2):
        # Clears conflict
        if status1 == Status.CONFLICT or status2 == Status.CONFLICT:
            return Status.CONFLICT
        
        # Clears undefined
        if status1 == Status.UNDEFINED:
            return status2
        if status2 == Status.UNDEFINED:
            return status1
        
        # Clears habitable from s1
        if status1 == Status.HABITABLE:
            if status2 == Status.UNINHABITABLE:
                return Status.CONFLICT
            if status2 == Status.CONTAINS:
                return Status.CONTAINS
            return Status.HABITABLE
        
        # Clears uninhabitable from s1
        if status1 == Status.UNINHABITABLE:
            if status2 == Status.HABITABLE or status2 == Status.CONTAINS:
                return Status.CONFLICT
            return Status.UNINHABITABLE
            
        # Clears Contains from s1
        if status1 == Status.CONTAINS:
            if status2 == Status.UNINHABITABLE:
                return Status.CONFLICT
            return Status.CONTAINS


    @staticmethod
    def evaluate_syllogism(region_managers):
        # Evaluate the validity of the syllogism based on the region managers
        major_premise_manager = region_managers['major_premise']
        minor_premise_manager = region_managers['minor_premise']
        conclusion_manager = region_managers['conclusion']
        
        # Evaluate the status of each region in the premises
        SyllogismEvaluator.evaluate_status(major_premise_manager)
        SyllogismEvaluator.evaluate_status(minor_premise_manager)
        
        # Check for internal conflicts in premises
        if not major_premise_manager.is_valid() or not minor_premise_manager.is_valid():
            outputCode = "Malformed premises"
        
        # Combine the regions from the major and minor premises and check for conflict
        premises_manager = SyllogismEvaluator.combine_region_managers(major_premise_manager, minor_premise_manager)
        if not premises_manager.is_valid():
            outputCode = "Contradictory premises"
        
        # Evaluate the status of each region in the conclusion and check for internal conflicts
        SyllogismEvaluator.evaluate_status(conclusion_manager)
        if not conclusion_manager.is_valid():
            outputCode = "Malformed conclusion"
        
        # Combine the conclusion with the combined premises
        final_manager = SyllogismEvaluator.combine_region_managers(premises_manager, conclusion_manager)
        
        if final_manager.is_valid():
            outputCode = "Valid conclusion"
        else:
            outputCode = "Invalid conclusion"
        
        return {
            'outputCode': outputCode,
            'major_premise': major_premise_manager,
            'minor_premise': minor_premise_manager,
            'conclusion': conclusion_manager,
            'premises': premises_manager,
            'final_manager': final_manager
        }
    
    @staticmethod
    def combine_region_managers(manager1, manager2):
        # Combine the regions from two managers and return a new manager
        combined_manager = RegionManager([])
        for region_tuple in manager1.get_all_regions().keys():
            status1 = manager1.get_status(region_tuple)
            status2 = manager2.get_status(region_tuple)
            combined_status = SyllogismEvaluator.combine_status(status1, status2)
            combined_manager.set_habatibility(region_tuple, combined_status)
        
        # Update the validity status if there is conflict
        if Status.CONFLICT in [region.status for region in combined_manager.get_all_regions().values()]:
            combined_manager.set_validity(False)
        
        return combined_manager