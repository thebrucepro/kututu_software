class Dialogue:
    def __init__(self, text, choices=None):
        self.text = text
        self.choices = choices or []

    def display(self):
        print(self.text)
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")
        selection = int(input("Elige una opción: "))
        return self.choices[selection - 1]
        
