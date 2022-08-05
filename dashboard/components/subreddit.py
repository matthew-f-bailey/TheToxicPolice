from dash import Input, Output, callback
from dash.dcc import Dropdown
from dash.html import Div

from aws.dynamo import get_all_subs

def subreddit():
    subs = get_all_subs()
    print(subs[0])
    sub_names = sorted([x['display_name_prefixed'] for x in subs])
    return \
        Div(id='subreddit-view', children=[
            Dropdown(sub_names, sub_names[0], id='sub_dropdown')
        ])


# @callback(
#     Output(component_id='content', component_property='children'),
#     Input(component_id='tab_switch', component_property='value')
# )
# def update_sub_list(input_value)