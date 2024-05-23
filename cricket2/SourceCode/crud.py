import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from PIL import Image, ImageTk
import os

class AdminPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Page")
        self.root.attributes("-fullscreen", True)  # Open in full screen

        # MongoDB connection
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['cricket']
        self.collection = self.db['users']

        # Background Image
        image_path = r"C:\Users\Nandan\Downloads\crud.jpg"
        if not os.path.isfile(image_path):
            messagebox.showerror("Image Error", f"Image file not found at: {image_path}")
        else:
            self.img = Image.open(image_path)
            self.img = ImageTk.PhotoImage(self.img)

            background_label = tk.Label(self.root, image=self.img)
            background_label.place(relwidth=1, relheight=1)

        # Admin Page Heading
        self.label = tk.Label(self.root, text="Admin Page", font=("Helvetica", 28, "bold"))
        self.label.place(relx=0.5, rely=0, anchor=tk.N)

        # Buttons for different modules
        create_users_button = tk.Button(self.root, text="Create Users", command=self.create_users)
        create_users_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        view_users_button = tk.Button(self.root, text="View/Update Users", command=self.view_users)
        view_users_button.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        delete_users_button = tk.Button(self.root, text="Delete Users", command=self.delete_users)
        delete_users_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Back button
        back_button = tk.Button(self.root, text="Back", command=self.root.quit, height=2, width=10,bg="#FF6347", fg="black")
        back_button.place(relx=0.95, rely=0.05, anchor=tk.NE)

        # User database (in-memory representation)
        self.users = []

    # The rest of your methods remain unchanged...


    def add_user_to_mongodb(self, user_id, password, name, phone, age, create_window):
        if not user_id or not password or not name or not phone or not age:
            messagebox.showerror("Incomplete Information", "All fields are mandatory to create a user.")
            return

        if not user_id.isdigit():
            messagebox.showerror("Invalid User ID", "User ID must contain only numeric characters.")
            return
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror("Invalid Phone Number", "Phone number must contain exactly 10 numeric characters.")
            return
        if not age.isdigit():
            messagebox.showerror("Invalid Age", "Age must contain only numeric characters.")
            return

        user_info = {
            "User ID": user_id,
            "Password": password,
            "Name": name,
            "Phone Number": phone,
            "Age": age
        }

        try:
            # Insert user information into MongoDB
            result = self.collection.insert_one(user_info)

            if result.inserted_id:
                messagebox.showinfo("User Created", "User successfully created and added to MongoDB!")
                create_window.destroy()  # Close the create user window
            else:
                messagebox.showerror("Error", "Failed to add user to MongoDB.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def create_users(self):
        create_window = tk.Toplevel(self.root)
        create_window.title("Create User")

        # Create entry widgets for user input
        user_id_label = tk.Label(create_window, text="User ID:")
        user_id_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        user_id_entry = tk.Entry(create_window)
        user_id_entry.grid(row=0, column=1, padx=10, pady=5)
        user_id_entry.config(validate="key", validatecommand=(self.root.register(self.validate_entry), "%P"))

        password_label = tk.Label(create_window, text="Password:")
        password_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        password_entry = tk.Entry(create_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)

        # Show/Hide password functionality
        show_hide_button = tk.Button(create_window, text="Show", command=lambda: self.toggle_show_hide(password_entry))
        show_hide_button.grid(row=1, column=2, padx=5, pady=5)

        name_label = tk.Label(create_window, text="Name:")
        name_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        name_entry = tk.Entry(create_window)
        name_entry.grid(row=2, column=1, padx=10, pady=5)

        phone_label = tk.Label(create_window, text="Phone Number:")
        phone_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        phone_entry = tk.Entry(create_window)
        phone_entry.grid(row=3, column=1, padx=10, pady=5)
        phone_entry.config(validate="key", validatecommand=(self.root.register(self.validate_phone), "%P"))

        age_label = tk.Label(create_window, text="Age:")
        age_label.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)
        age_entry = tk.Entry(create_window)
        age_entry.grid(row=4, column=1, padx=10, pady=5)
        age_entry.config(validate="key", validatecommand=(self.root.register(self.validate_entry), "%P"))

        submit_button = tk.Button(create_window, text="Submit", command=lambda: self.add_user_to_mongodb(
            user_id_entry.get(), password_entry.get(), name_entry.get(), phone_entry.get(), age_entry.get(), create_window))
        submit_button.grid(row=5, column=1, pady=10)

    def toggle_show_hide(self, entry_widget):
        current_value = entry_widget.cget("show")
        if current_value == "":
            entry_widget.config(show="*")
            entry_widget.focus()
        else:
            entry_widget.config(show="")
            entry_widget.focus()

    def view_users(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View/Update Users")

        # Fetch all users from MongoDB
        users_from_mongo = self.collection.find()

        for i, user in enumerate(users_from_mongo):
            user_info_label = tk.Label(view_window, text=f"User {i + 1}:")
            user_info_label.grid(row=i * 2, column=0, padx=10, pady=5)

            # Display user information
            user_id_label = tk.Label(view_window, text=f"User ID: {user['User ID']}")
            user_id_label.grid(row=i * 2 + 1, column=0, padx=10, pady=5)

            password_label = tk.Label(view_window, text=f"Password: {user['Password']}")
            password_label.grid(row=i * 2 + 1, column=1, padx=10, pady=5)

            name_label = tk.Label(view_window, text=f"Name: {user['Name']}")
            name_label.grid(row=i * 2 + 1, column=2, padx=10, pady=5)

            phone_label = tk.Label(view_window, text=f"Phone Number: {user['Phone Number']}")
            phone_label.grid(row=i * 2 + 1, column=3, padx=10, pady=5)

            age_label = tk.Label(view_window, text=f"Age: {user['Age']}")
            age_label.grid(row=i * 2 + 1, column=4, padx=10, pady=5)

            # Add an "Update" button for each user
            update_button = tk.Button(view_window, text="Update", command=lambda u=user: self.open_update_window(u))
            update_button.grid(row=i * 2 + 1, column=5, padx=10, pady=5)

            # Separator below each user
            separator = tk.Label(view_window, text="------------------------")
            separator.grid(row=i * 2 + 2, column=0, columnspan=6, padx=10, pady=5)

        if users_from_mongo.count() == 0:
            messagebox.showinfo("No Users", "No users found in MongoDB.")

    def open_update_window(self, user):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update User Info")

        # Center the update window on the screen
        window_width = 300
        window_height = 200
        screen_width = update_window.winfo_screenwidth()
        screen_height = update_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        update_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Bring the update window to the front
        update_window.lift(self.root)
        update_window.attributes('-topmost', True)
        update_window.attributes('-topmost', False)  # Allow other windows to be on top

        # Populate the entry fields with the current user information
        password_label = tk.Label(update_window, text="Password:")
        password_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        password_entry = tk.Entry(update_window, show="*")
        password_entry.insert(0, user["Password"])
        password_entry.grid(row=0, column=1, padx=10, pady=5)

        # Show/Hide password functionality
        show_hide_button = tk.Button(update_window, text="Show", command=lambda: self.toggle_show_hide(password_entry))
        show_hide_button.grid(row=0, column=2, padx=5, pady=5)

        name_label = tk.Label(update_window, text="Name:")
        name_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        name_entry = tk.Entry(update_window)
        name_entry.insert(0, user["Name"])
        name_entry.grid(row=1, column=1, padx=10, pady=5)

        phone_label = tk.Label(update_window, text="Phone Number:")
        phone_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        phone_entry = tk.Entry(update_window)
        phone_entry.insert(0, user["Phone Number"])
        phone_entry.grid(row=2, column=1, padx=10, pady=5)
        phone_entry.config(validate="key", validatecommand=(self.root.register(self.validate_phone), "%P"))

        age_label = tk.Label(update_window, text="Age:")
        age_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        age_entry = tk.Entry(update_window)
        age_entry.insert(0, user["Age"])
        age_entry.grid(row=3, column=1, padx=10, pady=5)
        age_entry.config(validate="key", validatecommand=(self.root.register(self.validate_entry), "%P"))

        update_button = tk.Button(update_window, text="Update",
                                  command=lambda: self.update_user_info(user, password_entry.get(), name_entry.get(),
                                                                        phone_entry.get(), age_entry.get(), update_window))
        update_button.grid(row=4, column=1, pady=10)

    def update_user_info(self, user, password, name, phone, age, update_window):
        user["Password"] = password
        user["Name"] = name
        user["Phone Number"] = phone
        user["Age"] = age
        messagebox.showinfo("Update Successful", "User information updated successfully!")

        # Update the user information in MongoDB
        self.collection.update_one({"User ID": user["User ID"]},
                                   {"$set": {"Password": password, "Name": name, "Phone Number": phone, "Age": age}})

        update_window.destroy()  # Close the update user window

    def delete_users(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Users")

        # Fetch all users from MongoDB
        users_from_mongo = self.collection.find()

        for i, user in enumerate(users_from_mongo):
            user_info_label = tk.Label(delete_window, text=f"User {i + 1}:")
            user_info_label.grid(row=i * 2, column=0, padx=10, pady=5)

            # Display user information
            user_id_label = tk.Label(delete_window, text=f"User ID: {user['User ID']}")
            user_id_label.grid(row=i * 2 + 1, column=0, padx=10, pady=5)

            name_label = tk.Label(delete_window, text=f"Name: {user['Name']}")
            name_label.grid(row=i * 2 + 1, column=1, padx=10, pady=5)

            # Add a "Delete" button for each user
            delete_button = tk.Button(delete_window, text="Delete", command=lambda u=user: self.delete_user(u, delete_window))
            delete_button.grid(row=i * 2 + 1, column=2, padx=10, pady=5)

            # Separator below each user
            separator = tk.Label(delete_window, text="------------------------")
            separator.grid(row=i * 2 + 2, column=0, columnspan=3, padx=10, pady=5)

        if users_from_mongo.count() == 0:
            messagebox.showinfo("No Users", "No users found in MongoDB.")

    def delete_user(self, user, delete_window):
        self.collection.delete_one({"User ID": user["User ID"]})
        messagebox.showinfo("Delete Successful", "User deleted successfully!")
        delete_window.destroy()  # Close the delete user window

    def validate_entry(self, value):
        return value.isdigit()

    def validate_phone(self, value):
        return value.isdigit() and len(value) <= 10

if __name__ == "__main__":
    root = tk.Tk()
    admin_page = AdminPage(root)
    root.mainloop()
