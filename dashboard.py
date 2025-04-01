import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import json
import threading
import time

from radsafe.core.alert_engine import check_for_critical_faults

# Load system config
with open('config/sample_system.json') as f:
    system_config = json.load(f)

# Load fault log data
fault_df = pd.read_csv('fault_logs.csv')

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
app.title = "RADSAFE Dashboard"

# Layout
app.layout = dbc.Container([
    html.H1("🚀 RADSAFE System Dashboard", className="text-primary mt-4"),
    html.H2(system_config['system_name'], className="text-info"),

    html.Hr(),

    dbc.Row([
        dbc.Col([
            html.H4("🧠 CPU"),
            html.P(f"Registers: {system_config['cpu']['registers']}"),
            html.P(f"Cache: {system_config['cpu']['cache_kb']} KB"),
            html.P(f"Frequency: {system_config['cpu']['frequency_ghz']} GHz")
        ], width=4),
        dbc.Col([
            html.H4("💾 Memory"),
            html.P(f"Size: {system_config['memory']['size_mb']} MB"),
            html.P(f"Type: {system_config['memory']['mem_type']}")
        ], width=4),
        dbc.Col([
            html.H4("🛠 Bus"),
            html.P(f"Type: {system_config['bus']['bus_type']}"),
            html.P(f"Width: {system_config['bus']['width_bits']} bits")
        ], width=4)
    ]),

    html.Hr(),

    html.H3("📊 Fault Log Analytics", className="text-warning"),

    dbc.Row([
        dbc.Col([
            html.Label("Component"),
            dcc.Dropdown(
                options=[{'label': c, 'value': c} for c in fault_df['component'].unique()],
                id='component-dropdown'
            )
        ], width=6),
        dbc.Col([
            html.Label("Severity"),
            dcc.Dropdown(
                options=[{'label': s, 'value': s} for s in fault_df['severity'].unique()],
                id='severity-dropdown'
            )
        ], width=6)
    ], className="mb-4"),

    dcc.Graph(id='fault-graph'),

    html.Div(id='live-alerts', className="text-danger font-weight-bold mt-4"),

    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # every 5 seconds
        n_intervals=0
    )
], fluid=True)

# Callback for updating graph
@app.callback(
    Output('fault-graph', 'figure'),
    [Input('component-dropdown', 'value'),
     Input('severity-dropdown', 'value')]
)
def update_chart(component, severity):
    filtered = fault_df.copy()
    if component:
        filtered = filtered[filtered["component"] == component]
    if severity:
        filtered = filtered[filtered["severity"] == severity]

    fig = px.histogram(
        filtered,
        x="timestamp",
        color="severity",
        title="Filtered Faults Over Time",
        nbins=30
    )
    fig.update_layout(bargap=0.2, plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e", font_color="white")
    return fig

# Callback for real-time alert UI display
@app.callback(
    Output('live-alerts', 'children'),
    Input('interval-component', 'n_intervals')
)
def display_alert(n):
    alert_msg = check_for_critical_faults()
    if alert_msg:
        return f"🚨 {alert_msg}"
    return ""

if __name__ == "__main__":
    app.run(debug=True)
