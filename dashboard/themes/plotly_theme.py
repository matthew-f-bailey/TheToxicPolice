import plotly.graph_objects as go
import plotly.io as pio

from settings import COLORS

pio.templates["custom"] = go.layout.Template(
    # LAYOUT
    layout = {
        # Fonts
        # Note - 'family' must be a single string, NOT a list or dict!
        'title':
            {'font': {'family': 'verdana, arial, helvetica, sans-serif',
                      'size': 14,
                      'color': '#333'}
            },
        'font': {'family': 'verdana, arial, helvetica, sans-serif',
                      'size':12,
                      'color': '#333'},
        # Colorways
        'colorway': ['#ec7424', '#a4abab'],
        # Keep adding others as needed below
        'paper_bgcolor': COLORS.WHITE
    },
    # DATA
    data = {
        # Each graph object must be in a tuple or list for each trace
        'bar': [go.Bar(textposition='outside',
                       textfont={'family': 'Helvetica Neue, Helvetica, Sans-serif',
                                 'size': 20,
                                 'color': '#FFFFFF'
                                 })]
    }
)