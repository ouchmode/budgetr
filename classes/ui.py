# psl imports.
from datetime import datetime
import sys

# rich imports.
from rich.console import Console
from rich.box import DOUBLE_EDGE
from rich.prompt import Confirm
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print

# project imports.
from classes.transaction import Transaction
from classes.budget import Budget
from util import date_stuff


class UserInterface:

    """
    this class is used to display different interfaces. mostly to organize the 
    different menus that will be appearing.
    """

    def __init__(self, menu="", username="", date=""):
        self.menu = menu 
        self.username = username 
        self.date = date 
        self.budget = Budget()
        self.budget.load_budget()

    def main_menu(self):
        """
        runs the main menu containing all of the options for adding, viewing, 
        deleting transactions, view totals, perform budgeting and exit.

        only ran once in main.py when the program starts.
        """
                
        console = Console()

        while True:
            self.greeting()

            menu = "[cyan]0.[/] Budgeting"
            menu += "\n[cyan]1.[/] Add Transaction"
            menu += "\n[cyan]2.[/] View Transaction"
            menu += "\n[cyan]3.[/] Delete Transaction"
            menu += "\n[cyan]4.[/] Totals"
            menu += "\n[cyan]5.[/] Exit"
           
            panel = Panel(menu, title="Main Menu", box=DOUBLE_EDGE, border_style="cyan", width=50)
            console.print(panel)
            
            ans = input("\nSelect an Option: ").strip()
            print("\n\n")

            match ans:
                # budgeting options.
                case "0":
                    print("\n")
                    self.budget_menu()

                # add transaction.
                case "1":
                    while True:
                        # txn amount user input.
                        txn_amt_input = float(input("\nEnter Transaction Amount: ").strip())
                        txn_amt_input = f"{txn_amt_input:.2f}" # formatting to 2 dec.
                            
                        # txn category user input (rent, utility, snacks, etc.)
                        txn_cat_input = input("\nEnter Transaction Category (e.g., 'Rent'): ").strip()
                        
                        # txn date user input. if nothing is entered, use today's date.
                        while True:
                            txn_date_input = input(f"\nEnter Transaction Date "
                                                   f"(MM/DD/YYYY - can leave blank"
                                                   f"for today's date): ").strip()

                            if txn_date_input == "":
                                txn_date = date_stuff.get_current_date_time_fmtd()
                                break
                            try:
                                parsed_date = datetime.strptime(txn_date_input, 
                                                                "%m/%d/%Y")
                                txn_date = parsed_date.strftime("%m/%d/%Y")
                                break
                            except ValueError:
                                print("Invalid date format. Please enter the date as MM/DD/YYYY.")
                            
                        txn = Transaction()
                        txn.add_transaction(float(txn_amt_input), 
                                            txn_cat_input, 
                                            txn_date)
                        
                        # this is made in ui.py as it's mainly a prompt that 
                        # redirects to add_transaction() in transaction.py.
                        self.add_more_txn()

                case "2":
                    # shows all transactions, rendered in a table view.
                    txn = Transaction()
                    txn.view_transactions()
                    self.back_to_main_or_exit()
                # exit.
                case "5":
                    print("Exiting... Bye!")
                    break
                case _:
                    print("\nInvalid option.")


    def greeting(self):
        """
        greets the user and displays the current time along with their set 
        budget. 
        """
        twelve_hr = datetime.today().strftime('%I:%M %p')
        twenty_four_hr = datetime.today().strftime('%H:%M')

        print(f"\n{'=' * 71}")
        print("[bold white] /$$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$$$ /$$$$$$$[/bold white]") 
        print("[bold white]| $$__  $$| $$  | $$| $$__  $$ /$$__  $$| $$_____/|__  $$__/| $$__  $$[/bold white]")
        print("[bold white]| $$ \\ $$|  $$  | $$| $$  \\ $$| $$  \\__/| $$         | $$   | $$  \\ $$[/bold white]")
        print("[bold white]| $$$$$$$ | $$  | $$| $$  | $$| $$ /$$$$| $$$$$      | $$   | $$$$$$$/[/bold white]")
        print("[bold white]| $$__  $$| $$  | $$| $$  | $$| $$|_  $$| $$__/      | $$   | $$__  $$[/bold white]")
        print("[bold white]| $$  \\ $$| $$  | $$| $$  | $$| $$  \\ $$| $$         | $$   | $$  \\ $$[/bold white]")
        print("[bold white]| $$$$$$$/|  $$$$$$/| $$$$$$$/|  $$$$$$/| $$$$$$$$   | $$   | $$  | $$[/bold white]")
        print("[bold white]|_______/  \\______/ |_______/  \\______/ |________/   |__/   |__/  |__/[/bold white]")
        print(f"\nGood {date_stuff.get_time_period_of_day()}! "
              f"It is currently {twelve_hr} ({twenty_four_hr})")

        if self.budget.is_budget_set():
            print(f"\nCurrent Budget: ${self.budget.amt} | "
                  f"Occurs: {self.budget.occurs}")
        else:
            print("\nNo budget is currently set.")
        print(f"{'=' * 70}")


    def budget_menu(self):
        """
        menu specifically for budgeting. when selecting '0' in the main menu, 
        this menu appears and allows the user to set, update and remove a 
        budget. 

        the update and remove options are only present if a budget is set.
        """
        console = Console()

        while True:
            budget_menu = "1. Set Budget"
            if self.budget.is_budget_set():
                budget_menu += "\n2. Update Budget"
                budget_menu += "\n3. Remove Budget"
            budget_menu += "\n4. Back to Main Menu"
        
            panel = Panel(budget_menu, 
                          title="Budget Menu", 
                          border_style="cyan", 
                          width=50)
            console.print(panel)

            ans = input("\nSelect an Option: ").strip()
            print("\n\n")

            match ans:
                case "1":
                    # the set option is always present.
                    print("\n-- Set Budget --")
                    budget_amt = input("Enter Budget Amount: ").strip()
                    budget_occur = Prompt.ask("Enter Occurrence ", 
                                              choices=['Daily','Weekly','Monthly']
                                              ).strip().title()
                    self.budget = Budget(budget_occur, budget_amt)
                    self.budget.save_budget()
                    print("\nBudget saved!")

                case "2":
                    if self.budget.is_budget_set():
                        print(f"\n-- Your Budget --"
                              f"\n====Amount: {self.budget.amt}"
                              f"\n====Occurs: {self.budget.occurs}")
                    else:
                        print("You need to set a budget first using option 1.")

                case "3":
                    if self.budget.is_budget_set():
                        self.budget.remove_budget()
                        print("Budget removed.\n")

                case "4":
                    break

                case _:
                    print("\nInvalid option.\n\n")


    def back_to_main_or_exit(self):
        """
        yes/no menu to go back to the main menu or exit the program 
        entirely.
        """
        ans = Confirm.ask("Back to Main Menu?")
        # the y/n from Confirm.ask() returns True or False, and apparently the 
        # match-case doesn't work with bools.
        ans = int(ans)
        while True:
            match ans:
                case 1:
                    self.main_menu()
                case 0:
                    print("\n\nExiting... Bye!")
                    sys.exit()
                case _:
                    print("\nInvalid option. Only 'y' or 'n' should be entered.\n\n")


    def add_more_txn(self):
        """
        yes/no menu to add another transaction or go back to the main menu.
        """
        ask_txn = Confirm.ask("\nAdd Another Transaction?")
        ask_txn = int(ask_txn)
        while True:
            match ask_txn:    
                case 1:
                    break
                case 0:
                    return self.main_menu()
                case _:
                    print("\nInvalid option. Only 'y' or 'n' should be entered.\n\n")
