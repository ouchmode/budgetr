import json

from rich.prompt import Prompt

class Budget:
    """
    this class handles the budget info.

    setting, modifying, removing a budget as well as an option to set if it is 
    a daily, weekly, or monthly budget.

    mostly using this to show some stats on the main menu.
    """  

    def __init__(self, occurs=None, amt=None):
        """
        setting attributes for a budget like occurrence and amount.
        """
        self.occurs = occurs
        self.amt = amt
   

    def is_budget_set(self):
        """
        based on the amt (if it is empty or not) return False or True.
        """
        return bool(self.amt)


    def save_budget(self):
        """
        save budget to json.
        """
        with open('./data/budget.json', 'w') as file:
            json.dump({"amt": self.amt, "occurs": self.occurs}, file)


    def load_budget(self):
        """
        Retrieve budget data from the .json file.
        """
        try:
            with open('./data/budget.json', 'r') as file:
                data = json.load(file)
                
                # making sure the keys exist in the file.
                if "occurs" in data:
                    self.occurs = data["occurs"]
                else:
                    self.occurs = ""

                if "amt" in data:
                    self.amt = data["amt"]
                else:
                    self.amt = ""
        except (FileNotFoundError, json.JSONDecodeError):
            self.occurs = ""
            self.amt = ""


    def remove_budget(self):
        """
        a budget isn't necessarily required, so it can be removed if desired.
        """
        self.amt = ""
        self.occurs = ""
        self.save_budget()


    def set_budget(self):
        """
        set a budget amount and occurrence, saves to json.
        """
        # the set option is always present.
        print("\n-- Set Budget --")
        self.occurs = Prompt.ask("Enter Occurrence ", 
                                  choices=['Daily','Weekly','Monthly']
                                  ).strip().title()
        self.amt = input("Enter Budget Amount: ").strip()

        self.budget = Budget(self.occurs, self.amt)
        self.budget.save_budget()
        print("\nBudget saved!")
