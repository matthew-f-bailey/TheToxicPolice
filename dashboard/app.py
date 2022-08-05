import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table

from utils.md_utils import get_markdown_file
from aws.dynamo import query_comments_by_subreddit

app = Dash(__name__)

HEADER_MD = get_markdown_file('header')

comments = query_comments_by_subreddit('r/funny')
top_comments = comments.sort_values('score', ascending=False).head()
table = dash_table.DataTable(top_comments.to_dict('records'))



app.layout = html.Div(children=[
    dcc.Markdown(HEADER_MD),
    html.H1(children="Hello Dash"),
    html.Div(children="Dash: A web application framework"),
    table
])

if __name__=='__main__':
    app.run_server(debug=True)