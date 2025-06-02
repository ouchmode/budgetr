from rich.table import Table
from rich import box

def all_txns_table_setup():
    table = Table(title="//$---TRANSACTIONS---$//", 
                  border_style="white", 
                  box=box.SIMPLE_HEAD, 
                  row_styles=["dim", ""], 
                  highlight=True)

    table.add_column("ID", width=10, header_style="magenta")
    table.add_column("AMOUNT", width=15, header_style="magenta")
    table.add_column("CATEGORY", width=20, no_wrap=False, header_style="magenta")
    table.add_column("DATE", width=10, header_style="magenta")
    
    return table

