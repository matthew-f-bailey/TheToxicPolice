import logging

from dash import Input, Output, callback, clientside_callback
from dash.dcc import Dropdown
from dash.html import Div, P, H2, A
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from aws.dynamo import get_all_subs, query_comments_by_subreddit_past_day
from settings import COLORS
from themes import plotly_theme
from components.errors import no_content_error_message
from settings import PLOTLY_TEMPLATE


logger = logging.getLogger(__name__)

SUBS = get_all_subs()

def subreddit():
    """
    The core component, presents needed interface and options and buttons
    to update the datat to be displayed
    """

    sub_names = sorted([x['display_name_prefixed'] for x in SUBS])
    return \
        Div(id='subreddit_view', children=[
            Dropdown(sub_names, sub_names[0], id='sub_dropdown'),
            Div(id='subreddit_info', children=[], style={'height': '15vh'}),
            Div(id='subreddit_content', children=[], style={'height': '85vh'})
        ])

def get_sub_desc(subreddit_name):
    """Update the sub description from the pulled in sub list"""
    the_sub = [x for x in SUBS if x['display_name_prefixed']==subreddit_name][0]
    desc = the_sub['public_description']
    if not desc:
        desc = 'No publc subreddit description available'
    return dbc.Card([
        dbc.Row([
            dbc.Col([
                H2([dbc.Badge(
                    subreddit_name,
                    color=COLORS.RED,
                    text_color=COLORS.WHITE,
                    className="border me-1",
                    pill=True
                )])
            ], width='auto'),
            dbc.Col([desc], width='auto')
        ])
    ])


@callback(
    Output(component_id='subreddit_content', component_property='children'),
    Output(component_id='subreddit_info', component_property='children'),
    Input(component_id='sub_dropdown', component_property='value')
)
def update_content(subreddit_name: str):
    """
    Single function to grab the commmetn data by sub, then pass it to get all
    the other componenets we need to udpate.
    Updates the content section and tirggers when a sub is selected
    """
    desc = get_sub_desc(subreddit_name)
    comment_data = query_comments_by_subreddit_past_day(subreddit_name)

    if not comment_data:
        return no_content_error_message(), desc

    df = pd.DataFrame(comment_data)

    children = []

    # Top Row
    top_row = dbc.Row(children=[], class_name='h-25')
    top_row.children.append(
        dbc.Col(get_top_toxic_cards(comment_data), width=6)
    )
    top_row.children.append(
        dbc.Col(create_toxic_count_bar(df), width=6)
    )
    children.append(top_row)

    # Second row
    second_row = dbc.Row(children=[], class_name='h-50')
    second_row.children.append(
        dbc.Col(create_toxic_count_bar(df), width=4)
    )
    second_row.children.append(
        dbc.Col(create_toxic_count_bar(df), width=4)
    )
    second_row.children.append(
        dbc.Col(create_toxic_count_bar(df), width=4)
    )
    children.append(second_row)

    # Third row
    third_row = dbc.Row(children=[], class_name='h-25')
    third_row.children.append(
        dbc.Col(create_toxic_count_bar(df), width=4)
    )
    third_row.children.append(
        dbc.Col(create_toxic_count_bar(df), width=4)
    )
    third_row.children.append(
        dbc.Col(create_toxic_count_bar(df), width=4)
    )
    children.append(third_row)
    return (children, desc)

##################################
##### Update helper functions ####
##################################
def get_top_toxic_cards(comment_data: list, num_cards:int = 4) -> list:
    """Grab the top toxic comments for the subreddit

    Args:
        comment_data (list): The comments as returned by dynamo

    Returns:
        dbc.Row: Row of cards
    """
    toxic_comments = [x for x in comment_data if x['toxic'] > 0.7]
    cards = dbc.Row(children=[])
    for i, comment in  enumerate(toxic_comments):

        if len(comment['body']) >= 125:
            comment_body = f"{comment['body'][0:125]}..."
        else:
            comment_body = comment['body']

        cards.children.append(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(f"Toxic probability: {comment['toxic']}", style={'backgroundColor': COLORS.DARK_BLUE, 'color': COLORS.WHITE}),
                    dbc.CardBody(
                        [
                            P(
                                comment_body,
                                className="card-text",
                            ),
                            dbc.Badge(
                                [A("Comment Link", href='https://www.reddit.com'+comment["permalink"], style={'color':COLORS.WHITE, 'text-decoration': 'none'})],
                                color=COLORS.DARK_BLUE,
                                className="me-1",
                                pill=True
                            )
                        ]
                    ),
                    dbc.CardFooter(f"Commented on post: {comment['post_title']}"),
                ]),
            )
        )
        if i==num_cards-1:
            break
    return cards

def create_toxic_count_bar(comment_df: pd.DataFrame) -> dcc.Graph:
    """Create a bar chart for counts of toxic comments"""
    mappings = {
        'toxic': 'Toxic',
        'severe_toxic': 'Severe Toxic',
        'obscene': 'Obscene',
        'threat': 'Threat',
        'insult': 'Insult',
        'identity_hate': 'Identity Hate',
    }
    totals = comment_df[list(mappings.keys())].sum().rename('Count', inplace=True)
    totals.index = list(mappings.values())
    fig = px.bar(
        totals,
        title='Total counts of toxic comments by toxicity type',
        labels={'index': 'Toxicity Type', 'value': 'Count'},
        template=PLOTLY_TEMPLATE
    )
    fig.update_layout(
        showlegend=False,
        height=200,
        margin=dict(l=10, r=10, t=10, b=20),
    )
    return  dbc.Card([dbc.CardBody([
        dcc.Graph(figure=fig)
    ])])
