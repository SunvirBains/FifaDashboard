
import plotly.express as px
import pandas as pd
import numpy as np
import dash
from dash import dcc, html, Input, Output
from dash.dependencies import Input, Output, State

df = pd.read_csv('FIFA.csv')

df['WINNERS'] = df['WINNERS'].replace('West Germany', 'Germany')
df['RUNNERUP'] = df['RUNNERUP'].replace('West Germany', 'Germany')

wins= df['WINNERS'].value_counts().reset_index()
wins.columns = ['Country','Wins']

container_style = {
    'backgroundColor': 'black',
    'color': 'white',
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif',
    'minHeight': '100vh'
}

navbar_style = {
    'display': 'flex',
    'flexDirection': 'row',
    'justifyContent': 'center',
    'gap': '30px',
    'padding': '20px',
    'backgroundColor': 'black'
}

dropdown_style = {
    'backgroundColor': 'black',
    'color': 'black'
}

label_style = {
    'color': 'white',
    'fontWeight': 'bold'
}


app = dash.Dash(__name__)
server=app.server

app.layout= html.Div(style=container_style, children=[
    html.H1("FIFA World Cup Stats",style={'textAlign': 'center', 'marginBottom': '20px'}),


    html.Div(style=navbar_style, children=[
        html.Div([
            html.Label("Select Country", style=label_style),
            dcc.Dropdown(
                id='Country_dropdown',
                options=[{'label': country, 'value': country} for country in wins['Country']],
                value=None,
                placeholder="Country",
                style=dropdown_style,
                clearable=True
            )
        ]),
        html.Div([
            html.Label("Select Year", style=label_style),
            dcc.Dropdown(
                id='Year_dropdown',
                options=[{'label': str(year), 'value': year} for year in df['YEAR'].unique()],
                value=None,
                placeholder="Year",
                style=dropdown_style,
                clearable=True
            )
        ])
    ]),

    # Display text outputs below the dropdowns
    html.Div(style={'padding': '10px', 'textAlign': 'center'}, children=[
        html.Div(id='country_wins', style={'marginBottom': '10px'}),
        html.Div(id='year_result', style={'marginBottom': '10px'})
    ]),
    html.H2("Choropleth Map of Winners",style={'textAlign':'center'}),
    dcc.Graph(id= 'worldcup_map'),


])

@app.callback(
    Output('worldcup_map','figure'),
    Input('Country_dropdown', 'value')
    
)
def update_map(selected_country):
    fig=px.choropleth(
        wins,
        locations='Country',
        locationmode= 'country names',
        color= 'Wins',
        hover_name= 'Country',
        color_continuous_scale= px.colors.sequential.Plasma,
        title= "World Cup wins by Country"
    )
    return fig

@app.callback(
    Output('country_wins','children'),
    Input('Country_dropdown','value')
)
def display_wins(selected_country):
    if selected_country is None:
        return 
    wins_count=wins[wins['Country']== selected_country]['Wins'].values[0]
    return f"{selected_country} has won the world cup {wins_count} times."

@app.callback(
    Output('year_result','children'),
    Input('Year_dropdown', 'value')
)

def display_final(selected_year):
    if selected_year is None:
        return 
    
    row= df[df['YEAR']==selected_year]
    winner=row.iloc[0]['WINNERS']
    runnerup= row.iloc[0]['RUNNERUP']
    return f"In {selected_year} the winner was {winner}, and the runner up was {runnerup}."


if __name__ == '__main__':
    app.run(debug=True)
