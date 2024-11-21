import tkinter as tk
from tkinter import messagebox
from venn_diagram import gen_matplot_venn_output, gen_matplot_venn_interactive

class SyllogismGUI:
    def __init__(self, root, main_controller):
        self.root = root
        self.root.title("Syllogism Evaluator")
        self.main_controller = main_controller
        
        self.create_input_text_frame(rowIn=0)
        self.create_interactive_venn_frame(rowIn=4) 
        self.create_output_text_frame(rowIn=5)
        self.create_output_venn_frame(rowIn=6)
        
        # If input not processed then the output boxes remain empty
        self.process_input()

    def create_input_text_frame(self, rowIn):
        self.input_frame = tk.Frame(self.root)
        self.input_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        self.create_premise_row("Major Premise:", rowIn, "A", "B", 0)
        self.create_premise_row("Minor Premise:", rowIn+1, "B", "C", 1)
        self.create_premise_row("Conclusion:", rowIn+2, "A", "C", 2)
        
        self.process_button = tk.Button(self.input_frame, text="Check validity", command=self.process_input)
        self.process_button.grid(row=rowIn+3, column=0, columnspan=7, pady=10)

    def create_premise_row(self, label_text, row, antecedent_default, consequent_default, case_code):
        tk.Label(self.input_frame, text=label_text, anchor="center").grid(row=row, column=0, padx=5, pady=5)
        
        antecedent_neg_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.input_frame, text="¬", variable=antecedent_neg_var).grid(row=row, column=1, padx=5, pady=5)
        
        antecedent_entry = tk.Entry(self.input_frame, width=5)
        antecedent_entry.grid(row=row, column=2, padx=5, pady=5)
        antecedent_entry.insert(0, antecedent_default)
        
        entailment_var = tk.StringVar(value="⊨")
        tk.Radiobutton(self.input_frame, text="⊨", variable=entailment_var, value="⊨").grid(row=row, column=3, padx=5, pady=5)
        tk.Radiobutton(self.input_frame, text="⊭", variable=entailment_var, value="⊭").grid(row=row, column=4, padx=5, pady=5)
        
        consequent_neg_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self.input_frame, text="¬", variable=consequent_neg_var).grid(row=row, column=5, padx=5, pady=5)
        
        consequent_entry = tk.Entry(self.input_frame, width=5)
        consequent_entry.grid(row=row, column=6, padx=5, pady=5)
        consequent_entry.insert(0, consequent_default)
        
        if case_code == 0:
            self.major_antecedent_neg = antecedent_neg_var
            self.major_antecedent = antecedent_entry
            self.major_entailment = entailment_var
            self.major_consequent_neg = consequent_neg_var
            self.major_consequent = consequent_entry
        elif case_code == 1:
            self.minor_antecedent_neg = antecedent_neg_var
            self.minor_antecedent = antecedent_entry
            self.minor_entailment = entailment_var
            self.minor_consequent_neg = consequent_neg_var
            self.minor_consequent = consequent_entry
        elif case_code == 2:
            self.conc_antecedent_neg = antecedent_neg_var
            self.conc_antecedent = antecedent_entry
            self.conc_entailment = entailment_var
            self.conc_consequent_neg = consequent_neg_var
            self.conc_consequent = consequent_entry

    def create_interactive_venn_frame(self, rowIn):
        self.interactive_frame = tk.Frame(self.root)
        self.interactive_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        self.create_interactive_venn_diagram_frame("Interactive Premises", self.interactive_frame, rowIn, 0)
        self.create_interactive_venn_diagram_frame("Interactive Conclusion", self.interactive_frame, rowIn, 1)

    def create_output_text_frame(self, rowIn):
        self.output_frame = tk.Frame(self.root)
        self.output_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        self.output_label = tk.Label(self.output_frame, text="Output:", anchor="center")
        self.output_label.pack()
        
        self.output_text = tk.Text(self.output_frame, height=2, width=60)
        self.output_text.pack(expand=True, fill="both")

    def create_output_venn_frame(self, rowIn):
        self.output_venn_frame = tk.Frame(self.root)
        self.output_venn_frame.grid(row=rowIn, column=0, padx=10, pady=10)
        
        self.create_output_venn_diagram_frame("Premises", self.output_venn_frame, side=tk.LEFT)
        self.create_output_venn_diagram_frame("Conclusion", self.output_venn_frame, side=tk.RIGHT)

    def create_interactive_venn_diagram_frame(self, title, parent_frame, rowIn, column):
        frame = tk.Frame(parent_frame)
        frame.grid(row=rowIn, column=column, padx=10, pady=10)
        
        label = tk.Label(frame, text=title, anchor="center")
        label.pack()
        
        canvas = gen_matplot_venn_interactive(frame)
        canvas.get_tk_widget().pack(expand=True, fill="both")
        
        setattr(self, f"{title.lower().replace(' ', '_')}_frame", frame)
        setattr(self, f"{title.lower().replace(' ', '_')}_canvas", canvas)

    def create_output_venn_diagram_frame(self, title, parent_frame, side):
        frame = tk.Frame(parent_frame)
        frame.pack(side=side, padx=10, expand=True, fill="both")
        
        label = tk.Label(frame, text=title, anchor="center")
        label.pack()
        
        setattr(self, f"{title.lower()}_frame", frame)
        setattr(self, f"{title.lower()}_label", label)
        setattr(self, f"{title.lower()}_canvas", None)

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
            evaluation = self.main_controller.process_input(raw_input)
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
        
        self.premises_canvas = gen_matplot_venn_output(premises_manager, self.premises_frame)
        self.premises_canvas.get_tk_widget().pack(expand=True, fill="both")
        
        self.conclusion_canvas = gen_matplot_venn_output(conclusion_manager, self.conclusion_frame)
        self.conclusion_canvas.get_tk_widget().pack(expand=True, fill="both")