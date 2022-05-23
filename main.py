from dash import dcc, html
import dash
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd 


df = pd.read_csv('EMSdataset.csv')
df_diff = df.drop(columns=['Date/time']).diff()
df_diff.insert(0, 'Date/time' ,df['Date/time'])
df_diff = df_diff.iloc[1:,:]
df = df_diff
df['Date/time'] = pd.to_datetime(df['Date/time'])
df['Date'] = pd.to_datetime(df['Date/time']).dt.date



app = dash.Dash(
    __name__,
    suppress_callback_exceptions = True, 
    )

app.layout = html.Div([
    html.H1(id='sankey-page', children=['App 5'], style={'textAlign':'center', 'marginBottom':'5vh'}),
        dbc.Row([
            html.Div([
                dcc.Dropdown(
                    id='slct_month_s', 
                    options=[
                        {'label': m , 'value':m} for m in df['Date/time'].dt.month_name().unique()
                        ],
                    value='July',
                    style={"textAlign": "center", 'border':'transparent'}, 
                ),

            ], 
            style={'width':'20%'}),
        ]),
        dbc.Row([
            html.H3(id='simple-title', children=['Sankey']),
            dcc.Graph(id='basic-sankey', figure={}),
        ]),
])


@app.callback(
  Output('basic-sankey', 'figure'),
  Input('slct_month_s','value'),
  
)
def basic_sankey(slct_month):
    dfs = df.copy()
    dfs = dfs[dfs['Date/time'].dt.month_name() ==slct_month]
    
    generators = [g for g in dfs.columns if g.startswith('Gen')]
    receivers = [r for r in dfs.columns if r.startswith('Rec')]
    
    fig = go.Figure(data= [go.Sankey(
        node = dict(
          pad = 15,
          thickness = 20,
          line = dict(color = "black", width = 0.5),
            label = ["Total Consumption"] + generators + receivers,
          color = ['red'] + ['green']*len(generators) + ['red']*len(receivers),
        ),
        link = dict(
          source = [i for i in range(1, len(generators)+1)]+[0]*(len(receivers)), 
          target = [0]*len(generators)+[i for i in range(11, len(receivers)+11)],
          value = [df[g].sum() for g in generators] + [df[r].sum() for r in receivers]
      ))]
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, threaded= True)
