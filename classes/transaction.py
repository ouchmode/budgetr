from pathlib import Path
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box


class Transaction:

    """handles all transaction CRUD actions + saving & loading to JSON."""

    def __init__(self):
        """
        an instance of this class sets up the path to the JSON file and 
        holds a dictionary of each transaction called 'transactions'. 
        this comes from the load_txn() method.
        """
        self.filepath = './data/transactions.json'
        self.transactions = self.load_txn()


    def add_transaction(self, amount, category, date):
        """
        add a new transaction as a dict and save it.
        """
        console = Console()

        txn_id = len(self.transactions) + 1
        self.transactions[txn_id] = {
            "amount": float(amount),
            "category": category,
            "date": date
        }
        self.save_txn()
        
        print("\n")

        added = f"-ID: {txn_id}"
        added += f"\n-AMOUNT: ${float(amount):.2f}"
        added += f"\n-CATEGORY: {category}"
        added += f"\n-DATE: {date}"
        
        panel = Panel(added, 
                      title="Transaction Added!", 
                      border_style="green", 
                      width=50)    
        
        console.print(panel)
        print("\n\n")


    def view_transactions(self):
        """
        displays all transactions.
        """
        console = Console()
        table = Table(title="//$---TRANSACTIONS---$//", 
                      border_style="white", 
                      box=box.SIMPLE_HEAD, 
                      row_styles=["dim", ""], 
                      highlight=True)

        if not self.transactions:
            print("\nNo transactions found.")
            return

        table.add_column("ID", width=10, header_style="magenta")
        table.add_column("AMOUNT", width=15, header_style="magenta")
        table.add_column("CATEGORY", width=20, no_wrap=False, header_style="magenta")
        table.add_column("DATE", width=10, header_style="magenta")
        for txn_id, txn in self.transactions.items():
            amount_str = f"${txn['amount']:.2f}"
            table.add_row(txn_id, amount_str, txn['category'].title(), txn['date'])

        console.print(table)
        print("\n\n")


    def update_transaction(self, user_txn_id, new_amt=0.0, new_cat="", new_date=""):
        """
        update a specific key's values in a transaction. saves the update 
        using save_txn.
        """
        table = Table(title="//$---TRANSACTIONS---$//", 
                      border_style="white", 
                      box=box.SIMPLE_HEAD, 
                      highlight=True)
        console = Console()

        table.add_column("ID", width=10, header_style="magenta")
        table.add_column("AMOUNT", width=10, header_style="magenta")
        table.add_column("CATEGORY", width=20, no_wrap=False, header_style="magenta")
        table.add_column("DATE", width=10, header_style="magenta")

        # need to make sure the id entered is valid. if it is, update the 
        # key's value to new_value and run the save.
        if user_txn_id in self.transactions:
            
            # showing the selected transaction's details in a table.
            amt_for_table = f"${new_amt:,.2f}"
            table.add_row(user_txn_id, amt_for_table, new_cat, new_date)
            console.print(table)
            print("\n")

            self.transactions[user_txn_id] = {
                "amount": float(new_amt),
                "category": new_cat,
                "date": new_date,
            }      
            self.save_txn()
            print(f"\n\nTransaction {user_txn_id} updated.\n\n")
        else:
            print("\n\nInvalid transaction ID or key.")


    def save_txn(self):
        """saves to the JSON file."""
        path = Path(self.filepath)
        if not path.exists():
            print(f"\n\n[ERROR]: {self.filepath} does not exist."
                  f"\nMake sure exists under the project root.")
        path.write_text(json.dumps(self.transactions, indent=4))


    def load_txn(self):
        """loads from the JSON file."""
        path = Path(self.filepath)
        if not path.exists():
            return {}

        content = path.read_text().strip()
        if not content:
            return {}

        return json.loads(content)  
