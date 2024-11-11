from syllogism_controller import SyllogismController

def main():
    print("Started main()")
    control = SyllogismController()
    #control.process_input("e ⊨ s, s ⊨ g, e ⊨ g")
    
    #print("Started main() again")
    #control = SyllogismController()
    control.process_input("a ⊨ b, b ⊭ c, b ⊨ c")

if __name__ == "__main__":
    main()
    
# c ⊭ b, b ⊭ a, c ⊭ a ¬¬¬¬¬
# e ⊨ s, s ⊨ g, e ⊨ g
# a ⊭ b, b ⊭ c, a ⊭ c

