# psl imports.
from datetime import datetime, timedelta

# rich imports.
from rich.console import Console 
from rich.panel import Panel
from rich.table import Table
from rich import print
from rich import box

# custom module imports.
import util.date_stuff as dates
import util.file_mgmt as files
import util.tables as tables

class Transaction:

    """handles all transaction CRUD actions + saving & loading to JSON."""

    def __init__(self):
        """
        an instance of this class sets up the path to the JSON file and 
        holds a dictionary of each transaction called 'transactions'. 
        this comes from the load_txn() method.
        """
        self.filepath = './data/transactions.json'
        self.transactions = files.load_txn(self.filepath)


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
        files.save_txn(self.filepath, self.transactions)
        
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
        print("\n")


    def view_transactions(self):
        """
        displays all transactions.
        """
        console = Console()

        table = tables.all_txns_table_setup() 

        for txn_id, txn in self.transactions.items():
            amount_str = f"${txn['amount']:.2f}"
            if txn['category'] == "" or txn['category']:
                table.add_row(str(txn_id), amount_str, txn['category'].title(), txn['date'])

        console.print(table)
        print("\n\n")   


    def update_transaction(self, user_txn_id, new_amt=0.0, new_cat="", new_date=""):
        """
        update a specific key's values in a transaction. saves the update 
        using save_txn.
        """
        console = Console()
        table = tables.all_txns_table_setup() 

        # showing the selected transaction's details in a table.
        amt_for_table = f"${new_amt:,.2f}"
        table.add_row(user_txn_id, amt_for_table, new_cat, new_date)
        console.print(table)

        self.transactions[user_txn_id] = {
            "amount": float(new_amt),
            "category": new_cat,
            "date": new_date,
        }      
        files.save_txn(self.filepath, self.transactions)
        panel = Panel(f"\n\t\tTransaction {user_txn_id} updated.\n\n",
                      title="Transaction Updated!", 
                      border_style="green", 
                      width=50)

        console.print(panel) 


    def delete_transaction(self, user_txn_id):
        """
        remove a transaction based on a selected id. 
        """
        del self.transactions[user_txn_id]
        files.save_txn(self.filepath, self.transactions)


    def get_totals(self, budget_occurs):
        """
        gets daily, weekly and monthly totals based on entered transactions.
        
        if a budget is set, these will be used against it to show how above or 
        below your budget you are.
        """
        # today = datetime.today().strftime('%m-%d-%Y')
        console = Console()
        table = Table(border_style="white", 
                      box=box.SIMPLE_HEAD, 
                      row_styles=["dim", ""], 
                      highlight=True)
        
        today_tot = self.today_total()
        today_tot_str = f"${today_tot:,.2f}"

        week_tot = self.week_total()
        week_tot_str = f"${week_tot:,.2f}"

        month_tot = self.month_total()
        month_tot_str = f"${month_tot:,.2f}"

        # changing the color of the set budget's occurrence column so it stands 
        # out.

        # im not sure if i can change the color of an individual amount in the table.
        if budget_occurs == "Daily":
            table.add_column("TODAY", width=23, header_style="green", justify="center")
        else:
            table.add_column("TODAY", width=23, header_style="bright_black", justify="center")

        if budget_occurs == "Weekly":
            table.add_column("WEEK", width=23, header_style="green", justify="center")
        else:
            table.add_column("WEEK", width=23, header_style="bright_black", justify="center")

        if budget_occurs == "Monthly":
            table.add_column("MONTH", width=23, header_style="green", justify="center")
        else:
            table.add_column("MONTH", width=23, header_style="bright_black", justify="center")
        
        table.add_row(today_tot_str, week_tot_str, month_tot_str)

        panel = Panel(table, 
                      title="TOTALS", 
                      border_style="green", 
                      width=70)

        console.print(panel)
     

    def today_total(self):
        """
        returns the total of all transactions that fall within the same day.
        """
        today_tot = 0
        for v in self.transactions.values():
            if v['date'] == datetime.strftime(dates.get_current_date(), '%m/%d/%Y'):
                if v['amount']:
                    today_tot += v['amount']
            else:
                continue
        
        return today_tot


    def week_total(self):
        """
        Returns the total for all transactions that fall within the current week.
        """
        week_tot = 0

        today = dates.get_current_date()
        weekday_num = today.weekday()

        start_of_week = today - timedelta(days=weekday_num)

        for txn in self.transactions.values():
            txn_datetime = datetime.strptime(txn['date'], '%m/%d/%Y')
            # checking if the txn date is within the current week. 
            if start_of_week <= txn_datetime <= today:
                week_tot += txn['amount']

        return week_tot


    def month_total(self):
        """
        returns the total for all transactions that fall within the same month.
        """
        month_tot = 0
        
        today = dates.get_current_date()
        curr_month_num = today.month 
        
        for txn in self.transactions.values():
            txn_date = datetime.strptime(txn['date'], '%m/%d/%Y')
            txn_date_mon = txn_date.month
            # comparing the month a transaction occurred to the current month.
            if txn_date_mon == curr_month_num:
                month_tot += txn['amount']
                
        return month_tot

