from region_struct import RegionManager, Status

class SyllogismEvaluator:
    
    @staticmethod
    def evaluate_status(manager):
        """
        Evaluate status based on all statements in the RegionManager.
        """
        for statement in manager.statements:
            SyllogismEvaluator.evaluate_statement(manager, statement)
        
        # Update the validity status based on the status of regions
        has_conflict = any(manager.get_status(region_tuple) == Status.CONFLICT for region_tuple in manager.get_all_regions().keys())
        manager.set_validity(not has_conflict) # Set validity to False if there is a conflict
        
        return manager
    
    @staticmethod
    def evaluate_all_region_managers(region_managers):
        """
        Evaluate status for each RegionManager given by the controller.
        """
        for manager in region_managers:
            SyllogismEvaluator.evaluate_status(manager)
        return region_managers
    
    @staticmethod
    def can_coexist(manager1, manager2):
        """
        Check if two RegionManagers can coexist with one another.
        """
        for region_tuple in manager1.get_all_regions().keys():
            if manager1.get_status(region_tuple) == Status.HABITABLE and manager2.get_status(region_tuple) == Status.UNINHABITABLE:
                return False
            if manager1.get_status(region_tuple) == Status.UNINHABITABLE and manager2.get_status(region_tuple) == Status.HABITABLE:
                return False
        return True
    
    @staticmethod
    def evaluate_statement(manager, statement):
        """
        Evaluate a single statement and update the status of regions in the RegionManager.
        """
        for region_tuple, region in manager.get_all_regions().items():
            current_status = region.status
            new_status = SyllogismEvaluator.determine_status(statement, region)
            
            if current_status == Status.UNDEFINED:
                region.status = new_status
            elif current_status != new_status and new_status != Status.UNDEFINED:
                region.status = Status.CONFLICT
                manager.set_validity(False)
    
    @staticmethod
    def determine_status(statement, region):
        """
        Determine the status of a region based on a statement.
        """
        #TODO: CONTINUE HERE
        if statement.entails:
            return SyllogismEvaluator.determine_entails_status(statement, region)
        else:
            return SyllogismEvaluator.determine_not_entails_status(statement, region)
        
    @staticmethod
    def determine_entails_status(statement, region):
        """
        Determine the status of a region based on a statement that entails.
        """
        if statement.antecedent.negation:
            if region.is_in_set(statement.antecedent.name):
                return None
        else:
            return SyllogismEvaluator.determine_entails_status_helper(statement, region)
        
    @staticmethod
    def determine_not_entails_status(statement, region):
        """
        Determine the status of a region based on a statement that does not entail.
        """
        if statement.antecedent.negation:
            return SyllogismEvaluator.determine_entails_status_helper(statement, region)
        else:
            return SyllogismEvaluator.determine_not_entails_status_helper(statement, region)