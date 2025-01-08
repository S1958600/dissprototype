import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

from image_controller import ImageController
from venn_diagram import gen_matplot_venn_output, gen_matplot_venn_interactive, generate_region_manager_from_venn, generate_matplot_venn_interactive_from_region_manager

class SyllogismGUI:
    def __init__(self, root, main_controller):
        self.root = root
        self.root.title("Syllogism Evaluator")
        self.main_controller = main_controller
        self.image_controller = ImageController() 
        self.row_counter = 0
        self.set_names = ["A", "B", "C"]
        
        self.create_set_name_input_frame()
        self.create_input_text_frame()
        self.create_interactive_venn_frame() 
        self.create_upload_file_frame()
        self.create_output_text_frame()
        self.create_output_venn_frame()
        
        # If input not processed then the output boxes dont show
        self.process_syllogism_input()

    def create_set_name_input_frame(self):
        rowIn = self.row_counter
        self.set_name_frame = tk.Frame(self.root)
        self.set_name_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        tk.Label(self.set_name_frame, text="Set Names:", anchor="center").grid(row=rowIn, column=0, padx=5, pady=5)
        
        #make tkinter variables for the set names and create entry fields for them
        self.set_name_vars = [tk.StringVar(value=name) for name in self.set_names]
        for i, set_name_var in enumerate(self.set_name_vars):
            tk.Entry(self.set_name_frame, textvariable=set_name_var, width=5).grid(row=rowIn, column=i+1, padx=5, pady=5)
        
        self.update_button = tk.Button(self.set_name_frame, text="Update Set Labels", command=self.update_set_labels)
        self.update_button.grid(row=rowIn, column=len(self.set_name_vars)+1, padx=5, pady=5)
        
        self.row_counter += 1

    def create_input_text_frame(self):
        rowIn = self.row_counter
        self.input_frame = tk.Frame(self.root)
        self.input_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        # case code 0 = major premise, 1 = minor premise, 2 = conclusion
        self.create_premise_row("Major Premise:", rowIn, 0)
        self.create_premise_row("Minor Premise:", rowIn+1, 1)
        self.create_premise_row("Conclusion:", rowIn+2, 2)
        
        self.process_button = tk.Button(self.input_frame, text="Display output Venn Diagram", command=self.process_syllogism_input)
        self.process_button.grid(row=rowIn+3, column=0, columnspan=7, pady=10)
        
        self.row_counter += 4

    def create_premise_row(self, label_text, row, case_code):
        tk.Label(self.input_frame, text=label_text, anchor="center").grid(row=row, column=0, padx=5, pady=5)
        
        antecedent_neg_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.input_frame, text="¬", variable=antecedent_neg_var).grid(row=row, column=1, padx=5, pady=5)
        
        # set up the default syllogism that the system starts with
        if case_code == 0:
            antecedent_var = tk.StringVar(value=self.set_names[0])  #A
            consequent_var = tk.StringVar(value=self.set_names[1])  #B
        elif case_code == 1:
            antecedent_var = tk.StringVar(value=self.set_names[1])  #B
            consequent_var = tk.StringVar(value=self.set_names[2])  #C
        elif case_code == 2:
            antecedent_var = tk.StringVar(value=self.set_names[0])  #A
            consequent_var = tk.StringVar(value=self.set_names[2])  #C
        
        antecedent_menu = tk.OptionMenu(self.input_frame, antecedent_var, *self.set_names)
        antecedent_menu.grid(row=row, column=2, padx=5, pady=5)
        
        entailment_var = tk.StringVar(value="⊨")
        tk.Radiobutton(self.input_frame, text="⊨", variable=entailment_var, value="⊨").grid(row=row, column=3, padx=3, pady=5)
        tk.Radiobutton(self.input_frame, text="⊭", variable=entailment_var, value="⊭").grid(row=row, column=4, padx=3, pady=5)
        
        consequent_neg_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.input_frame, text="¬", variable=consequent_neg_var).grid(row=row, column=5, padx=5, pady=5)
        
        consequent_menu = tk.OptionMenu(self.input_frame, consequent_var, *self.set_names)
        consequent_menu.grid(row=row, column=6, padx=5, pady=5)
        
        if case_code == 0:
            # major premise
            self.major_antecedent_neg = antecedent_neg_var
            self.major_antecedent = antecedent_var
            self.major_entailment = entailment_var
            self.major_consequent_neg = consequent_neg_var
            self.major_consequent = consequent_var
            self.major_antecedent_menu = antecedent_menu
            self.major_consequent_menu = consequent_menu
        elif case_code == 1:
            # minor premise
            self.minor_antecedent_neg = antecedent_neg_var
            self.minor_antecedent = antecedent_var
            self.minor_entailment = entailment_var
            self.minor_consequent_neg = consequent_neg_var
            self.minor_consequent = consequent_var
            self.minor_antecedent_menu = antecedent_menu
            self.minor_consequent_menu = consequent_menu
        elif case_code == 2:
            # conclusion
            self.conc_antecedent_neg = antecedent_neg_var
            self.conc_antecedent = antecedent_var
            self.conc_entailment = entailment_var
            self.conc_consequent_neg = consequent_neg_var
            self.conc_consequent = consequent_var
            self.conc_antecedent_menu = antecedent_menu
            self.conc_consequent_menu = consequent_menu

    def update_set_labels(self):
        self.set_names = [var.get() for var in self.set_name_vars]
        
        # Update dropdown menus
        for menu, var in [
            (self.major_antecedent_menu, self.major_antecedent),
            (self.major_consequent_menu, self.major_consequent),
            (self.minor_antecedent_menu, self.minor_antecedent),
            (self.minor_consequent_menu, self.minor_consequent),
            (self.conc_antecedent_menu, self.conc_antecedent),
            (self.conc_consequent_menu, self.conc_consequent)
        ]:
            menu['menu'].delete(0, 'end')
            for name in self.set_names:
                menu['menu'].add_command(label=name, command=tk._setit(var, name))
        
        #interactive venn diagrams need to be regenerated to reflect new labels
        self.interactive_premises_canvas.get_tk_widget().pack_forget()
        self.interactive_conclusion_canvas.get_tk_widget().pack_forget()
        
        self.interactive_premises_canvas, self.interactive_premises_venn = gen_matplot_venn_interactive(
            self.interactive_premises_frame, self.region_status, set_labels=self.set_names)
        self.interactive_premises_canvas.get_tk_widget().pack(expand=True, fill="both")
        
        self.interactive_conclusion_canvas, self.interactive_conclusion_venn = gen_matplot_venn_interactive(
            self.interactive_conclusion_frame, self.region_status, set_labels=self.set_names)
        self.interactive_conclusion_canvas.get_tk_widget().pack(expand=True, fill="both")

    def create_output_text_frame(self):
        rowIn = self.row_counter
        
        self.output_frame = tk.Frame(self.root)
        self.output_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        self.output_label = tk.Label(self.output_frame, text="Output:", anchor="center")
        self.output_label.pack()
        
        self.output_text = tk.Text(self.output_frame, height=2, width=60)
        self.output_text.pack(expand=True, fill="both")
        
        self.row_counter += 1
    
    # Make a frame for interactive venn diagrams - takes up two additional rows for radio buttons and button
    def create_interactive_venn_frame(self):
        rowIn = self.row_counter
        
        self.interactive_frame = tk.Frame(self.root)
        self.interactive_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        self.region_status = tk.StringVar(value="habitable")
        
        self.create_interactive_venn_diagram("Interactive Premises", self.interactive_frame, rowIn, 0)
        self.create_interactive_venn_diagram("Interactive Conclusion", self.interactive_frame, rowIn, 1)   
             
        radio_frame = tk.Frame(self.interactive_frame)
        radio_frame.grid(row=rowIn+1, column=0, padx=10, pady=10)
        
        tk.Radiobutton(radio_frame, text="Habitable", variable=self.region_status, value="habitable").grid(row=rowIn+1, column=0, padx=5)
        tk.Radiobutton(radio_frame, text="Uninhabitable", variable=self.region_status, value="uninhabitable").grid(row=rowIn+1, column=1, padx=5)
        tk.Radiobutton(radio_frame, text="Contains", variable=self.region_status, value="contains").grid(row=rowIn+1, column=2, padx=5)
        
        self.check_button = tk.Button(self.interactive_frame, text="Check venn diagram against syllogism", command=self.process_venn_input)
        self.check_button.grid(row=rowIn+2, column=0, columnspan=2, pady=10)
        
        self.row_counter += 3

    # Makes a single interactive venn diagram
    def create_interactive_venn_diagram(self, title, parent_frame, rowIn, column):
        frame = tk.Frame(parent_frame)
        frame.grid(row=rowIn, column=column, padx=10, pady=10)
        
        label = tk.Label(frame, text=title, anchor="center")
        label.pack()
        
        canvas, venn = gen_matplot_venn_interactive(frame, self.region_status, set_labels=self.set_names)
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        setattr(self, f"{title.lower().replace(' ', '_')}_frame", frame)
        setattr(self, f"{title.lower().replace(' ', '_')}_canvas", canvas)
        setattr(self, f"{title.lower().replace(' ', '_')}_venn", venn)
        
    # Make a frame for output venn diagrams
    def create_output_venn_frame(self):
        rowIn = self.row_counter
        
        self.output_venn_frame = tk.Frame(self.root)
        self.output_venn_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        self.create_output_venn_diagram("Premises", self.output_venn_frame, side=tk.LEFT)
        self.create_output_venn_diagram("Conclusion", self.output_venn_frame, side=tk.RIGHT)
        
        self.row_counter += 1
        
    # Makes a single output venn diagram
    def create_output_venn_diagram(self, title, parent_frame, side):
        frame = tk.Frame(parent_frame)
        frame.pack(side=side, padx=10, expand=True, fill="both")
        
        label = tk.Label(frame, text=title, anchor="center")
        label.pack()
        
        setattr(self, f"{title.lower()}_frame", frame)
        setattr(self, f"{title.lower()}_label", label)
        setattr(self, f"{title.lower()}_canvas", None)

    def create_upload_file_frame(self):
        rowIn = self.row_counter
        
        self.upload_frame = tk.Frame(self.root)
        self.upload_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        self.upload_premise_button = tk.Button(self.upload_frame, text="Upload Premise Image", command=self.upload_premise_image)
        self.upload_premise_button.grid(row=rowIn, column=1, padx=5, pady=5)
        
        self.upload_conclusion_button = tk.Button(self.upload_frame, text="Upload Conclusion Image", command=self.upload_conclusion_image)
        self.upload_conclusion_button.grid(row=rowIn, column=2, padx=5, pady=5)
        
        #add a process button to process the file
        self.process_file_button = tk.Button(self.upload_frame, text="Process Images", command=self.process_images)
        self.process_file_button.grid(row=rowIn, column=3, padx=5, pady=5)
        
        self.row_counter += 1
    
    def upload_premise_image(self):
        self.image_controller.upload_premise_image()

    def upload_conclusion_image(self):
        self.image_controller.upload_conclusion_image()

    def process_images(self):
        try:
            premise_venn_manager, conclusion_venn_manager = self.image_controller.process_images()
            self.update_interactive_venn_diagrams(premise_venn_manager, conclusion_venn_manager)
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

    def update_interactive_venn_diagrams(self, premise_venn_manager, conclusion_venn_manager):
        self.interactive_premises_canvas.get_tk_widget().pack_forget()
        self.interactive_conclusion_canvas.get_tk_widget().pack_forget()
        
        self.interactive_premises_canvas, self.interactive_premises_venn = generate_matplot_venn_interactive_from_region_manager(
            self.interactive_premises_frame, premise_venn_manager, set_labels=self.set_names)
        self.interactive_premises_canvas.get_tk_widget().pack(expand=True, fill="both")
        
        self.interactive_conclusion_canvas, self.interactive_conclusion_venn = generate_matplot_venn_interactive_from_region_manager(
            self.interactive_conclusion_frame, conclusion_venn_manager, set_labels=self.set_names)
        self.interactive_conclusion_canvas.get_tk_widget().pack(expand=True, fill="both")

    def get_raw_syllogism_input(self):
        #construct a plain text syllogism from the input fields
        major_premise = f"{'¬' if self.major_antecedent_neg.get() else ''}{self.major_antecedent.get()} {self.major_entailment.get()} {'¬' if self.major_consequent_neg.get() else ''}{self.major_consequent.get()}"
        minor_premise = f"{'¬' if self.minor_antecedent_neg.get() else ''}{self.minor_antecedent.get()} {self.minor_entailment.get()} {'¬' if self.minor_consequent_neg.get() else ''}{self.minor_consequent.get()}"
        conclusion = f"{'¬' if self.conc_antecedent_neg.get() else ''}{self.conc_antecedent.get()} {self.conc_entailment.get()} {'¬' if self.conc_consequent_neg.get() else ''}{self.conc_consequent.get()}"
        
        out = f"{major_premise}, {minor_premise}, {conclusion}"
        return out

    def process_syllogism_input(self):
        raw_input = self.get_raw_syllogism_input()
        
        if not raw_input:
            messagebox.showerror("Input Error", "Please enter a syllogism.")
            return
        
        #get the strings needed for the labels
        major_premise = f"{'¬' if self.major_antecedent_neg.get() else ''}{self.major_antecedent.get()} {self.major_entailment.get()} {'¬' if self.major_consequent_neg.get() else ''}{self.major_consequent.get()}"
        minor_premise = f"{'¬' if self.minor_antecedent_neg.get() else ''}{self.minor_antecedent.get()} {self.minor_entailment.get()} {'¬' if self.minor_consequent_neg.get() else ''}{self.minor_consequent.get()}"
        conclusion = f"{'¬' if self.conc_antecedent_neg.get() else ''}{self.conc_antecedent.get()} {self.conc_entailment.get()} {'¬' if self.conc_consequent_neg.get() else ''}{self.conc_consequent.get()}"
        
        self.output_text.delete(1.0, tk.END)
        try:
            evaluation = self.main_controller.process_syllogism_input(raw_input)
            self.output_text.insert(tk.END, f"Syllogism is: {evaluation['outputCode']}\n")
            premise_text = f"{major_premise}, {minor_premise}"
            self.display_venn_diagrams(evaluation['premises'], evaluation['conclusion'], premise_text, conclusion)
        
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))

    def display_venn_diagrams(self, premises_manager, conclusion_manager, premise_text, conclusion_text):
        if self.premises_canvas:
            self.premises_canvas.get_tk_widget().pack_forget()
        if self.conclusion_canvas:
            self.conclusion_canvas.get_tk_widget().pack_forget()
        
        self.premises_label.config(text=f"Premises: {premise_text}")
        self.conclusion_label.config(text=f"Conclusion: {conclusion_text}")
        
        self.premises_canvas = gen_matplot_venn_output(premises_manager, self.premises_frame, set_labels=self.set_names)
        self.premises_canvas.get_tk_widget().pack(expand=True, fill="both")
        
        self.conclusion_canvas = gen_matplot_venn_output(conclusion_manager, self.conclusion_frame, set_labels=self.set_names)
        self.conclusion_canvas.get_tk_widget().pack(expand=True, fill="both")
            
    def process_venn_input(self):
        # Retrieve the Venn diagram objects
        premises_venn = self.interactive_premises_venn
        conclusion_venn = self.interactive_conclusion_venn
        
        # Generate region managers from the Venn diagrams
        premises_manager = generate_region_manager_from_venn(premises_venn)
        conclusion_manager = generate_region_manager_from_venn(conclusion_venn)
        
        # Use the generated region managers for further processing
        try:
            premises_manager, conclusion_manager = self.main_controller.process_venn_input(self.get_raw_syllogism_input(), premises_manager, conclusion_manager)
            self.display_venn_diagrams(premises_manager, conclusion_manager, "Interactive Premises", "Interactive Conclusion")
            
            # Output text
            self.output_text.delete(1.0, tk.END)
            if premises_manager.is_valid() and conclusion_manager.is_valid():
                self.output_text.insert(tk.END, "The Venn diagrams correctly represent the syllogism.")
            elif premises_manager.is_valid() and not conclusion_manager.is_valid():
                self.output_text.insert(tk.END, "The conclusion Venn diagram breaks the syllogism statement.")
            elif not premises_manager.is_valid() and conclusion_manager.is_valid():
                self.output_text.insert(tk.END, "The premises Venn diagram breaks the syllogism statement.")
            elif not premises_manager.is_valid() and not conclusion_manager.is_valid():
                self.output_text.insert(tk.END, "Both the premises and conclusion Venn diagrams break the syllogism statement.")
            
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))