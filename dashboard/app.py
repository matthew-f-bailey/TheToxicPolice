import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html
from dash.dcc import Markdown

from dash.html import H1

from aws.dynamo import get_all_subs
from components.body import body
from utils.md_utils import get_markdown_file
from settings import COLORS
import flask

# Load all subs available upon startup

THEME = dbc.themes.CYBORG

server = flask.Flask(__name__)

app = Dash(
    __name__,
    external_stylesheets=[THEME, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    server=server
)

app.layout = html.Div(className='container-fluid', children=[
    H1('Reddit Toxicity Dashboard (WIP)'),
    body()
])

if __name__=='__main__':
    app.run_server(debug=True)
