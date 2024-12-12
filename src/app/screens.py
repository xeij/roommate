from tkinter import messagebox, Tk, Label, Button, Entry, Frame
from app.user_data import create_user, validate_user
from app.profile_manager import manage_profile_screen
from app.browse import search_user_by_name_or_building

def login_screen(window):
    """Display the login screen."""
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text="Login Page").pack()
    username_entry = Entry(window)
    username_entry.pack()
    password_entry = Entry(window, show="*")
    password_entry.pack()

    def login():
        username = username_entry.get()
        password = password_entry.get()
        if validate_user(username, password):
            messagebox.showinfo("Login", "Login Successful!")
            main_display_screen(window, username)
        else:
            messagebox.showerror("Login", "Invalid Username or Password")

    Button(window, text="Login", command=login).pack()
    Button(window, text="Create Account", command=lambda: create_account_screen(window)).pack()

def create_account_screen(window):
    """Display the create account screen."""
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text="Create Account").pack()
    username_entry = Entry(window)
    username_entry.pack()
    password_entry = Entry(window, show="*")
    password_entry.pack()

    def create_account():
        username = username_entry.get()
        password = password_entry.get()
        create_user(username, password)
        messagebox.showinfo("Success", "Account created!")
        login_screen(window)

    Button(window, text="Create Account", command=create_account).pack()
    Button(window, text="Back to Login", command=lambda: login_screen(window)).pack()

def main_display_screen(window, username):
    """Display the main menu screen."""
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text=f"Welcome, {username}!").pack()
    Button(window, text="Manage Profile", command=lambda: manage_profile_screen(window, username, lambda: main_display_screen(window, username))).pack()
    Button(window, text="Browse Users", command=lambda: browse_users_screen(window, lambda: main_display_screen(window, username))).pack()
    Button(window, text="Logout", command=lambda: login_screen(window)).pack()

def browse_users_screen(window, back_callback):
    """Display the user browsing screen."""
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text="Browse Users").pack()
    name_entry = Entry(window)
    name_entry.pack()
    building_entry = Entry(window)
    building_entry.pack()

    def search_user():
        name = name_entry.get()
        building = building_entry.get()
        user, error = search_user_by_name_or_building(name, building)
        if error:
            messagebox.showerror("Error", error)
        else:
            messagebox.showinfo("Found", f"User: {user['name']}, Building: {user.get('building', 'N/A')}")

    Button(window, text="Search", command=search_user).pack()
    Button(window, text="Back", command=back_callback).pack()
