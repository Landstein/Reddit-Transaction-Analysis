import numpy as np
import pandas as pd
import praw
import re
import plotly.graph_objects as go

reddit = praw.Reddit(client_id = "",
                    client_secret = "",
                    user_agent="",
                    username = "",
                    password = "")

state_list = []
for comment in reddit.subreddit('hardwareswap').hot(limit=None):
    x = re.search(r'(?<=\-)(.*?)(?=\])', comment.title)
    if x != None:
        state_list.append(x.group()[:2])

states = pd.DataFrame(state_list, columns=['state'])
dff = states['state'].value_counts().rename_axis('state').to_frame('counts')
fig = go.Figure(data=go.Choropleth(
    locations=dff.index, # Spatial coordinates
    z = dff['counts'], # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = 'Rainbow',
    colorbar_title = "Amount of Posts per state",
    zmin = 0,
    zmax = 100,
))

fig.update_layout(
    title_text = 'Last 1000 submissions heatmap',
    geo_scope='usa', # limite map scope to USA
)

fig.show()