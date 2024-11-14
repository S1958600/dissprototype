import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib_venn import venn3
import matplotlib.pyplot as plt

class SyllogismGUI:
    def __init__(self, root, main_controller):
        self.root = root
        self.root.title("Syllogism Evaluator")
        
        self.main_controller = main_controller
        
        # Input frame
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=10)
        
        # Major premise
        self.major_label = tk.Label(self.input_frame, text="Major Premise:")
        self.major_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.major_antecedent_neg = tk.StringVar(value="")
        self.major_antecedent_neg_dropdown = tk.OptionMenu(self.input_frame, self.major_antecedent_neg, "", "¬")
        self.major_antecedent_neg_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        self.major_antecedent = tk.Entry(self.input_frame, width=5)
        self.major_antecedent.grid(row=0, column=2, padx=5, pady=5)
        
        self.major_entailment = tk.StringVar(value="⊨")
        self.major_entailment_dropdown = tk.OptionMenu(self.input_frame, self.major_entailment, "⊨", "⊭")
        self.major_entailment_dropdown.grid(row=0, column=3, padx=5, pady=5)
        
        self.major_consequent_neg = tk.StringVar(value="")
        self.major_consequent_neg_dropdown = tk.OptionMenu(self.input_frame, self.major_consequent_neg, "", "¬")
        self.major_consequent_neg_dropdown.grid(row=0, column=4, padx=5, pady=5)
        
        self.major_consequent = tk.Entry(self.input_frame, width=5)
        self.major_consequent.grid(row=0, column=5, padx=5, pady=5)
        
        # Minor premise
        self.minor_label = tk.Label(self.input_frame, text="Minor Premise:")
        self.minor_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.minor_antecedent_neg = tk.StringVar(value="")
        self.minor_antecedent_neg_dropdown = tk.OptionMenu(self.input_frame, self.minor_antecedent_neg, "", "¬")
        self.minor_antecedent_neg_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        self.minor_antecedent = tk.Entry(self.input_frame, width=5)
        self.minor_antecedent.grid(row=1, column=2, padx=5, pady=5)
        
        self.minor_entailment = tk.StringVar(value="⊨")
        self.minor_entailment_dropdown = tk.OptionMenu(self.input_frame, self.minor_entailment, "⊨", "⊭")
        self.minor_entailment_dropdown.grid(row=1, column=3, padx=5, pady=5)
        
        self.minor_consequent_neg = tk.StringVar(value="")
        self.minor_consequent_neg_dropdown = tk.OptionMenu(self.input_frame, self.minor_consequent_neg, "", "¬")
        self.minor_consequent_neg_dropdown.grid(row=1, column=4, padx=5, pady=5)
        
        self.minor_consequent = tk.Entry(self.input_frame, width=5)
        self.minor_consequent.grid(row=1, column=5, padx=5, pady=5)
        
        # Conclusion
        self.conclusion_label = tk.Label(self.input_frame, text="Conclusion:")
        self.conclusion_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.conclusion_antecedent_neg = tk.StringVar(value="")
        self.conclusion_antecedent_neg_dropdown = tk.OptionMenu(self.input_frame, self.conclusion_antecedent_neg, "", "¬")
        self.conclusion_antecedent_neg_dropdown.grid(row=2, column=1, padx=5, pady=5)
        
        self.conclusion_antecedent = tk.Entry(self.input_frame, width=5)
        self.conclusion_antecedent.grid(row=2, column=2, padx=5, pady=5)
        
        self.conclusion_entailment = tk.StringVar(value="⊨")
        self.conclusion_entailment_dropdown = tk.OptionMenu(self.input_frame, self.conclusion_entailment, "⊨", "⊭")
        self.conclusion_entailment_dropdown.grid(row=2, column=3, padx=5, pady=5)
        
        self.conclusion_consequent_neg = tk.StringVar(value="")
        self.conclusion_consequent_neg_dropdown = tk.OptionMenu(self.input_frame, self.conclusion_consequent_neg, "", "¬")
        self.conclusion_consequent_neg_dropdown.grid(row=2, column=4, padx=5, pady=5)
        
        self.conclusion_consequent = tk.Entry(self.input_frame, width=5)
        self.conclusion_consequent.grid(row=2, column=5, padx=5, pady=5)
        
        self.process_button = tk.Button(self.input_frame, text="Process", command=self.process_input)
        self.process_button.grid(row=3, column=0, columnspan=6, pady=10)
        
        # Output frame
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(pady=10)
        
        self.output_label = tk.Label(self.output_frame, text="Output:")
        self.output_label.pack()
        
        self.output_text = tk.Text(self.output_frame, height=10, width=80)
        self.output_text.pack()
        
        # Venn diagram frame
        self.venn_frame = tk.Frame(self.root)
        self.venn_frame.pack(pady=10)
        
        self.venn_canvas = None
    
    def process_input(self):
        major_premise = f"{self.major_antecedent_neg.get()}{self.major_antecedent.get()} {self.major_entailment.get()} {self.major_consequent_neg.get()}{self.major_consequent.get()}"
        minor_premise = f"{self.minor_antecedent_neg.get()}{self.minor_antecedent.get()} {self.minor_entailment.get()} {self.minor_consequent_neg.get()}{self.minor_consequent.get()}"
        conclusion = f"{self.conclusion_antecedent_neg.get()}{self.conclusion_antecedent.get()} {self.conclusion_entailment.get()} {self.conclusion_consequent_neg.get()}{self.conclusion_consequent.get()}"
        print(major_premise)
        
        raw_input = f"{major_premise}, {minor_premise}, {conclusion}"
        
        if not raw_input:
            messagebox.showerror("Input Error", "Please enter a syllogism.")
            return
        
        self.output_text.delete(1.0, tk.END)
        
        try:
            # Process input and generate output
            evaluation = self.main_controller.process_input(raw_input)
            
            # Display output
            self.output_text.insert(tk.END, f"Syllogism is: {evaluation['outputCode']}\n")
            self.output_text.insert(tk.END, "Regions:\n")
            for region_tuple, region in evaluation['premises'].get_all_regions().items():
                sets = []
                sets.append('A' if region_tuple[0] else '¬A')
                sets.append('B' if region_tuple[1] else '¬B')
                sets.append('C' if region_tuple[2] else '¬C')
                sets_str = ', '.join(sets)
                self.output_text.insert(tk.END, f"Region: ({sets_str}), Status: {region.status.name}\n")
            
            # Display Venn diagram
            self.display_venn_diagram(evaluation['premises'])
        
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))
    
    def display_venn_diagram(self, region_manager):
        if self.venn_canvas:
            self.venn_canvas.get_tk_widget().pack_forget()
        
        # Create Venn diagram
        fig, ax = plt.subplots()
        venn = venn3(subsets=(1, 1, 1, 1, 1, 1, 1), set_labels=('A', 'B', 'C'))
        
        # Update Venn diagram based on region statuses
        for region_tuple, region in region_manager.get_all_regions().items():
            subset_label = ''.join(['1' if x else '0' for x in region_tuple])
            venn.get_label_by_id(subset_label).set_text(region.status.name)
        
        self.venn_canvas = FigureCanvasTkAgg(fig, master=self.venn_frame)
        self.venn_canvas.draw()
        self.venn_canvas.get_tk_widget().pack()