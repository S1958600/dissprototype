from syllogism_controller import SyllogismController

def main():
    print("Started main()")
    control = SyllogismController()
    control.process_input("e ⊨ s, s ⊨ g, e ⊨ g")

if __name__ == "__main__":
    main()