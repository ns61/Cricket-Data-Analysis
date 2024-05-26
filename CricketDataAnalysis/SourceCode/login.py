import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pymongo import MongoClient
import subprocess

# MongoDB connection
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['cricket']
mongo_collection = mongo_db['users']

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['cricket']
        self.users_collection = self.db['users']
        self.admin_collection = self.db['admin']

    def close_connection(self):
        self.client.close()

    def authenticate_user(self, user_id, password):
        return self.users_collection.find_one({"User ID": user_id, "Password": password})

    def authenticate_admin(self, admin_id, password):
        return self.admin_collection.find_one({"admin_id": admin_id, "password": password})

class LoginWindow:
    def __init__(self, root, user_type):
        self.root = root
        self.user_type = user_type
        self.init_ui()

    def init_ui(self):
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Cricket Data Analysis - Login")

        window_width = 300
        window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.login_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.create_widgets()

    def create_widgets(self):
        username_label = tk.Label(self.login_window, text="User ID:")
        username_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(self.login_window, textvariable=self.username_var)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        self.username_entry.config(validate="key", validatecommand=(self.root.register(self.validate_entry), "%P"))

        password_label = tk.Label(self.login_window, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.login_window, show="*", textvariable=self.password_var)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        self.show_password = tk.BooleanVar()
        self.show_password.set(False)
        show_hide_button = tk.Checkbutton(self.login_window, text="Show Password", variable=self.show_password, command=self.toggle_password)
        show_hide_button.grid(row=2, columnspan=2)

        login_button = tk.Button(self.login_window, text="Login", command=self.perform_login,
                                 width=15, height=2, relief=tk.RAISED, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
        login_button.grid(row=3, columnspan=2, pady=10)

    def validate_entry(self, value):
        return value.isdigit()

    def toggle_password(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def perform_login(self):
        user_id = self.username_var.get()
        password = self.password_var.get()

        if not user_id.isdigit():
            messagebox.showerror("Invalid User ID", "User ID must contain only numeric characters.")
            return

        if self.user_type == "user":
            user_data = db.authenticate_user(user_id, password)
            self.handle_login_result(user_data, "User", user_id)
        elif self.user_type == "admin":
            admin_data = db.authenticate_admin(user_id, password)
            self.handle_login_result(admin_data, "Admin", "Admin")

    def handle_login_result(self, data, role, user_id):
        if data:
            messagebox.showinfo("Login Successful", f"Welcome, {user_id} ({role})!")
            launch_next_file("analysis.py") if role == "User" else launch_next_file("crud.py")
            self.login_window.destroy()
        else:
            messagebox.showerror("Login Failed", f"Invalid {role} ID or password for {user_id}")

def launch_next_file(filename):
    try:
        subprocess.run(["python", filename], check=True)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to launch the next file: {e}")

def open_user_login():
    LoginWindow(root, "user")

def open_admin_login():
    LoginWindow(root, "admin")

def exit_program():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()

if __name__ == "__main__":
    db = Database()

    root = tk.Tk()
    root.title("Cricket Data Analysis")

    try:
        image_path = r"C:\Users\Nandan\Downloads\login.jpg"  # Replace with your image file path
        background_image = Image.open(image_path)
        background_photo = ImageTk.PhotoImage(background_image)
    except FileNotFoundError:
        messagebox.showerror("Image Error", f"Image file not found at: {image_path}")
        root.destroy()
    else:
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        root.geometry(f"{screen_width}x{screen_height}+0+0")
        root.attributes("-fullscreen", True)

        background_label = tk.Label(root, image=background_photo)
        background_label.place(relwidth=1, relheight=1)

        button_width = 15
        button_height = 2
        button_relx = 0.5
        user_button = tk.Button(root, text="User", command=open_user_login,
                                width=button_width, height=button_height, relief=tk.RAISED, bg="white", fg="#3366CC",
                                font=("Helvetica", 12, "bold"), bd=3, highlightthickness=0)
        admin_button = tk.Button(root, text="Admin", command=open_admin_login,
                                 width=button_width, height=button_height, relief=tk.RAISED, bg="white", fg="#FF6347",
                                 font=("Helvetica", 12, "bold"), bd=3, highlightthickness=0)

        exit_button = tk.Button(root, text="Exit", command=exit_program, relief=tk.RAISED, bg="white", fg="black",
                                font=("Helvetica", 12, "bold"), bd=3, highlightthickness=0)
        exit_button.place(relx=0.98, rely=0.02, anchor="ne")

        user_button.place(relx=button_relx, rely=0.58, anchor="center")
        admin_button.place(relx=button_relx, rely=0.68, anchor="center")

        root.mainloop()

    db.close_connection()
