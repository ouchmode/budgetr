# psl imports.
import json

# rich imports.
from rich.prompt import Prompt
from rich import print

# custom imports.
from classes.transaction import Transaction


class Budget:
    """
    this class handles the budget info.

    setting, modifying, removing a budget as well as an option to set if it is 
    a daily, weekly, or monthly budget.

    mostly using this to show some stats on the main menu.
    """  

    def __init__(self, occurs=None, amt=0):
        """
        setting attributes for a budget like occurrence and amount.
        """
        self.occurs = occurs
        self.amt = amt
        self.b = self.load_budget()
   

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

        self.budget = Budget(self.occurs, int(self.amt))
        self.budget.save_budget()
        print("\nBudget saved!")


    def budget_progress(self):
        """
        displays the progress of the set budget compared to the relative
        expense totals. (if it occurs daily, it compares against the today_tot)

        red = over budget
        green = under budget
        """
        txn = Transaction()

        # not sure why I have to do this since it's default is 0 unless python 
        # doesn't infer the type that way. 
        # this prevents some error I was getting that I did not understand lol.

        # i think i know how to fix having to NOT do this but that is for another day. :)
        amt = int(self.amt)
        
        if self.is_budget_set():
            if self.occurs == "Daily":
                today_tot = txn.today_total()
                # if the total exceeds the budget amount.
                if today_tot > amt:
                    budget_to_expense_pct = 100 * (today_tot / amt)
                    return f"PROGRESS: [bold red]%{round(budget_to_expense_pct)}[/bold red]"
                else:
                    budget_to_expense_pct = 100 - (100 * ((amt - today_tot) / amt))
                    return f"PROGRESS: [bold green]%{round(budget_to_expense_pct)}[/bold green]"

            if self.occurs == "Weekly":
                weekly_tot = txn.week_total()
                if weekly_tot > amt:
                    budget_to_expense_pct = 100 * (weekly_tot / amt)
                    return f"PROGRESS: [bold red]%{round(budget_to_expense_pct)}[/bold red]"
                else:
                    budget_to_expense_pct = 100 - (100 * ((amt - weekly_tot) / amt))
                    return f"PROGRESS: [bold green]%{round(budget_to_expense_pct)}[/bold green]"

            if self.occurs == "Monthly":
                monthly_tot = txn.month_total()
                if monthly_tot > amt:
                    budget_to_expense_pct = 100 * (monthly_tot / amt)
                    return f"PROGRESS: [bold red]%{round(budget_to_expense_pct)}[/bold red]"
                else:
                    budget_to_expense_pct = 100 - (100 * ((amt - monthly_tot) / amt))
                    return f"PROGRESS: [bold green]%{round(budget_to_expense_pct)}[/bold green]"

        else:
            print("No budget set.")
