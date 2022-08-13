from dash.html import Div
import dash_bootstrap_components as dbc

def no_content_error_message():
    return Div(children=[
        dbc.Alert("No data to display for subreddit within the past 24", color="warning")
    ])