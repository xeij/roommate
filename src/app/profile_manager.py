
from tkinter import filedialog, messagebox
from app.user_data import update_profile_image

def manage_profile_screen(window, username, back_callback):
    """Display the manage profile screen."""
    for widget in window.winfo_children():
        widget.destroy()

    import tkinter as tk
    tk.Label(window, text="Manage Profile").pack()

    def upload_profile_image():
        file_path = filedialog.askopenfilename(
            title="Select Profile Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )
        if file_path:
            update_profile_image(username, file_path)
            messagebox.showinfo("Success", "Profile image uploaded successfully!")

    tk.Button(window, text="Upload Profile Image", command=upload_profile_image).pack()
    tk.Button(window, text="Back", command=back_callback).pack()
