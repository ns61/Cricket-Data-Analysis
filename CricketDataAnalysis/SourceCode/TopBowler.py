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

deliveries_data['dismissal_kind'].unique()
dismissal_kinds = ['caught', 'bowled', 'lbw', 'caught and bowled',
       'stumped', 'hit wicket']
hwt=deliveries_data[deliveries_data["dismissal_kind"].isin(dismissal_kinds)]
bo=hwt['bowler'].value_counts()
colors = ['turquoise',] * 13
colors[0] = 'crimson'
fig=px.bar(x=bo[:10].index,y=bo[:10],labels=dict(x="Bowler",y="Total Wickets"),)
fig.update_layout(title="Leading wicket-takers",
                  titlefont={'size': 26},template='simple_white'     
                  )
fig.update_traces(marker_line_color='black',
                  marker_line_width=2.5, opacity=1,marker_color=colors)
fig.show()