from syllogism_controller import SyllogismController
from interface_controller import SyllogismGUI
import tkinter as tk

class MainController:
    def __init__(self):
        self.syllogism_controller = SyllogismController()
        self.root = tk.Tk()         # Create the main window
        self.interface_controller = SyllogismGUI(self.root, self)
    
    def run(self):
        self.root.mainloop()
    
    def process_input(self, raw_input):
        return self.syllogism_controller.process_input(raw_input)

if __name__ == "__main__":
    main_controller = MainController()
    main_controller.run()