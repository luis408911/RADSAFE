import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import json

# Load system config
with open("config/sample_system.json") as f:
    system_config = json.load(f)

# Load fault log CSV (update filename as needed)
fault_df = pd.read_csv("fault_log.csv")  # Ensure this file exists in the root directory

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

# Create a timeline bar chart of fault counts over time
fig_faults = px.histogram(
    fault_df,
    x="timestamp",
    color="severity",
    title="Faults Over Time",
    labels={"timestamp": "Timestamp", "count": "Fault Count"},
    nbins=30
)

fig_faults.update_layout(bargap=0.2, plot_bgcolor="#1e1e1e", paper_bgcolor="#1e1e1e", font_color="white")

app.layout = dbc.Container([
    html.H1("🚀 RADSAFE System Dashboard", className="my-3 text-warning"),

    html.H2(system_config["system_name"], className="text-light"),

    html.H4("\U0001F9EA CPU", className="mt-4 text-info"),
    html.P(f"Registers: {system_config['cpu']['registers']}", className="text-light"),
    html.P(f"Cache: {system_config['cpu']['cache_kb']} KB", className="text-light"),
    html.P(f"Frequency: {system_config['cpu']['frequency_ghz']} GHz", className="text-light"),

    html.H4("📠 Memory", className="mt-4 text-info"),
    html.P(f"Size: {system_config['memory']['size_mb']} MB", className="text-light"),
    html.P(f"Type: {system_config['memory']['mem_type']}", className="text-light"),

    html.H4("🧵 Bus", className="mt-4 text-info"),
    html.P(f"Type: {system_config['bus']['bus_type']}", className="text-light"),
    html.P(f"Width: {system_config['bus']['width_bits']} bits", className="text-light"),

    html.Hr(className="my-4"),

    html.H3("🔍 Fault Logs Explorer", className="text-warning"),

    dbc.Row([
        dbc.Col([
            html.Label("Component", className="text-light"),
            dcc.Dropdown(
                id="component-filter",
                options=[{"label": comp, "value": comp} for comp in fault_df["component"].unique()],
                placeholder="Select component"
            )
        ], md=6),

        dbc.Col([
            html.Label("Severity", className="text-light"),
            dcc.Dropdown(
                id="severity-filter",
                options=[{"label": sev, "value": sev} for sev in fault_df["severity"].unique()],
                placeholder="Select severity"
            )
        ], md=6),
    ], className="mb-4"),

    dcc.Graph(id="fault-timeline", figure=fig_faults),

], fluid=True)

@app.callback(
    Output("fault-timeline", "figure"),
    Input("component-filter", "value"),
    Input("severity-filter", "value")
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

if __name__ == "__main__":
    app.run(debug=True)
