from syllogism_controller import SyllogismController
from main_controller import MainController

def main():
    print("Started main()")
    #control = SyllogismController()
    #control.process_input("e ⊨ s, s ⊨ g, s ⊨ e")
    
    #print("Started main() again")
    #control = SyllogismController()
    #control.process_input("a ⊨ b, b ⊨ ¬c, a ⊨ c")
    
    #SyllogismController().process_input("a ⊨ b, b ⊨ c, a ⊨ c")
    #main_controller = MainController()
    #main_controller.process_syllogism_input("a ⊨ b, b ⊨ c, a ⊨ c")
    
    syllog_control = SyllogismController()
    
    
    # Define the possible types of statements
    statements = [
        " ⊨ ",
        " ⊨ ¬",
        " ⊭ ¬",
        " ⊭ "
    ]

    # Define the four types of moods for a syllogism
    figures = [
        (("B", "C"), ("A", "B"), ("A", "C")),
        (("C", "B"), ("A", "B"), ("A", "C")),
        (("B", "C"), ("B", "A"), ("A", "C")),
        (("C", "B"), ("B", "A"), ("A", "C"))
    ]
    
    valid_count = 0

    # Generate all possible syllogisms
    for figure in figures:
        for major in statements:
            for minor in statements:
                for conclusion in statements:
                    # Create entries for each tuple in the figure
                    major_premise = f"{figure[0][0]} {major} {figure[0][1]}"
                    minor_premise = f"{figure[1][0]} {minor} {figure[1][1]}"
                    conclusion_premise = f"{figure[2][0]} {conclusion} {figure[2][1]}"
                    syllogism_text = f"{major_premise}, {minor_premise}, {conclusion_premise}"
                    evaluation = SyllogismController().process_syllogism_input(syllogism_text)
                    if evaluation['outputCode']:
                        print(syllogism_text)
                        print("Valid")
                        valid_count += 1
    print(f"Valid count: {valid_count}")
    
    

if __name__ == "__main__":
    main()
    
# c ⊭ b, b ⊭ a, c ⊭ a ¬¬¬¬¬
# e ⊨ s, s ⊨ g, e ⊨ g
# a ⊭ b, b ⊭ c, a ⊭ c

