class Story:
    def __init__(self):
        self.flags = {"hablar": False, "atacar": False, "huir": False}

    def update_flags(self, choice):
        if choice == "Hablar":
            self.flags["hablar"] = True
        elif choice == "Atacar":
            self.flags["atacar"] = True
        elif choice == "Huir":
            self.flags["huir"] = True

    def get_ending(self):
        if self.flags["hablar"]:
            return "Final pacífico"
        elif self.flags["atacar"]:
            return "Final heroico"
        elif self.flags["huir"]:
            return "Final cobarde"
        else:
            return "Final neutral"
          
