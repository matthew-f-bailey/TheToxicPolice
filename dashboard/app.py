import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, html
from dash.dcc import Markdown

from dash.html import Iframe

from aws.dynamo import get_all_subs
from components.body import body
from utils.md_utils import get_markdown_file

# Load all subs available upon startup

THEME = dbc.themes.UNITED

app = Dash(
    __name__,
    external_stylesheets=[THEME],
    suppress_callback_exceptions=True
)

app.layout = html.Div(className='container-fluid', children=[
    Markdown(get_markdown_file('header')),
    body(),
    Markdown(get_markdown_file('footer'))
])

if __name__=='__main__':
    app.run_server(debug=True)
