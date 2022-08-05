import pandas as pd
import plotly.express as px
from dash import Dash, html
from dash.dcc import Markdown

from aws.dynamo import get_all_subs
from components.body import body
from utils.md_utils import get_markdown_file

# Load all subs available upon startup

app = Dash(__name__)

app.layout = html.Div([
    Markdown(get_markdown_file('header')),
    body(),
    Markdown(get_markdown_file('footer'))
])

if __name__=='__main__':
    app.run_server(debug=True)
