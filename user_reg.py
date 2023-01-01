# <-------It registers users------->
class RegisterUser:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.welcome = "Welcome to Angela Yu Flight Club"
        self.proclaimation = "We will check the best flight deals for you"

    def take_input(self):
        self.first_name = input("\nEnter your first name: ").title()
        self.last_name = input("Enter your last name: ").title()
        self.email = input("Enter your email: ")
        return self.first_name, self.last_name, self.email
