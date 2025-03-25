from syllogism_controller import SyllogismController
from interface_controller import SyllogismGUI
from image_controller import ImageController
import tkinter as tk

class MainController:
    def __init__(self):
        self.root = tk.Tk()  # Create the main window
        self.interface_controller = SyllogismGUI(self.root, self)
        self.image_controller = ImageController()
    
    def run(self):
        self.root.mainloop()
    
    def process_syllogism_input(self, raw_input, order=None):
        return SyllogismController.process_syllogism_input(raw_input, order)
    
    def process_venn_input(self, raw_syllogism, input_premises_manager, input_conclusion_manager, order):
        #returns a list of regions that are different between the two managers
        return SyllogismController.process_venn_input(raw_syllogism, input_premises_manager, input_conclusion_manager, order)

    def upload_premise_image(self):
        return self.image_controller.upload_premise_image()
    
    def upload_conclusion_image(self):
        return self.image_controller.upload_conclusion_image()
    
    def process_images(self):
        return self.image_controller.process_images()

# This is the main entry point for the program
if __name__ == "__main__":  # If this file is being run as the main
    main_controller = MainController()
    main_controller.run()