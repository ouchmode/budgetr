# psl imports.
from datetime import datetime
import sys
import os

# rich imports.
from rich.console import Console
from rich.box import DOUBLE_EDGE
from rich.prompt import Confirm
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
        self.txn = Transaction()
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
            menu += "\n[cyan]3.[/] Update Transaction"
            menu += "\n[cyan]4.[/] Delete Transaction"
            menu += "\n[cyan]5.[/] Exit"
           
            panel = Panel(menu, title="Main Menu", box=DOUBLE_EDGE, border_style="cyan", width=50)
            console.print(panel)
            
            ans = input("\nSelect an Option: ").strip()
            print("\n\n")

            match ans:
                # budgeting options.
                case "0":
                    self.clear_console()
                    print("\n")
                    self.budget_menu()

                # add transaction.
                case "1":
                    ui = UserInterface()
                    ui.clear_console()
                    while True:
                        txn_amt_input = float(input("\nEnter Transaction Amount: ").strip())
                        txn_cat_input = input("\nEnter Transaction Category (e.g., 'Rent'): ").strip()
                        print("\n")
                        txn_date = date_stuff.set_current_date_or_format_user_date()
                            
                        self.txn.add_transaction(float(txn_amt_input), 
                                            txn_cat_input, 
                                            txn_date)
                        
                        # this is made in ui.py as it's mainly a prompt that 
                        # redirects to add_transaction() in transaction.py.
                        self.add_or_update_more_txn("add")

                # shows all transactions, rendered in a table view.
                case "2":
                    self.clear_console()
                    if not self.txn.transactions:
                        print("\n\n\n\n[bold red]No transactions found.[/bold red]")
                        self.main_menu()
                    else:
                        self.txn.view_transactions()
                        self.back_to_main_or_exit()

                # update a transaction. shows a table of transactions to look 
                # through them and their ids before updating.
                case "3":
                    self.clear_console()
                    
                    user_txn_id = self.delete_and_update_prompts("update")

                    new_amount = float(input("\nEnter Transaction Amount: ").strip())
                    new_category = input("\nEnter Category: ".strip())        
                    new_date = date_stuff.set_current_date_or_format_user_date()

                    if user_txn_id:
                        self.txn.update_transaction(user_txn_id, 
                                               float(new_amount), 
                                               new_category, 
                                               new_date)
                    self.add_or_update_more_txn("update")
            
                # delete a transaction based on an id from a table of transactions.
                case "4":
                    self.clear_console()
                    
                    user_txn_id = self.delete_and_update_prompts("delete")

                    self.txn.delete_transaction(user_txn_id)

                # exit.
                case "5":
                    self.clear_console()
                    print("Exiting... Bye!")
                    break
                case _:
                    ui = UserInterface()
                    ui.clear_console()
                    print("\n\nInvalid option.")


    def greeting(self):
        """
        greets the user and displays the current time along with their set 
        budget. 
        """

        b_progress = self.budget.budget_progress()
        twelve_hr = datetime.today().strftime('%I:%M %p')
        twenty_four_hr = datetime.today().strftime('%H:%M')
        
        print("\n\n")
        print(f"="*70)
        print("[bold white] /$$$$$$$  /$$   /$$ /$$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$$$ /$$$$$$$[/bold white]") 
        print("[bold white]| $$__  $$| $$  | $$| $$__  $$ /$$__  $$| $$_____/|__  $$__/| $$__  $$[/bold white]")
        print("[bold white]| $$ \\ $$|  $$  | $$| $$  \\ $$| $$  \\__/| $$         | $$   | $$  \\ $$[/bold white]")
        print("[bold white]| $$$$$$$ | $$  | $$| $$  | $$| $$ /$$$$| $$$$$      | $$   | $$$$$$$/[/bold white]")
        print("[bold white]| $$__  $$| $$  | $$| $$  | $$| $$|_  $$| $$__/      | $$   | $$__  $$[/bold white]")
        print("[bold white]| $$  \\ $$| $$  | $$| $$  | $$| $$  \\ $$| $$         | $$   | $$  \\ $$[/bold white]")
        print("[bold white]| $$$$$$$/|  $$$$$$/| $$$$$$$/|  $$$$$$/| $$$$$$$$   | $$   | $$  | $$[/bold white]")
        print("[bold white]|_______/  \\______/ |_______/  \\______/ |________/   |__/   |__/  |__/[/bold white]")
        print(f"\nGood {date_stuff.get_time_period_of_day()}! "
              f"It is currently {twelve_hr} ({twenty_four_hr})\n")

        self.txn.get_totals(self.budget.occurs)
        
        if self.budget.is_budget_set():
            print(f"\nCurrent Budget: ${self.budget.amt} | "
                  f"Occurs: {self.budget.occurs} | "
                  f"Progress: {self.budget.budget_progress()}")
            print("\n")
        else:
            print("\nNo budget is currently set.")
        print(f"="*70)


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
                budget_menu += "\n2. Remove Budget"
            budget_menu += "\n3. Back to Main Menu"
        
            panel = Panel(budget_menu, 
                          title="Budget Menu", 
                          border_style="cyan", 
                          width=50)
            console.print(panel)

            ans = input("\nSelect an Option: ").strip()
            print("\n\n")

            match ans:
                # set a budget. not going to make an update as it seems 
                # redundant.
                case "1":
                    self.budget.set_budget()
                    self.budget.save_budget()
                # remove budget.
                case "2":
                    self.clear_console()
                    self.budget.remove_budget()
                    print("Budget removed.\n")
                # back to the main menu.
                case "3":
                    self.clear_console()
                    break

                case _:
                    self.clear_console()
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
        ui = UserInterface()

        while True:
            match ans:
                case 1:
                    ui.clear_console()
                    self.main_menu()
                case 0:
                    ui.clear_console()
                    print("\n\nExiting... Bye!")
                    sys.exit()
                case _:
                    print("\nInvalid option. Only 'y' or 'n' should be entered.\n\n")


    def add_or_update_more_txn(self, operation):
        """
        yes/no menu to add / update another transaction, or go back to the main menu.
        """
        ask_txn = Confirm.ask(f"\n{operation.title()} Another Transaction?")
        ask_txn = int(ask_txn)
        while True:
            match ask_txn:    
                case 1:
                    break
                case 0:
                    ui = UserInterface()
                    ui.clear_console()
                    return self.main_menu()
                case _:
                    print("\nInvalid option. Only 'y' or 'n' should be entered.")


    def delete_and_update_prompts(self, operation):
        """
        returning the user_txn_id for either a delete or update operation that 
        is specified as an argument.
        """
        if not self.txn.transactions:
            print("\n\n\n\n[bold red]No transactions found.[/bold red]")
            self.main_menu()
        else:
            self.txn.view_transactions()

        while True:
            user_txn_id = input(
                f"\nEnter the ID for the transaction you want to {operation.lower()}. "
                "\n\nAlternatively, enter 'm' for main menu, or 'e' to exit: "
            )

            if user_txn_id.lower() == 'm':
                ui = UserInterface()
                ui.clear_console()
                self.main_menu()
                return
            elif user_txn_id.lower() == 'e':
                ui = UserInterface()
                ui.clear_console()
                print("\nExiting... Bye!\n")
                sys.exit()
            
            if user_txn_id not in self.txn.transactions:
                print("\n[bold red]No transaction found for the selected ID.[/bold red]\n")
            else:
                return user_txn_id


    def clear_console(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

