from dash import Input, Output, callback
from dash.html import Div
from dash.dcc import RadioItems

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
        Div(className='body', children=[
            Div(id='tabs_switcher', children=[
                RadioItems([OVERVIEW, SUBREDDIT], OVERVIEW, id='tab_switch')
            ]),
            Div(id='content', children=[])
        ])

@callback(
    Output(component_id='content', component_property='children'),
    Input(component_id='tab_switch', component_property='value')
)
def update_content(input_value):
    return COMPONENT_MAPPING[input_value]
