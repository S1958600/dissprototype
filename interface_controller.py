import tkinter as tk
from tkinter import messagebox
from venn_diagram import create_venn_diagram

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
        
        self.major_antecedent_neg = tk.BooleanVar(value=False)
        self.major_antecedent_neg_checkbox = tk.Checkbutton(self.input_frame, text="¬", variable=self.major_antecedent_neg)
        self.major_antecedent_neg_checkbox.grid(row=0, column=1, padx=5, pady=5)
        
        self.major_antecedent = tk.Entry(self.input_frame, width=5)
        self.major_antecedent.grid(row=0, column=2, padx=5, pady=5)
        
        self.major_entailment = tk.StringVar(value="⊨")
        self.major_entailment_radio_entails = tk.Radiobutton(self.input_frame, text="⊨", variable=self.major_entailment, value="⊨")
        self.major_entailment_radio_not_entails = tk.Radiobutton(self.input_frame, text="⊭", variable=self.major_entailment, value="⊭")
        self.major_entailment_radio_entails.grid(row=0, column=3, padx=5, pady=5)
        self.major_entailment_radio_not_entails.grid(row=0, column=4, padx=5, pady=5)
        
        self.major_consequent_neg = tk.BooleanVar(value=False)
        self.major_consequent_neg_checkbox = tk.Checkbutton(self.input_frame, text="¬", variable=self.major_consequent_neg)
        self.major_consequent_neg_checkbox.grid(row=0, column=5, padx=5, pady=5)
        
        self.major_consequent = tk.Entry(self.input_frame, width=5)
        self.major_consequent.grid(row=0, column=6, padx=5, pady=5)
        
        # Minor premise
        self.minor_label = tk.Label(self.input_frame, text="Minor Premise:")
        self.minor_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.minor_antecedent_neg = tk.BooleanVar(value=False)
        self.minor_antecedent_neg_checkbox = tk.Checkbutton(self.input_frame, text="¬", variable=self.minor_antecedent_neg)
        self.minor_antecedent_neg_checkbox.grid(row=1, column=1, padx=5, pady=5)
        
        self.minor_antecedent = tk.Entry(self.input_frame, width=5)
        self.minor_antecedent.grid(row=1, column=2, padx=5, pady=5)
        
        self.minor_entailment = tk.StringVar(value="⊨")
        self.minor_entailment_radio_entails = tk.Radiobutton(self.input_frame, text="⊨", variable=self.minor_entailment, value="⊨")
        self.minor_entailment_radio_not_entails = tk.Radiobutton(self.input_frame, text="⊭", variable=self.minor_entailment, value="⊭")
        self.minor_entailment_radio_entails.grid(row=1, column=3, padx=5, pady=5)
        self.minor_entailment_radio_not_entails.grid(row=1, column=4, padx=5, pady=5)
        
        self.minor_consequent_neg = tk.BooleanVar(value=False)
        self.minor_consequent_neg_checkbox = tk.Checkbutton(self.input_frame, text="¬", variable=self.minor_consequent_neg)
        self.minor_consequent_neg_checkbox.grid(row=1, column=5, padx=5, pady=5)
        
        self.minor_consequent = tk.Entry(self.input_frame, width=5)
        self.minor_consequent.grid(row=1, column=6, padx=5, pady=5)
        
        # Conclusion
        self.conc_label = tk.Label(self.input_frame, text="Conclusion:")
        self.conc_label.grid(row=2, column=0, padx=5, pady=5)
        
        self.conc_antecedent_neg = tk.BooleanVar(value=False)
        self.conc_antecedent_neg_checkbox = tk.Checkbutton(self.input_frame, text="¬", variable=self.conc_antecedent_neg)
        self.conc_antecedent_neg_checkbox.grid(row=2, column=1, padx=5, pady=5)
        
        self.conc_antecedent = tk.Entry(self.input_frame, width=5)
        self.conc_antecedent.grid(row=2, column=2, padx=5, pady=5)
        
        self.conc_entailment = tk.StringVar(value="⊨")
        self.conc_entailment_radio_entails = tk.Radiobutton(self.input_frame, text="⊨", variable=self.conc_entailment, value="⊨")
        self.conc_entailment_radio_not_entails = tk.Radiobutton(self.input_frame, text="⊭", variable=self.conc_entailment, value="⊭")
        self.conc_entailment_radio_entails.grid(row=2, column=3, padx=5, pady=5)
        self.conc_entailment_radio_not_entails.grid(row=2, column=4, padx=5, pady=5)
        
        self.conc_consequent_neg = tk.BooleanVar(value=False)
        self.conc_consequent_neg_checkbox = tk.Checkbutton(self.input_frame, text="¬", variable=self.conc_consequent_neg)
        self.conc_consequent_neg_checkbox.grid(row=2, column=5, padx=5, pady=5)
        
        self.conc_consequent = tk.Entry(self.input_frame, width=5)
        self.conc_consequent.grid(row=2, column=6, padx=5, pady=5)
        
        self.process_button = tk.Button(self.input_frame, text="Check validity", command=self.process_input)
        self.process_button.grid(row=3, column=0, columnspan=7, pady=10)
        
        # Frame for output text / console output
        self.output_frame = tk.Frame(self.root)
        self.output_frame.pack(pady=10)
        
        self.output_label = tk.Label(self.output_frame, text="Output:")
        self.output_label.pack()
        
        self.output_text = tk.Text(self.output_frame, height=2, width=80)
        self.output_text.pack()
        
        # Venn diagram frame
        self.venn_frame = tk.Frame(self.root)
        self.venn_frame.pack(pady=10)
        
        # Premises Venn diagram frame
        self.premises_frame = tk.Frame(self.venn_frame)
        self.premises_frame.pack(side=tk.LEFT, padx=10)
        
        self.premises_label = tk.Label(self.premises_frame, text="Premises")
        self.premises_label.pack()
        
        self.premises_canvas = None
        
        # Conclusion Venn diagram frame
        self.conc_frame = tk.Frame(self.venn_frame)
        self.conc_frame.pack(side=tk.RIGHT, padx=10)
        
        self.conc_label = tk.Label(self.conc_frame, text="Conclusion")
        self.conc_label.pack()
        
        self.conc_canvas = None
    
    def process_input(self):
        major_premise = f"{'¬' if self.major_antecedent_neg.get() else ''}{self.major_antecedent.get()} {self.major_entailment.get()} {'¬' if self.major_consequent_neg.get() else ''}{self.major_consequent.get()}"
        minor_premise = f"{'¬' if self.minor_antecedent_neg.get() else ''}{self.minor_antecedent.get()} {self.minor_entailment.get()} {'¬' if self.minor_consequent_neg.get() else ''}{self.minor_consequent.get()}"
        conclusion = f"{'¬' if self.conc_antecedent_neg.get() else ''}{self.conc_antecedent.get()} {self.conc_entailment.get()} {'¬' if self.conc_consequent_neg.get() else ''}{self.conc_consequent.get()}"
        
        raw_input = f"{major_premise}, {minor_premise}, {conclusion}"
        
        if not raw_input:
            messagebox.showerror("Input Error", "Please enter a syllogism.")
            return
        
        self.output_text.delete(1.0, tk.END)
        
        try:
            # Process input and generate output
            evaluation = self.main_controller.process_input(raw_input)
            
            # Display output code
            self.output_text.insert(tk.END, f"Syllogism is: {evaluation['outputCode']}\n")
            
            # Display Venn diagrams
            premise_text = f"{major_premise}, {minor_premise}"
            self.display_venn_diagrams(evaluation['premises'], evaluation['conclusion'], premise_text, conclusion)
        
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))
    
    def display_venn_diagrams(self, premises_manager, conclusion_manager, premise_text, conclusion_text):
        if self.premises_canvas:
            self.premises_canvas.get_tk_widget().pack_forget()
        if self.conc_canvas:
            self.conc_canvas.get_tk_widget().pack_forget()
        
        # Update labels with raw input
        self.premises_label.config(text=f"Premises: {premise_text}")
        self.conc_label.config(text=f"Conclusion: {conclusion_text}")
        
        # Create Venn diagrams using the venn_diagram module
        self.premises_canvas = create_venn_diagram(premises_manager, self.premises_frame)
        self.premises_canvas.get_tk_widget().pack()
        
        self.conc_canvas = create_venn_diagram(conclusion_manager, self.conc_frame)
        self.conc_canvas.get_tk_widget().pack()