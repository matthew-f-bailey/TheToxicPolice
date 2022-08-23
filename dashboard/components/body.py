from dash import Input, Output, callback
from dash.html import A, Div
from dash.dcc import Tabs, Tab
import dash_bootstrap_components as dbc

from components.overview import overview
from components.subreddit import subreddit

from settings import COLORS

OVERVIEW = "Overview"
SUBREDDIT = "Subreddit"
COMPONENT_MAPPING = {
    OVERVIEW: overview(),
    SUBREDDIT: subreddit()
}

def body():
    """
    Responsible for updating the page to correct components and
    giving options to do so
    """
    return \
        Div(style={'backgroundColor': COLORS.BG_GREY}, children=[
            dbc.Row(
                dbc.Navbar(dark=True, color=COLORS.WHITE, children=[
                    dbc.Tabs(id='tab_switch', active_tab=SUBREDDIT, style={'backgroundColor': COLORS.BLUE}, children=[
                        dbc.Tab(label=OVERVIEW, tab_id=OVERVIEW, active_label_style={"color": COLORS.RED}),
                        dbc.Tab(label=SUBREDDIT, tab_id=SUBREDDIT, active_label_style={"color": COLORS.RED})
                    ])
                ])
            ),
            dbc.Row(
                dbc.CardBody(Div(id='content', children=[])),
            )
        ])

@callback(
    Output(component_id="content", component_property="children"),
    Input(component_id='tab_switch', component_property='active_tab')
)
def update_content(input_value):
    return COMPONENT_MAPPING[input_value]
