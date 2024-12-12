# main.py
from RoommateFinderApp import RoommateFinderApp  # Importing the RoommateFinderApp class from RoommateFinderApp.py

# Main entry point for the application
if __name__ == "__main__":
    # This block ensures that the following code only runs when this file is executed directly
    # (and not when it is imported as a module in another file)
    app = RoommateFinderApp()  # Creates an instance of the RoommateFinderApp class
    app.run()  # Starts the Tkinter main event loop, Calls the method to display the menu and start the application