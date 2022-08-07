import logging
import json

from dash import Input, Output, callback
from dash.dcc import Dropdown
from dash.html import Div, P, H4, H6
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from aws.dynamo import get_all_subs, query_comments_by_subreddit

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
                Div(id='subreddit_info', children=[]),
                Div(id='subreddit_content', children=[])
        ])

@callback(
    Output(component_id='subreddit_info', component_property='children'),
    Input(component_id='sub_dropdown', component_property='value')
)
def update_sub_desc(subreddit_name):
    """Update the sub description from the pulled in sub list"""
    the_sub = [x for x in SUBS if x['display_name_prefixed']==subreddit_name][0]
    desc = the_sub['public_description']
    return P(desc)


@callback(
    Output(component_id='subreddit_content', component_property='children'),
    Input(component_id='sub_dropdown', component_property='value')
)
def update_content(subreddit_name):
    """
    Single function to grab the commmetn data by sub, then pass it to get all
    the other componenets we need to udpate.
    Updates the content section and tirggers when a sub is selected
    """
    comment_data = query_comments_by_subreddit(subreddit_name)
    df = pd.DataFrame(comment_data)
    children = []
    children.append(get_top_toxic_cards(comment_data))
    children.append(create_toxic_count_hist(df))
    children.append(create_toxic_count_hist(df))
    return children

##################################
##### Update helper function #####
##################################
def get_top_toxic_cards(comment_data: list) -> dbc.Row:
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
                    dbc.CardHeader(f"Toxic probability: {comment['toxic']}"),
                    dbc.CardBody(
                        [
                            P(
                                comment_body,
                                className="card-text",
                            ),
                            dbc.CardLink("Comment link", href='https://www.reddit.com'+comment["permalink"]),
                        ]
                    ),
                    dbc.CardFooter(f"Commented on post: {comment['post_title']}"),
                ]),
                style={"width": "18rem"}
            )
        )
        if i==4:
            break
    return cards

def create_toxic_count_hist(comment_df: pd.DataFrame) -> dcc.Graph:
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
    )
    return dcc.Graph(figure=fig)
