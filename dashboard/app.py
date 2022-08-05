from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

app = Dash(__name__)

header_md = """
**This is some markdown**.
Here is a link to [Google](https://www.google.com)
- foo
- bar
- baz
"""

df = pd.DataFrame({
    "Fruit": "Apple Orange Apple Banana".split(' '),
    "Amount": "5 4 3 2".split(' '),
    "City": "SF NM OJ PO".split(' ')
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

app.layout = html.Div(children=[
    dcc.Markdown(header_md),
    html.H1(children="Hello Dash"),
    html.Div(children="Dash: A web application framework"),
    dcc.Graph(id='example', figure=fig)
])

if __name__=='__main__':
    app.run_server(debug=True)