import json
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import plotly.graph_objs as go

# Load system configuration
with open("config/sample_system.json") as f:
    system_config = json.load(f)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])  # NASA-vibe theme

# Extract data
cpu = system_config["cpu"]
memory = system_config["memory"]
bus = system_config["bus"]

# Bar graph for CPU specs
cpu_bar = dcc.Graph(
    figure=go.Figure(
        data=[
            go.Bar(name="CPU Specs", x=["Registers", "Cache (KB)", "Frequency (GHz)"],
                   y=[cpu["registers"], cpu["cache_kb"], cpu["frequency_ghz"]],
                   marker_color='lightblue')
        ],
        layout=go.Layout(title="CPU Specifications", plot_bgcolor='black', paper_bgcolor='black',
                         font=dict(color='white'))
    ),
    config={"displayModeBar": False}
)

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("🚀 RADSAFE System Dashboard", className="text-center text-info mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.H3(f"🛰️ {system_config['system_name']}", className="text-warning mb-3"),
            html.H5("🧠 CPU", className="text-light"),
            html.P(f"Registers: {cpu['registers']}", className="text-light"),
            html.P(f"Cache: {cpu['cache_kb']} KB", className="text-light"),
            html.P(f"Frequency: {cpu['frequency_ghz']} GHz", className="text-light"),
        ], md=4),
        dbc.Col(cpu_bar, md=8)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.H5("💾 Memory", className="text-light"),
            html.P(f"Size: {memory['size_mb']} MB", className="text-light"),
            html.P(f"Type: {memory['mem_type']}", className="text-light"),
        ], md=6),
        dbc.Col([
            html.H5("🔌 Bus", className="text-light"),
            html.P(f"Type: {bus['bus_type']}", className="text-light"),
            html.P(f"Width: {bus['width_bits']} bits", className="text-light"),
        ], md=6)
    ]),
    html.Hr(),
    dbc.Row([
        dbc.Col(html.P("🛰️ Designed for Mission Readiness | Powered by Dash + Plotly", className="text-center text-muted"))
    ])
], fluid=True)

if __name__ == '__main__':
    app.run(debug=False)
