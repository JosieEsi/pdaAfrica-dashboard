from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load your data
df1 = pd.read_excel("Membership.xlsx")
df2 = pd.read_excel("Yearly membership.xlsx")  # Membership data for line chart 1
df3 = pd.read_excel("Average reading session.xlsx")  # Average session data for line chart 2

# Mapping dictionary for consistent club names
club_name_mapping = {
    'Mankranso': 'Mankranso community reading club',
    'Boatenkrom': 'Boatengkrom community reading club',
    'Potrikrom': 'Potrikrom community reading club',
    'Dunyan Nkwanta': 'Dunyan Nkanta community reading club',
    'Kunsu': 'Kunsu community reading club',
    'Abesewa': 'Abesewa community reading club',
    'Asempaneye': 'Asempaneye community reading club',
    'Asuadei': 'Asuadei community reading club',
    'Barniekrom': 'Barniekrom community reading clubs',
    'Biemso No.1': 'Biemso no.1 community reading club'
}

# Apply the mapping to standardize names in df2 and df3
df2['Reading Club'] = df2['Reading Club'].replace(club_name_mapping)
df3['Reading Club'] = df3['Reading Club'].replace(club_name_mapping)

# Remove the word "community" from all club names for display purposes
df1['Reading club'] = df1['Reading club'].str.replace('community', '', regex=False)
df2['Reading Club'] = df2['Reading Club'].str.replace('community', '', regex=False)
df3['Reading Club'] = df3['Reading Club'].str.replace('community', '', regex=False)

# Initialize the Dash app
app = Dash(__name__)

# Define all clubs for the dropdown with a "Select All" option
all_clubs = df1['Reading club'].unique().tolist()
dropdown_options = [{'label': 'Select All', 'value': 'all'}] + [{'label': club, 'value': club} for club in all_clubs]

# Define the layout
app.layout = html.Div([
    # Navigation Bar with Title
    html.Div([
        html.H1("Community Reading Project", style={
            'margin': '0', 'color': '#FFFFFF', 'padding': '20px', 'textAlign': 'center',
            'fontWeight': 'bold', 'fontStyle': 'italic', 'fontSize': '36px', 'textShadow': '2px 2px 4px #000000'
        })
    ], style={'backgroundColor': '#007acc', 'marginBottom': '20px', 'boxShadow': '0px 4px 8px rgba(0, 0, 0, 0.1)'}),

    # Dropdown Slicer for Reading Clubs
    html.Div([
        dcc.Dropdown(
            id='club-selector',
            options=dropdown_options,
            value=all_clubs,  # Default to all clubs selected
            multi=True,
            placeholder="Select Reading Club(s)"
        )
    ], style={'width': '50%', 'margin': '0 auto', 'padding': '10px'}),

    # Cards for Total Numbers
    html.Div([
        html.Div(id='males-card', className='card', style={
            'backgroundColor': '#FFFFFF', 'padding': '30px', 'borderRadius': '10px',
            'boxShadow': '0px 4px 12px rgba(0, 0, 0, 0.1)', 'width': '30%', 'textAlign': 'center',
            'fontSize': '20px', 'margin': '10px', 'color': '#007acc'
        }),
        html.Div(id='females-card', className='card', style={
            'backgroundColor': '#FFFFFF', 'padding': '30px', 'borderRadius': '10px',
            'boxShadow': '0px 4px 12px rgba(0, 0, 0, 0.1)', 'width': '30%', 'textAlign': 'center',
            'fontSize': '20px', 'margin': '10px', 'color': '#FF7F50'
        }),
        html.Div(id='total-card', className='card', style={
            'backgroundColor': '#FFFFFF', 'padding': '30px', 'borderRadius': '10px',
            'boxShadow': '0px 4px 12px rgba(0, 0, 0, 0.1)', 'width': '30%', 'textAlign': 'center',
            'fontSize': '20px', 'margin': '10px', 'color': '#32CD32'
        }),
    ], style={'display': 'flex', 'justify-content': 'space-around', 'padding': '10px'}),

    # Chart Area
    html.Div([
        # Gender Difference Pie Chart
        html.Div([dcc.Graph(id='gender-pie-chart')],
                 style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),
        # Line Charts for Membership Comparison and Average Reading Sessions
        html.Div([
            dcc.Graph(id='membership-line-chart'),
            dcc.Graph(id='average-session-line-chart')
        ], style={'width': '65%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'})
    ], style={'backgroundColor': '#F3F3F3', 'padding': '20px', 'borderRadius': '15px',
              'boxShadow': '0px 4px 12px rgba(0, 0, 0, 0.2)', 'width': '90%', 'margin': '20px auto'})
], style={'backgroundColor': '#E6E6FA', 'fontFamily': 'Arial, sans-serif'})

# Callbacks for interactivity
@app.callback(
    Output('club-selector', 'value'),
    Input('club-selector', 'value')
)
def update_dropdown(selected_clubs):
    if 'all' in selected_clubs:
        return all_clubs  # Select all clubs when "Select All" is chosen
    return selected_clubs

@app.callback(
    [Output('males-card', 'children'),
     Output('females-card', 'children'),
     Output('total-card', 'children')],
    [Input('club-selector', 'value')]
)
def update_cards(selected_clubs):
    filtered_df = df1[df1['Reading club'].isin(selected_clubs)]
    males = filtered_df['Number of males'].sum()
    females = filtered_df['Number of females'].sum()
    total_readers = filtered_df['Total'].sum()
    return f'Males: {males}', f'Females: {females}', f'Total Readers: {total_readers}'

@app.callback(
    Output('gender-pie-chart', 'figure'),
    [Input('club-selector', 'value')]
)
def update_gender_pie_chart(selected_clubs):
    filtered_df = df1[df1['Reading club'].isin(selected_clubs)]
    gender_data = {'Gender': ['Males', 'Females'],
                   'Count': [filtered_df['Number of males'].sum(), filtered_df['Number of females'].sum()]}
    gender_df = pd.DataFrame(gender_data)
    fig = px.pie(gender_df, names='Gender', values='Count', title="Gender Difference of Members",
                 color_discrete_sequence=px.colors.sequential.RdBu)
    return fig

@app.callback(
    Output('membership-line-chart', 'figure'),
    [Input('club-selector', 'value')]
)
def update_membership_line_chart(selected_clubs):
    filtered_df = df2[df2['Reading Club'].isin(selected_clubs)]
    fig = px.line(
        filtered_df,
        x='Reading Club',
        y=['2023 Total Membership', '2024 Total Membership'],
        title="Membership of 2023 Vs 2024",
        markers=True
    )
    return fig

@app.callback(
    Output('average-session-line-chart', 'figure'),
    [Input('club-selector', 'value')]
)
def update_average_session_line_chart(selected_clubs):
    filtered_df = df3[df3['Reading Club'].isin(selected_clubs)]
    fig = px.line(
        filtered_df,
        x='Reading Club',
        y=['2023 Average reading session', '2024 Average reading session'],
        title="Average Reading Session of 2023 Vs 2024",
        markers=True
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
