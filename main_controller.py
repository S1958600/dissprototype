from syllogism_controller import SyllogismController
from interface_controller import SyllogismGUI
import tkinter as tk

class MainController:
    def __init__(self):
        self.root = tk.Tk()  # Create the main window
        self.interface_controller = SyllogismGUI(self.root, self)
    
    def run(self):
        self.root.mainloop()
    
    def process_syllogism_input(self, raw_input, order=None):
        return SyllogismController.process_syllogism_input(raw_input, order)
    
    def process_venn_input(self, raw_syllogism, input_premises_manager, input_conclusion_manager, order):
        #returns a list of regions that are different between the two managers
        return SyllogismController.process_venn_input(raw_syllogism, input_premises_manager, input_conclusion_manager, order)

# This is the main entry point for the program
if __name__ == "__main__":  # If this file is being run as the main
    main_controller = MainController()
    main_controller.run()