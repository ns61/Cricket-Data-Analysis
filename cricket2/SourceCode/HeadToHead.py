import pandas as pd
import plotly.express as px
import tkinter as tk
from tkinter import ttk
import pandas as pd
from pymongo import MongoClient

# MongoDB connection parameters
mongodb_host = 'mongodb://localhost:27017/'  # Change this to your MongoDB host
mongodb_port = 27017  # Change this to your MongoDB port
database_name = 'cricket'

# Connect to MongoDB
client = MongoClient(mongodb_host, mongodb_port)
db = client[database_name]

# Read data from MongoDB collections
deliveries_data_cursor = db.All_scores.find()
match_data_cursor = db.All_matches.find()

# Convert MongoDB cursors to pandas DataFrames
deliveries_data = pd.DataFrame(list(deliveries_data_cursor))
match_data = pd.DataFrame(list(match_data_cursor))

# Define colors
colors = ['red', 'blue', 'green', 'orange', 'purple']  # You can customize the list of colors as needed

class TeamComparisonApp(tk.Tk):
    def __init__(self, sections):
        super().__init__()

        self.title("Team Comparison App")

        # Create a notebook to contain multiple pages
        self.notebook = ttk.Notebook(self)

        # Create a frame for team selection
        team_frame = ttk.Frame(self.notebook)
        self.create_team_selection_frame(team_frame, sections)
        self.notebook.add(team_frame, text="Team Selection")

        self.notebook.pack(expand=1, fill="both")

    def create_team_selection_frame(self, frame, sections):
        # Add title label
        title_label = ttk.Label(frame, text="Select Teams for Comparison", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(10, 20))

        # Add dropdown lists for team selection
        team1_label = ttk.Label(frame, text="Team 1:")
        team1_label.pack()

        self.team1_combobox = ttk.Combobox(frame, values=sections[0]["teams"])
        self.team1_combobox.pack()

        team2_label = ttk.Label(frame, text="Team 2:")
        team2_label.pack()

        self.team2_combobox = ttk.Combobox(frame, values=sections[0]["teams"])
        self.team2_combobox.pack()

        # Add button to initiate comparison
        compare_button = ttk.Button(frame, text="Compare Teams", command=self.compare_teams)
        compare_button.pack()

    def compare_teams(self):
        # Get selected teams from dropdown lists
        team1 = self.team1_combobox.get()
        team2 = self.team2_combobox.get()

        # Check if both teams are selected
        if not team1 or not team2:
            tk.messagebox.showinfo("Error", "Please select both Team 1 and Team 2.")
            return

        self.show_comparison(team1, team2)

    def show_comparison(self, team1, team2):
        compare = match_data[((match_data['team1'] == team1) | (match_data['team2'] == team1)) & ((match_data['team1'] == team2) | (match_data['team2'] == team2))]

        # Print columns for debugging
        print(compare.columns)

        # Check if 'date' is in the columns
        if 'date' not in compare.columns:
            raise ValueError("The 'date' column is not present in the DataFrame.")

        fig = px.histogram(data_frame=compare, x='date', color='winner', labels=dict(x="date", y="Count"), barmode='group', nbins=16, color_discrete_sequence=colors)

        fig.update_layout(title=f"Team Comparison: {team1} vs {team2}", titlefont={'size': 26}, template='simple_white')

        fig.update_traces(marker_line_color='black', marker_line_width=2.5, opacity=1)

        fig.show(full_screen=True)

# Example usage
if __name__ == "__main__":
    # Pass the sections with team names to the TeamComparisonApp
    sections = [
        {"title": "Head to Head", "description": "Head to Head", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": ["Royal Challengers Bangalore", "Kings XI Punjab", "Delhi Daredevils", "Mumbai Indians", "Kolkata Knight Riders", "Rajasthan Royals", "Deccan Chargers", "Chennai Super Kings", "Kochi Tuskers Kerala", "Pune Warriors", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants", "Delhi Capitals"]},
        {"title": "Lucky Venue", "description": "Lucky Venue", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": ["Royal Challengers Bangalore", "Kings XI Punjab", "Delhi Daredevils", "Mumbai Indians", "Kolkata Knight Riders", "Rajasthan Royals", "Deccan Chargers", "Chennai Super Kings", "Kochi Tuskers Kerala", "Pune Warriors", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants", "Delhi Capitals"]},
        {"title": "Impact of toss", "description": "Impact of Toss", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": []},
        {"title": "Top Batsmens", "description": "Top runs scorer", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": []},
        {"title": "Top Bowlers", "description": "Top Wicket Takers", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": []},
    ]

    app = TeamComparisonApp(sections)
    app.mainloop()