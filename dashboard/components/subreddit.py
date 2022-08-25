import logging
from datetime import datetime, timezone

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, Input, Output, callback
from dash.dcc import Dropdown
from dash.html import Div, P, H1, H2, H5, A, I, Span

from aws.dynamo import get_all_subs, query_comments_by_subreddit_past_day
from components.errors import no_content_error_message
from settings import COLORS
from settings import PLOTLY_TEMPLATE
from themes import plotly_theme  # Caution: Needed even though not used


logger = logging.getLogger(__name__)

SUBS = get_all_subs()
FILL_PARENT_BS_CLASS = 'h-100 mx-sm pb-sm'
TOXIC_THRESH = 0.6


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

def get_sub_desc(subreddit_name: str, last_updated: str):
    """Update the sub description from the pulled in sub list"""
    the_sub = [x for x in SUBS if x['display_name_prefixed']==subreddit_name][0]
    desc = the_sub['public_description']
    if not desc:
        desc = 'No publc subreddit description available'
    return dbc.Card([
        dbc.Row([
            dbc.Col([
                H2([
                    dbc.Badge(
                        subreddit_name,
                        color=COLORS.RED,
                        text_color=COLORS.WHITE,
                        className="border me-1",
                        pill=True
                    ),
                ]),
                Span(f"Last updated: {last_updated}")
            ], width='auto'),
            dbc.Col([desc], width='auto')
        ])
    ])

def get_last_updated(comments: list) -> str:
    """From all the comments. find the most recent one"""
    create_dates = [
        comment.get('created_utc')
        for comment
        in comments
    ]
    if not create_dates:
        return "More than 24 hours ago"
    latest = int(max(create_dates))
    latest_time = datetime.utcfromtimestamp(latest)
    return str(latest_time) + ' utc'

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
    comment_data = query_comments_by_subreddit_past_day(subreddit_name)
    last_updated = get_last_updated(comment_data)
    desc = get_sub_desc(subreddit_name, last_updated)

    if not comment_data:
        return no_content_error_message(), desc

    df = pd.DataFrame(comment_data)

    children = []

    # Top Row
    top_row = dbc.Row(children=[], class_name='h-25')
    top_row.children.append(
        dbc.Col(get_top_toxic_cards(comment_data), md=4, class_name=FILL_PARENT_BS_CLASS)
    )
    top_row.children.append(
        dbc.Col(get_toxic_count_cards(comment_data), md=8, class_name=FILL_PARENT_BS_CLASS)
    )
    children.append(top_row)

    # Second row
    second_row = dbc.Row(children=[], class_name='h-50')
    second_row.children.append(
        dbc.Col(get_score_box_charts(df), md=8, class_name=FILL_PARENT_BS_CLASS)
    )
    second_row.children.append(
        dbc.Col(create_pie_toxicity_type(df), md=4, class_name=FILL_PARENT_BS_CLASS)
    )
    children.append(second_row)

    # Third row
    third_row = dbc.Row(children=[], class_name='h-25')
    third_row.children.append(
        dbc.Col(create_toxic_count_bar(df), md=4, class_name=FILL_PARENT_BS_CLASS)
    )
    third_row.children.append(
        dbc.Col(create_toxic_count_bar(df), md=4, class_name=FILL_PARENT_BS_CLASS)
    )
    third_row.children.append(
        dbc.Col(create_toxic_count_bar(df), md=4, class_name=FILL_PARENT_BS_CLASS)
    )
    children.append(third_row)
    return (children, desc)

##################################
##### Update helper functions ####
##################################
def get_top_toxic_cards(comment_data: list, num_cards:int = 1) -> list:
    """Grab the top toxic comments for the subreddit

    Args:
        comment_data (list): The comments as returned by dynamo

    Returns:
        dbc.Row: Row of cards
    """
    toxic_comments = [x for x in comment_data if x['toxic'] > TOXIC_THRESH]
    cards = dbc.Row(children=[], class_name=FILL_PARENT_BS_CLASS)
    for i, comment in  enumerate(toxic_comments):

        shrink_under = lambda s, num: s if len(s)<=num else s[0:num]

        comment_body = shrink_under(comment['body'], 1000)
        post_title = shrink_under(comment['post_title'], 1000)

        cards.children.append(
            dbc.Col(class_name=FILL_PARENT_BS_CLASS, md=12, children=[
                dbc.Card(children=[
                    dbc.CardHeader(style={'backgroundColor': COLORS.DARK_BLUE, 'color': COLORS.WHITE}, children=[
                        Span(f"Random Toxic Comment"),
                        Span(f" (Toxic probability: {comment['toxic']})", style={'font-style': 'italic'})
                    ]),
                    dbc.CardBody(children=[
                            P(
                                comment_body,
                                className="card-text text-truncate",
                            ),
                            dbc.Badge(
                                [A("Comment Link", href='https://www.reddit.com'+comment["permalink"], style={'color':COLORS.WHITE, 'text-decoration': 'none'})],
                                color=COLORS.DARK_BLUE,
                                className="me-1",
                                pill=True
                            )
                        ]
                    ),
                    dbc.CardFooter(
                        P(f"Commented on post: {post_title}", className='text-truncate')
                    ),
                ]),
            ])
        )
        if i==num_cards-1:
            break
    return cards

