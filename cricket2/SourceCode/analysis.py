import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess


class AnalysisPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Analysis Page")
        self.attributes('-fullscreen', True)  # Set fullscreen mode

        # Create a style for buttons
        self.style = ttk.Style()
        self.style.configure("Analyze.TButton", font=("Helvetica", 12, "bold"))
        self.style.map("Analyze.TButton", foreground=[("active", "white"), ("pressed", "white")])

        # Create a notebook to contain multiple pages
        self.notebook = ttk.Notebook(self)

        # Create five sections with titles, descriptions, images, and dropdown lists
        sections = [
            {"title": "Head to Head", "description": "Head-to-head analysis of IPL teams involves examining the historical performances and outcomes of matches between two specific teams in the Indian Premier League", "image_path": r"C:\Users\Nandan\Downloads\e073f785-568b-4c07-8201-94a7ac206c7a.jpg"},
            {"title": "Lucky Venue", "description": "Analyzing the best venue for a particular team in the Indian Premier League involves studying the team's historical performances at different stadiums and identifying where they have had the most success", "image_path": r"C:\Users\Nandan\Downloads\2c5d4d2e-ab0d-4ceb-b771-ad6b17a0a672.jpg"},
            {"title": "Impact of toss", "description": "The toss in IPL matches holds significant importance due to its potential impact on the outcome of the game", "image_path": r"C:\Users\Nandan\Downloads\vector-cricket-stadium.jpg"},
            {"title": "Top Batsmen", "description": "Analyzing the top run-scorer in the Indian Premier League involves examining various factors related to the player's performance, consistency, and impact on their team's success", "image_path": r"C:\Users\Nandan\Downloads\vector-cricket-player-in-playing-action.jpg"},
            {"title": "Top Bowlers", "description": "Analyzing the top wicket-takers in the Indian Premier League involves examining various aspects of their bowling performance, consistency, and impact on their team's success.", "image_path": r"C:\Users\Nandan\Downloads\e073f785-568b-4c07-8201-94a7ac206c7a.jpg"},
        ]

        for section in sections:
            frame = ttk.Frame(self.notebook)
            self.create_section(frame, section)
            self.notebook.add(frame, text=section["title"])

        self.notebook.pack(expand=1, fill="both")

        # Add an exit button
        exit_button = tk.Button(self, text="Exit", command=self.quit, font=("Helvetica", 12, "bold"), bg="red", fg="white")
        exit_button.place(relx=0.95, rely=0.05, anchor="center")

    def create_section(self, frame, section):
        # Add title label
        title_label = ttk.Label(frame, text=section["title"], font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(10, 0))

        # Add description label
        description_label = ttk.Label(frame, text=section["description"], wraplength=500, padding=(10, 10))
        description_label.pack()

        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Add Canvas for the background image
        canvas = tk.Canvas(frame, width=screen_width, height=screen_height)
        canvas.pack(fill=tk.BOTH, expand=True)  # Fill the entire frame

        # Add image as background
        if "image_path" in section:
            image = Image.open(section["image_path"])
            # Resize the image to fit the screen
            image = image.resize((screen_width, screen_height), Image.LANCZOS)
            section["photo_image"] = ImageTk.PhotoImage(image)
            canvas.create_image(0, 0, anchor=tk.NW, image=section["photo_image"])

        # Create a frame for buttons
        button_frame = ttk.Frame(canvas)
        button_frame.pack(pady=10)

        # Add Analyze button
        analyze_button = ttk.Button(button_frame, text="Analyze", command=lambda: self.show_specific_page(section["title"]), style="Analyze.TButton")
        analyze_button.pack(side=tk.LEFT, padx=20)

        # Add back button
        back_button = ttk.Button(button_frame, text="Back to Login", command=self.go_to_login, style="Analyze.TButton")
        back_button.pack(side=tk.LEFT)

    def show_specific_page(self, section_title):
        if section_title == "Head to Head":
            # Launch HeadToHead.py as a separate process
            subprocess.Popen(["python", "HeadToHead.py"])
        elif section_title == "Impact of toss":
            subprocess.Popen(["Python", "ImpactOfToss.py"])
        elif section_title == "Lucky Venue":
            subprocess.Popen(["Python", "LuckyVenues.py"])
        elif section_title == "Top Batsmen":
            subprocess.Popen(["Python", "TopBatsmen.py"])
        elif section_title == "Top Bowlers":
            subprocess.Popen(["Python", "TopBowler.py"])
        else:
            print(f"Button clicked for {section_title}")

    def go_to_login(self):
        # Open login.py file as a separate process
        subprocess.Popen(["python", "login.py"])

if __name__ == "__main__":
    app = AnalysisPage()
    app.mainloop()

