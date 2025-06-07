from classes.ui import UserInterface

if __name__ == "__main__":
    ui = UserInterface()
    # custom clear_console() method to clear the console using the os module.
    # for some reason, some instances of powershell (at least on my machine) 
    # don't clear the console properly with rich.
    ui.clear_console()
    ui.main_menu()
