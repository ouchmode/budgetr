from rich.console import Console

from classes.ui import UserInterface

if __name__ == "__main__":
    console = Console()
    console.clear()

    ui = UserInterface()
    ui.main_menu()