def get_toxic_count_cards(comment_data: list) -> list:

    toxic, severe_toxic, obscene, threat, insult, identity_hate = [],[],[],[],[],[]
    for comment in comment_data:
        if comment['toxic'] > TOXIC_THRESH:
            toxic.append(comment)
        if comment['severe_toxic'] > TOXIC_THRESH:
            severe_toxic.append(comment)
        if comment['obscene'] > TOXIC_THRESH:
            obscene.append(comment)
        if comment['threat'] > TOXIC_THRESH:
            threat.append(comment)
        if comment['insult'] > TOXIC_THRESH:
            insult.append(comment)
        if comment['identity_hate'] > TOXIC_THRESH:
            identity_hate.append(comment)

    toxic_counts = {
        'Toxic': [len(toxic), 'fas fa-skull-crossbones', 'red'],
        'Severe Toxic': [len(severe_toxic), 'fa-solid fa-biohazard', 'green'],
        'Obscene': [len(obscene), 'fa-solid fa-eye-slash', 'purple'],
        'Threat': [len(threat), 'fa-solid fa-gun', 'black'],
        'Insult': [len(insult), 'fa-solid fa-sad-cry', 'blue'],
        'Identity Hate': [len(identity_hate), 'fa-solid fa-id-card', 'green'],
    }
    cards = dbc.Row(children=[], class_name=FILL_PARENT_BS_CLASS)
    for label, count_icon in toxic_counts.items():
        count = count_icon[0]
        icon = count_icon[1]
        color = count_icon[2]
        cards.children.append(
            dbc.Col(class_name=FILL_PARENT_BS_CLASS, children=[
                dbc.Card(children=[
                    dbc.CardBody(children=[
                        H1(count, className='display-1 counter', id=f"data-{count}"),
                        Span([
                            I(className=icon, style={'color': color}),
                            Span(' '+label, style={'font-size': '20px'}),
                        ], className='d-inline')
                    ], class_name=f'text-center {FILL_PARENT_BS_CLASS}'),
                ], class_name=FILL_PARENT_BS_CLASS),
            ])
        )
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
        autosize = True
    )
    return  dbc.Card([dbc.CardBody([
        dcc.Graph(figure=fig, className=FILL_PARENT_BS_CLASS)
    ], className=FILL_PARENT_BS_CLASS)], className=FILL_PARENT_BS_CLASS)

def create_pie_toxicity_type(comment_df: pd.DataFrame) -> dcc.Graph:

    totals = comment_df[['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']].sum()
    totals.rename('Count', inplace=True)
    totals.index = ['Toxic', 'Severe Toxic', 'Obscene', 'Threat', 'Insult', 'Identity Hate']
    fig = px.pie(
        totals,
        title="Breakdown of toxic comments by type",
        values="Count",
        names=totals.index,
        hole=.3
    )
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10))
    return  dbc.Card([dbc.CardBody([
        dcc.Graph(figure=fig, className=FILL_PARENT_BS_CLASS)
    ], className=FILL_PARENT_BS_CLASS)], className=FILL_PARENT_BS_CLASS)

def get_score_box_charts(comments: pd.DataFrame):

    # Take only toxic comments
    all_toxic = comments.copy()[
        (comments['toxic']==1) |
        (comments['severe_toxic']==1) |
        (comments['obscene']==1) |
        (comments['threat']==1) |
        (comments['insult']==1) |
        (comments['identity_hate']==1)
    ]
    toxic_cols = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    all_toxic['total_toxic'] = all_toxic[toxic_cols].sum(axis=1)

    def toxic_cat(row):
        """Define which toxic type they are, or multiple"""
        if row['total_toxic'] > 1:
            return 'Multiple'
        for col in toxic_cols:
            if row[col]:
                return col.replace('_', ' ').title()

    all_toxic['toxic_cat'] = all_toxic.apply(toxic_cat, axis=1)

    fig = px.box(all_toxic, x='score', y='toxic_cat', color='toxic_cat', boxmode="overlay",
                 title='Score by Toxicity Type', labels={"toxic_cat": "Category", "score": "Score"})
    fig.update_layout(legend_title_text='Toxicity Category', boxgap=0.2, boxgroupgap=0.2, margin=dict(l=0, r=0, t=40, b=0))
    fig.update_traces(orientation='h')
    trace = list(px.scatter(all_toxic, x='score', y='toxic_cat', color='toxic_cat').select_traces())
    for i in range(7):
        try:
            trace[i].update(showlegend=False)
        except IndexError:
            pass
    return  dbc.Card([dbc.CardBody([
        dcc.Graph(figure=fig, className=FILL_PARENT_BS_CLASS)
    ], className=FILL_PARENT_BS_CLASS)], className=FILL_PARENT_BS_CLASS)
