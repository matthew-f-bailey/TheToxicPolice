from dash import Input, Output, callback
from dash.html import Div, Ul
from dash.dcc import Tabs, Tab
import dash_bootstrap_components as dbc

from components.overview import overview
from components.subreddit import subreddit

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
        dbc.Card([
            dbc.CardHeader(
                dbc.Tabs(id='tab_switch', active_tab=OVERVIEW, children=[
                    dbc.Tab(label=OVERVIEW, tab_id=OVERVIEW),
                    dbc.Tab(label=SUBREDDIT, tab_id=SUBREDDIT)
                ])
            ),
            dbc.CardBody(Div(id='content', children=[])),
        ])
        # Div(className='container', children=[
        #     Div(id='tabs_switcher', className='nav flex-column nav-pills', children=[
        #         Tabs(value=OVERVIEW, id='tab_switch', children=[
        #             Tab(value=k, label=k) for k in COMPONENT_MAPPING.keys()
        #         ])
        #     ]),
        #     Div(id='content', children=[])
        # ])

@callback(
    Output(component_id="content", component_property="children"),
    Input(component_id='tab_switch', component_property='active_tab')
)
def update_content(input_value):
    return COMPONENT_MAPPING[input_value]
