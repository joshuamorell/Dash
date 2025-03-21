#!/usr/bin/env python
# coding: utf-8

# In[2]:

import dash
from dash import Dash, dcc, html, Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

# Load and process data
df = pd.read_csv('Trial.csv')
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df.dropna(subset=['Result', 'Site', 'Compound'])

# Initialize Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Trial Results Dashboard", style={'textAlign': 'center'}),
    
    # Dropdowns for selecting Site and Compound
    html.Div([
        html.Label("Select Site:"),
        dcc.Dropdown(
            id='site-dropdown',
            options=[{'label': site, 'value': site} for site in sorted(df['Site'].unique())],
            value=df['Site'].unique()[0],  # Default value
            clearable=False
        ),
    ], style={'width': '50%', 'margin': '10px'}),

    html.Div([
        html.Label("Select Compound:"),
        dcc.Dropdown(
            id='compound-dropdown',
            options=[{'label': compound, 'value': compound} for compound in sorted(df['Compound'].unique())],
            value=df['Compound'].unique()[0],  # Default value
            clearable=False
        ),
    ], style={'width': '50%', 'margin': '10px'}),
    
    # Graph display
    dcc.Graph(id='result-graph')
])

# Callback to update the graph
@app.callback(
    Output('result-graph', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('compound-dropdown', 'value')]
)
def update_graph(selected_site, selected_compound):
    filtered_df = df[(df['Site'] == selected_site) & (df['Compound'] == selected_compound)]

    if filtered_df.empty:
        fig = px.scatter(title=f"No data available for {selected_compound} at {selected_site}")
    else:
        fig = px.scatter(
            filtered_df,
            x='Date',
            y='Result',
            color='Source',
            title=f'Results for {selected_compound} at {selected_site}',
            labels={'Result': 'Concentration', 'Date': 'Date'},
            template='plotly_white'
        )
        fig.update_layout(hovermode='x unified', showlegend=True, height=600)

    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




