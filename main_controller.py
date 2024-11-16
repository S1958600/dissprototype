from syllogism_controller import SyllogismController
from interface_controller import SyllogismGUI
import tkinter as tk

class MainController:
    def __init__(self):
        self.root = tk.Tk()  # Create the main window
        self.interface_controller = SyllogismGUI(self.root, self)
    
    def run(self):
        self.root.mainloop()
    
    def process_input(self, raw_input):
        return SyllogismController.process_input(raw_input)

# This is the main entry point for the program
if __name__ == "__main__":  # If this file is being run as the main
    main_controller = MainController()
    main_controller.run()