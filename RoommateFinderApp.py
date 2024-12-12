import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from UserManager import UserManager
from MessagingManager import MessagingManager
from FriendsManager import FriendsManager
from DataBaseManager import DataBaseManager


class RoommateFinderApp:
    def __init__(self):
        self.db_manager = DataBaseManager()
        self.user_manager = UserManager(self.db_manager)
        self.messaging_manager = MessagingManager(self.db_manager)
        self.friends_manager = FriendsManager(self.db_manager)
        self.logged_in_user = None
        self.profile_picture_path = None

        # Root setup
        self.root = tk.Tk()
        self.root.title("Roommate Finder")

        # Desired window size
        window_width = 1200
        window_height = 800

        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # Styling Configuration
        self.bg_color = "#2b2b2b"
        self.fg_color = "#f5f5f5"
        self.highlight_color = "#3c3c3c"
        self.button_color = "#4c4c4c"
        self.button_hover_color = "#6c6c6c"
        self.font_main = ("Arial", 14)
        self.font_bold = ("Arial", 14, "bold")
        self.font_small = ("Arial", 10)

        self.root.configure(bg=self.bg_color)

        # Scrollable Canvas Setup
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg=self.bg_color)
        self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Container Frame
        self.container_frame = tk.Frame(self.canvas, bg=self.bg_color)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.container_frame, anchor="n")
        self.container_frame.bind("<Configure>", self.update_scroll_region)
        self.root.bind("<Configure>", self.center_canvas)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        


        self.survey_questions = {
            "wake_up": ("What time do you usually wake up?", ["Early", "Late", "Flexible"]),
            "cleanliness": ("How clean do you prefer your living space?", ["Always tidy", "Manageable mess", "Comfortable with clutter"]),
            "noise": ("Do you prefer a quiet environment?", ["Always quiet", "Some noise is okay", "Lively and noisy"]),
            "diet": ("Do you have specific dietary habits or restrictions?", ["None", "Vegetarian/Vegan", "Other"]),
            "guests": ("How do you feel about guests?", ["Rarely", "Occasionally", "Frequently"]),
            "study": ("Where do you prefer to study?", ["Dorm/room", "Library", "Anywhere"]),
            "social": ("How often do you socialize?", ["Rarely", "A few times a week", "Almost every day"]),
            "hosting": ("Do you enjoy hosting group activities?", ["Yes", "Occasionally", "Not really"]),
            "conflict": ("How do you handle conflicts?", ["Directly resolve", "Need time before discussing", "Avoid confrontation"]),
            "introvert": ("Are you an introvert, extrovert, or ambivert?", ["Introvert", "Extrovert", "Ambivert"]),
            "pets": ("Do you prefer a pet-free environment?", ["Yes", "No", "Depends"]),
            "sharing": ("Are you comfortable sharing items?", ["Yes", "If discussed", "Prefer separate"]),
            "quirks": ("Do you have any habits roommates should know about?", ["Yes", "No"]),
            "qualities": ("What qualities are important in a roommate?", ["Friendliness", "Cleanliness", "Respect"]),
            "cooking": ("How often do you cook?", ["Rarely", "Occasionally", "Frequently"]),
            "sleep": ("What’s your usual sleeping environment?", ["Complete darkness", "Light/noise is fine", "Flexible"]),
            "tech": ("How do you use technology in your room?", ["Studying", "Gaming/entertainment", "Both"]),
            "temperature": ("Preferred room temperature?", ["Cooler", "Warmer", "Flexible"]),
            "cleaning": ("How do you feel about shared cleaning responsibilities?", ["Set schedule", "Flexible", "Not concerned"]),
            "meals": ("How often do you eat meals in the dorm?", ["Rarely", "Occasionally", "Frequently"]),
        }

        self.center_canvas(event=None)  # Call directly with no event
        self.show_login_screen()
        


    def center_canvas(self, event=None):
        """Center the canvas and dynamically adjust its size."""
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()

        # Update canvas dimensions
        self.canvas.configure(width=window_width, height=window_height)

        # Update the canvas window to match the root window dimensions
        self.canvas.itemconfig(self.canvas_window, width=window_width)

        # Ensure the scroll region encompasses all content
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def update_scroll_region(self, event=None):
        """Update the scrollable region to encompass all content."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Debugging: Print dimensions
        print("Updated scroll region:", self.canvas.bbox("all"))

    def on_mousewheel(self, event):
        """Scroll canvas content with mouse wheel."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def clear_screen(self):
        """Clear all widgets in the container frame."""
        for widget in self.container_frame.winfo_children():
            widget.destroy()
        self.canvas.yview_moveto(0)  # Reset scrollbar to the top

    
        # UI Components
    def create_label(self, text, font=None, fg=None, bg=None, **kwargs):
        """Create a styled label."""
        return tk.Label(self.container_frame, text=text, font=font or self.font_main, fg=fg or self.fg_color, bg=bg or self.bg_color, **kwargs)

    def create_button(self, text, command, font=None, **kwargs):
        """Create a styled button with hover effects."""
        button = tk.Button(self.container_frame, text=text, font=font or self.font_main, command=command,
                           bg=self.button_color, fg=self.fg_color, activebackground=self.button_hover_color,
                           activeforeground=self.fg_color, **kwargs)
        button.bind("<Enter>", lambda e: button.config(bg=self.button_hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=self.button_color))
        return button

        # Login Screen
    def show_login_screen(self):
        """Display login screen."""
        self.clear_screen()
        self.root.geometry("800x600")
        self.root.title("Login - Roommate Finder")

        self.create_label("Welcome to Roommate Finder", font=self.font_bold).pack(pady=20)
        self.create_label("Username:").pack(pady=5)
        self.username_entry = tk.Entry(self.container_frame, font=self.font_main)
        self.username_entry.pack(pady=5)
        self.create_label("Password:").pack(pady=5)
        self.password_entry = tk.Entry(self.container_frame, show="*", font=self.font_main)
        self.password_entry.pack(pady=5)
        self.create_button("Login", self.login_user).pack(pady=10)
        self.create_button("Register", self.show_registration_screen).pack(pady=5)

    def login_user(self):
        """Handle login functionality."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.user_manager.authenticate_user(username, password):
            self.logged_in_user = username
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid login credentials")

    def show_registration_screen(self):
        self.clear_screen()

        # Set default window size
        self.root.geometry("400x400")
        self.root.title("Register - Roommate Finder")

        # Add a title
        tk.Label(self.container_frame, text="Create an Account", font=("Arial", 16, "bold")).pack(pady=20)

        # Username label and entry
        tk.Label(self.container_frame, text="Username:", font=("Arial", 12)).pack(pady=5)
        self.reg_username = tk.Entry(self.container_frame, font=("Arial", 12), width=30)
        self.reg_username.pack(pady=5)

        # Email label and entry
        tk.Label(self.container_frame, text="Email:", font=("Arial", 12)).pack(pady=5)
        self.reg_email = tk.Entry(self.container_frame, font=("Arial", 12), width=30)
        self.reg_email.pack(pady=5)

        # Password label and entry
        tk.Label(self.container_frame, text="Password:", font=("Arial", 12)).pack(pady=5)
        self.reg_password = tk.Entry(self.container_frame, show="*", font=("Arial", 12), width=30)
        self.reg_password.pack(pady=5)

        # Next button to proceed to survey
        tk.Button(self.container_frame, text="Next", command=self.save_registration_details, font=("Arial", 12)).pack(pady=20)

    def save_registration_details(self):
        """Save the registration details and proceed to the survey."""
        self.temp_username = self.reg_username.get()
        self.temp_email = self.reg_email.get()
        self.temp_password = self.reg_password.get()

        if not self.temp_username or not self.temp_email or not self.temp_password:
            messagebox.showerror("Error", "All fields are required!")
            return

        self.show_registration_survey()

    def show_registration_survey(self):
        self.clear_screen()

        tk.Label(self.container_frame, text="Survey", font=("Arial", 16, "bold")).pack(pady=10)

        self.survey_answers = {}
        for key, (label, options) in self.survey_questions.items():
            tk.Label(self.container_frame, text=label, font=("Arial", 12), wraplength=600).pack(pady=5)
            var = tk.StringVar(value=options[0])
            for option in options:
                tk.Radiobutton(self.container_frame, text=option, variable=var, value=option, font=("Arial", 10)).pack(anchor="w", padx=20)
            self.survey_answers[key] = var

        tk.Button(self.container_frame, text="Complete Registration", command=self.register_user, font=("Arial", 12)).pack(pady=20)

    def register_user(self):
        """Register a new user with the provided details."""
        username = self.temp_username
        email = self.temp_email
        password = self.temp_password

        # Collect survey answers
        preferences = {key: var.get() for key, var in self.survey_answers.items()}

        # Call the user manager to register the user
        result = self.user_manager.register_user(username, email, password, preferences)
        if result:
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            self.show_login_screen()  # Redirect to login screen
        else:
            messagebox.showerror("Error", "Registration failed. Username or email may already exist.")
    
        # Main Menu
    def show_main_menu(self):
        """Display main menu."""
        self.clear_screen()
        self.create_label(f"Welcome, {self.logged_in_user}!", font=self.font_bold).pack(pady=20)
        self.create_button("View Profile", self.view_profile).pack(pady=10)
        self.create_button("Browse Users", self.browse_users).pack(pady=10)
        self.create_button("Messages", self.show_messages).pack(pady=10)
        self.create_button("Friends", self.show_friends_list).pack(pady=10)
        self.create_button("Logout", self.logout_user).pack(pady=10)

    def view_profile(self):
        """Display the logged-in user's profile."""
        self.clear_screen()

        # Fetch the user's profile
        profile = self.user_manager.get_user_profile(self.logged_in_user)
        if profile:
            # Title
            self.create_label("Your Profile", font=self.font_bold).pack(pady=10)

            # Profile Picture
            if profile.get('profile_picture'):
                try:
                    img = Image.open(profile['profile_picture'])
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)  # Resize for consistent appearance
                    photo = ImageTk.PhotoImage(img)
                    tk.Label(self.container_frame, image=photo, bg=self.bg_color).pack(pady=10)
                    self.root.image = photo  # Prevent garbage collection of the image
                except Exception as e:
                    print(f"Error loading profile picture for {self.logged_in_user}: {e}")

            # User's Name
            self.create_label(f"Name: {profile.get('name', 'N/A')}").pack(pady=5)

            # User's Bio
            self.create_label(f"Bio: {profile.get('bio', 'N/A')}").pack(pady=5)

            # User's Preferences
            self.create_label("Preferences:", font=self.font_bold).pack(pady=10)
            for key, value in profile.get('preferences', {}).items():
                label = self.survey_questions[key][0] if key in self.survey_questions else key
                self.create_label(f"{label}: {value}", font=self.font_small).pack(anchor="w", padx=20)

        else:
            self.create_label("Profile not found.", font=self.font_bold, fg="red").pack(pady=10)

        # Edit Profile Button
        self.create_button("Edit Profile", self.edit_profile).pack(pady=10)

        # Back Button
        self.create_button("Back", self.show_main_menu).pack(pady=10)

    def edit_profile(self):
        self.clear_screen()

        # Retrieve the user's profile
        profile = self.user_manager.get_user_profile(self.logged_in_user)

        if not profile:
            messagebox.showerror("Error", "Profile not found.")
            self.show_main_menu()
            return

        # Add a title
        tk.Label(self.container_frame, text="Edit Profile", font=("Arial", 16, "bold")).pack(pady=10)

        # Name field
        tk.Label(self.container_frame, text="Name:", font=("Arial", 12)).pack(pady=5)
        self.name_entry = tk.Entry(self.container_frame, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        # Insert name value, ensure it's a string
        name = str(profile.get('name', ''))
        self.name_entry.insert(0, name)

        # Bio field
        tk.Label(self.container_frame, text="Bio:", font=("Arial", 12)).pack(pady=5)
        self.bio_entry = tk.Entry(self.container_frame, font=("Arial", 12))
        self.bio_entry.pack(pady=5)

        # Insert bio value, ensure it's a string
        bio = str(profile.get('bio', ''))
        self.bio_entry.insert(0, bio)

        # Preferences fields
        tk.Label(self.container_frame, text="Preferences:", font=("Arial", 12, "bold")).pack(pady=10)
        self.pref_entries = {}
        for key, value in profile.get('preferences', {}).items():
            tk.Label(self.container_frame, text=key, font=("Arial", 10)).pack(anchor="w", padx=20)
            entry = tk.Entry(self.container_frame, font=("Arial", 10))
            entry.pack(anchor="w", padx=20)
            entry.insert(0, str(value))  # Ensure value is string
            self.pref_entries[key] = entry

        # Upload Picture Button
        tk.Button(self.container_frame, text="Upload Picture", command=self.upload_profile_picture, font=("Arial", 12)).pack(pady=10)

        # Save and Back Buttons
        tk.Button(self.container_frame, text="Save", command=self.save_profile, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.container_frame, text="Back", command=self.view_profile, font=("Arial", 12)).pack(pady=10)

    def upload_profile_picture(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if filepath:
            self.profile_picture_path = filepath
            messagebox.showinfo("Success", "Profile picture uploaded!")

    def save_profile(self):
        name = self.name_entry.get()
        bio = self.bio_entry.get()
        preferences = {key: entry.get() for key, entry in self.pref_entries.items()}
        profile_picture = getattr(self, 'profile_picture_path', None)

        if self.user_manager.update_user_profile(self.logged_in_user, name, bio, preferences, profile_picture):
            messagebox.showinfo("Success", "Profile updated!")
            self.view_profile()
        else:
            messagebox.showerror("Error", "Failed to update profile.")

    def browse_users(self):
        """Display a list of all users excluding the logged-in user with options to view their profile, send a message, or add them as a friend."""
        self.clear_screen()
        tk.Label(self.container_frame, text="Browse Users", font=("Arial", 16, "bold")).pack(pady=10)

        users = self.db_manager.fetch_all('SELECT username FROM users WHERE username != ?', (self.logged_in_user,))
        if users:
            for user in users:
                username = user[0]
                frame = tk.Frame(self.container_frame)
                frame.pack(pady=5)

                # Username Label
                tk.Label(frame, text=username, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

                # View Profile Button
                tk.Button(
                    frame,
                    text="View Profile",
                    command=lambda u=username: self.view_other_profile(u),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT)

                # Send Message Button
                tk.Button(
                    frame,
                    text="Send Message",
                    command=lambda u=username: self.send_message_to_user(u),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT)

                # Add Friend Button
                tk.Button(
                    frame,
                    text="Add Friend",
                    command=lambda u=username: self.send_friend_request(u),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT)
        else:
            tk.Label(self.container_frame, text="No users found.", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.container_frame, text="Back", command=self.show_main_menu, font=("Arial", 12)).pack(pady=10)

    def send_message_to_user(self, recipient_username):
        """Send a message to the selected user."""
        self.clear_screen()

        # Add a title
        tk.Label(self.container_frame, text=f"Send Message to {recipient_username}", font=("Arial", 16, "bold")).pack(pady=10)

        # Message input
        tk.Label(self.container_frame, text="Message:", font=("Arial", 12)).pack(pady=5)
        message_entry = tk.Text(self.container_frame, height=5, width=50, font=("Arial", 12))
        message_entry.pack(pady=10)

        # Send button
        def send_message_action():
            message_content = message_entry.get("1.0", tk.END).strip()  # Get the message content
            if message_content:
                if self.messaging_manager.send_message(self.logged_in_user, recipient_username, message_content):
                    messagebox.showinfo("Success", f"Message sent to {recipient_username}!")
                    self.browse_users()
                else:
                    messagebox.showerror("Error", "Failed to send message.")
            else:
                messagebox.showerror("Error", "Message cannot be empty.")

        tk.Button(self.container_frame, text="Send", command=send_message_action, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.container_frame, text="Back", command=self.browse_users, font=("Arial", 12)).pack(pady=10)

    def view_other_profile(self, username):
        """Display another user's profile."""
        self.clear_screen()

        # Fetch the user's profile
        profile = self.user_manager.get_user_profile(username)
        if profile:
            # Title
            self.create_label(f"Profile of {username}", font=self.font_bold).pack(pady=10)

            # Profile Picture
            if profile.get('profile_picture'):
                try:
                    img = Image.open(profile['profile_picture'])
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)  # Resize for consistent appearance
                    photo = ImageTk.PhotoImage(img)
                    tk.Label(self.container_frame, image=photo, bg=self.bg_color).pack(pady=10)
                    self.root.image = photo  # Prevent garbage collection of the image
                except Exception as e:
                    print(f"Error loading profile picture for {username}: {e}")

            # User's Name
            self.create_label(f"Name: {profile.get('name', 'N/A')}").pack(pady=5)

            # User's Bio
            self.create_label(f"Bio: {profile.get('bio', 'N/A')}").pack(pady=5)

            # User's Preferences
            self.create_label("Preferences:", font=self.font_bold).pack(pady=10)
            for key, value in profile.get('preferences', {}).items():
                label = self.survey_questions[key][0] if key in self.survey_questions else key
                self.create_label(f"{label}: {value}", font=self.font_small).pack(anchor="w", padx=20)

        else:
            self.create_label("Profile not found.", font=self.font_bold, fg="red").pack(pady=10)

        # Back Button
        self.create_button("Back", self.show_friends_list).pack(pady=10)

    def show_friends_list(self):
        """Display the user's friends, sent friend requests, and received friend requests."""
        self.clear_screen()
        tk.Label(self.container_frame, text="Friends List", font=("Arial", 16, "bold")).pack(pady=10)

        # Friends Section
        tk.Label(self.container_frame, text="Your Friends:", font=("Arial", 12, "bold")).pack(pady=5)
        friends = self.friends_manager.get_friends_list(self.logged_in_user)
        print(f"Friends for {self.logged_in_user}: {friends}")  # Debugging
        if friends:
            for friend in friends:
                frame = tk.Frame(self.container_frame)
                frame.pack(anchor="w", padx=20, pady=5)

                # Friend's Name
                tk.Label(frame, text=friend, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

                # View Profile Button
                tk.Button(
                    frame,
                    text="View Profile",
                    command=lambda f=friend: self.view_other_profile(f),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT, padx=5)

                # Remove Friend Button
                tk.Button(
                    frame,
                    text="Remove Friend",
                    command=lambda f=friend: self.remove_friend(f),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT, padx=5)
        else:
            tk.Label(self.container_frame, text="No friends yet.", font=("Arial", 10)).pack(anchor="w", padx=20)

        # Sent Friend Requests Section
        tk.Label(self.container_frame, text="Friend Requests Sent:", font=("Arial", 12, "bold")).pack(pady=5)
        sent_requests = self.friends_manager.get_sent_requests(self.logged_in_user)
        print(f"Sent requests for {self.logged_in_user}: {sent_requests}")  # Debugging
        if sent_requests:
            for request in sent_requests:
                frame = tk.Frame(self.container_frame)
                frame.pack(anchor="w", padx=20, pady=5)

                # Sent Request User
                tk.Label(frame, text=request, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

                # View Profile Button
                tk.Button(
                    frame,
                    text="View Profile",
                    command=lambda r=request: self.view_other_profile(r),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT, padx=5)

                # Cancel Request Button
                tk.Button(
                    frame,
                    text="Cancel Request",
                    command=lambda r=request: self.cancel_friend_request(r),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT)
        else:
            tk.Label(self.container_frame, text="No sent requests.", font=("Arial", 10)).pack(anchor="w", padx=20)

        # Received Friend Requests Section
        tk.Label(self.container_frame, text="Friend Requests Received:", font=("Arial", 12, "bold")).pack(pady=5)
        received_requests = self.friends_manager.get_received_requests(self.logged_in_user)
        print(f"Received requests for {self.logged_in_user}: {received_requests}")  # Debugging
        if received_requests:
            for request in received_requests:
                frame = tk.Frame(self.container_frame)
                frame.pack(anchor="w", padx=20, pady=5)

                # Received Request User
                tk.Label(frame, text=request, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

                # View Profile Button
                tk.Button(
                    frame,
                    text="View Profile",
                    command=lambda r=request: self.view_other_profile(r),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT, padx=5)

                # Accept Button
                tk.Button(
                    frame,
                    text="Accept",
                    command=lambda r=request: self.accept_friend_request(r),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT)

                # Decline Button
                tk.Button(
                    frame,
                    text="Decline",
                    command=lambda r=request: self.decline_friend_request(r),
                    font=("Arial", 10)
                ).pack(side=tk.LEFT)
        else:
            tk.Label(self.container_frame, text="No received requests.", font=("Arial", 10)).pack(anchor="w", padx=20)

        # Back Button
        tk.Button(self.container_frame, text="Back", command=self.show_main_menu, font=("Arial", 12)).pack(pady=10)

    def cancel_friend_request(self, receiver):
        query = "DELETE FROM friend_requests WHERE sender = ? AND receiver = ? AND LOWER(status) = 'pending'"
        print(f"Attempting to cancel friend request: {self.logged_in_user} -> {receiver}")  # Debugging
        if self.db_manager.execute_query(query, (self.logged_in_user, receiver)):
            print(f"Successfully canceled request: {self.logged_in_user} -> {receiver}")  # Debugging
            messagebox.showinfo("Success", f"Friend request to {receiver} has been canceled.")
            self.show_friends_list()  # Refresh the UI
        else:
            print(f"Failed to cancel request: {self.logged_in_user} -> {receiver}")  # Debugging
            messagebox.showerror("Error", f"Failed to cancel friend request to {receiver}.")

    def send_friend_request(self, recipient_username):
        """Handle the friend request sending process."""
        result = self.friends_manager.send_request(self.logged_in_user, recipient_username)
        if result == "Friend request sent.":
            messagebox.showinfo("Success", f"Friend request sent to {recipient_username}!")
            self.browse_users()  # Refresh the Browse Users page
        elif result == "Friend request already pending.":
            messagebox.showwarning("Info", f"A friend request is already pending with {recipient_username}.")
        elif result == "Already friends.":
            messagebox.showwarning("Info", f"You are already friends with {recipient_username}.")
        else:
            messagebox.showerror("Error", "Failed to send friend request. Please try again.")

    def accept_friend_request(self, sender):
        """Accept a received friend request."""
        if self.friends_manager.accept_request(self.logged_in_user, sender):
            messagebox.showinfo("Success", f"You are now friends with {sender}.")
            self.show_friends_list()  # Refresh the Friends List
        else:
            messagebox.showerror("Error", "Failed to accept friend request.")

    def decline_friend_request(self, sender):
        """Decline a received friend request."""
        if self.friends_manager.decline_request(self.logged_in_user, sender):
            messagebox.showinfo("Success", f"You declined the friend request from {sender}.")
        else:
            messagebox.showerror("Error", "Failed to decline friend request.")
        self.show_friends_list()  # Refresh the friends list

    def remove_friend(self, friend_username):
        """Remove a friend from the user's friends list."""
        if messagebox.askyesno("Confirm", f"Are you sure you want to remove {friend_username} as a friend?"):
            if self.friends_manager.remove_friend(self.logged_in_user, friend_username):
                messagebox.showinfo("Success", f"{friend_username} has been removed from your friends list.")
                self.show_friends_list()  # Refresh the friends list
            else:
                messagebox.showerror("Error", f"Failed to remove {friend_username} from your friends list.")

    def show_messages(self):
        """Show the list of users with whom messages have been exchanged."""
        self.clear_screen()
        tk.Label(self.container_frame, text="Messages", font=("Arial", 16, "bold")).pack(pady=10)

        # Fetch unique users from messaging history
        users = self.messaging_manager.get_conversation_users(self.logged_in_user)

        if users:
            for user in users:
                tk.Button(
                    self.container_frame,
                    text=f"Chat with {user}",
                    command=lambda u=user: self.view_conversation(u),
                    font=("Arial", 12)
                ).pack(pady=5)
        else:
            tk.Label(self.container_frame, text="No conversations yet.", font=("Arial", 12)).pack(pady=10)

        tk.Button(self.container_frame, text="Back", command=self.show_main_menu, font=("Arial", 12)).pack(pady=10)

    def view_conversation(self, recipient_username):
        """View messages exchanged with a specific user."""
        self.clear_screen()

        tk.Label(
            self.container_frame,
            text=f"Conversation with {recipient_username}",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        messages = self.messaging_manager.get_messages_with_user(self.logged_in_user, recipient_username)

        if messages:
            for sender, receiver, msg, timestamp in messages:
                message_frame = tk.Frame(self.container_frame)
                message_frame.pack(anchor="w", padx=20, pady=5)
                tk.Label(
                    message_frame,
                    text=f"From: {sender}",
                    font=("Arial", 10, "bold")
                ).pack(anchor="w")
                tk.Label(
                    message_frame,
                    text=msg,
                    font=("Arial", 10)
                ).pack(anchor="w")
                tk.Label(
                    message_frame,
                    text=f"Time: {timestamp}",
                    font=("Arial", 8)
                ).pack(anchor="w")
        else:
            tk.Label(self.container_frame, text="No messages in this conversation.", font=("Arial", 12)).pack(pady=10)

        # Input box for new message
        tk.Label(self.container_frame, text="New Message:", font=("Arial", 12)).pack(pady=5)
        message_entry = tk.Text(self.container_frame, height=3, width=50, font=("Arial", 12))
        message_entry.pack(pady=10)

        # Send button
        def send_message_action():
            message_content = message_entry.get("1.0", tk.END).strip()
            if message_content:
                if self.messaging_manager.send_message(self.logged_in_user, recipient_username, message_content):
                    messagebox.showinfo("Success", f"Message sent to {recipient_username}!")
                    self.view_conversation(recipient_username)
                else:
                    messagebox.showerror("Error", "Failed to send message.")
            else:
                messagebox.showerror("Error", "Message cannot be empty.")

        tk.Button(self.container_frame, text="Send", command=send_message_action, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.container_frame, text="Back", command=self.show_messages, font=("Arial", 12)).pack(pady=10)

    # def show_admin_menu(self):
    #     self.clear_screen()

    #     # Add a title for the admin menu
    #     tk.Label(self.container_frame, text="Admin Menu", font=self.font_bold).pack(pady=20)

    #     # Button to review flagged messages
    #     tk.Button(
    #         self.container_frame, 
    #         text="Review Flagged Messages", 
    #         command=self.show_flagged_messages_screen, 
    #         bg="blue", 
    #         fg="white"
    #     ).pack(pady=10)

    #     # Button to ban a user
    #     tk.Button(
    #         self.container_frame, 
    #         text="Ban User", 
    #         command=self.show_ban_user_screen, 
    #         bg="red", 
    #         fg="white"
    #     ).pack(pady=10)

    #     # Button to unban a user
    #     tk.Button(
    #         self.container_frame, 
    #         text="Unban User", 
    #         command=self.show_unban_user_screen, 
    #         bg="green", 
    #         fg="white"
    #     ).pack(pady=10)

    #     # Button to remove a message
    #     tk.Button(
    #         self.container_frame, 
    #         text="Remove Message", 
    #         command=self.show_remove_message_screen, 
    #         bg="orange", 
    #         fg="white"
    #     ).pack(pady=10)

    #     # Button to update app permissions
    #     tk.Button(
    #         self.container_frame, 
    #         text="Update Permissions", 
    #         command=self.show_update_permissions_screen, 
    #         bg="cyan", 
    #         fg="black"
    #     ).pack(pady=10)

    #     # Button to list admin responsibilities
    #     tk.Button(
    #         self.container_frame, 
    #         text="List Responsibilities", 
    #         command=lambda: self.logged_in_user.list_admin_responsibilities(), 
    #         bg="gray", 
    #         fg="white"
    #     ).pack(pady=10)

    #     # Back button to go to the login screen
    #     tk.Button(
    #         self.container_frame, 
    #         text="Back to Login Screen", 
    #         command=self.show_login_screen, 
    #         bg="white", 
    #         fg="black"
    #     ).pack(pady=10)

    def logout_user(self):
        self.logged_in_user = None
        self.show_login_screen()

    def update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def run(self):
        """Starts the Tkinter main event loop."""
        self.root.mainloop()
