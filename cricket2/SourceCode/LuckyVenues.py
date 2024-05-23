import pandas as pd
import plotly.express as px
import tkinter as tk
from tkinter import ttk
import pandas as pd
from pymongo import MongoClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import plotly.express as px
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, plot, iplot
from plotly import tools
from warnings import filterwarnings
import pandas as pd
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk
filterwarnings('ignore')    

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

def lucky(match_data, team_name):
    return match_data[match_data['winner'] == team_name]['venue'].value_counts().nlargest(10)

class LuckyVenueApp(tk.Tk):
    def __init__(self, sections):
        super().__init__()

        self.title("Lucky Venue Analysis")

        # Create a frame for the analysis
        analysis_frame = ttk.Frame(self)
        self.create_analysis_frame(analysis_frame, sections)
        analysis_frame.pack()

    def create_analysis_frame(self, frame, sections):
        # Add title label
        title_label = ttk.Label(frame, text="Lucky Venue Analysis", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(10, 20))

        # Add dropdown list for team selection
        team_label = ttk.Label(frame, text="Select Team:")
        team_label.pack()

        self.team_combobox = ttk.Combobox(frame, values=sections[0]["teams"])
        self.team_combobox.pack()

        # Add button to initiate analysis
        analyze_button = ttk.Button(frame, text="Analyze Lucky Venues", command=self.analyze_venues)
        analyze_button.pack()

    def analyze_venues(self):
        # Get selected team from dropdown list
        team_name = self.team_combobox.get()

        # Check if a team is selected
        if not team_name:
            tk.messagebox.showinfo("Error", "Please select a team.")
            return

        # Perform analysis
        lucky_venues = lucky(match_data, team_name)

        # Plot the analysis using Plotly
        values = lucky_venues
        labels = lucky_venues.index
        colors = ['turquoise', 'crimson']
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                          marker=dict(colors=colors, line=dict(color='#000000', width=3)))
        fig.update_layout(title=f"Wins at different Venues for {team_name}:",
                          titlefont={'size': 30})
        fig.show()

# Example usage
if __name__ == "__main__":
    # Pass the sections with team names to the LuckyVenueApp
    sections = [
        {"title": "Head to Head", "description": "Head to Head", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": ["Royal Challengers Bangalore", "Kings XI Punjab", "Delhi Daredevils", "Mumbai Indians", "Kolkata Knight Riders", "Rajasthan Royals", "Deccan Chargers", "Chennai Super Kings", "Kochi Tuskers Kerala", "Pune Warriors", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants", "Delhi Capitals"]},
        {"title": "Lucky Venue", "description": "Lucky Venue", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": ["Royal Challengers Bangalore", "Kings XI Punjab", "Delhi Daredevils", "Mumbai Indians", "Kolkata Knight Riders", "Rajasthan Royals", "Deccan Chargers", "Chennai Super Kings", "Kochi Tuskers Kerala", "Pune Warriors", "Sunrisers Hyderabad", "Gujarat Lions", "Rising Pune Supergiants", "Delhi Capitals"]},
        {"title": "Impact of toss", "description": "Impact of Toss", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": []},
        {"title": "Top Batsmens", "description": "Top runs scorer", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": []},
        {"title": "Top Bowlers", "description": "Top Wicket Takers", "image_path": r"C:\Users\Nandan\Downloads\IPL.gif", "teams": []},
    ]

    app = LuckyVenueApp(sections)
    app.mainloop()
