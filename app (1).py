import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# Load data
df = pd.read_csv("data/owid-covid-data.csv")
df["date"] = pd.to_datetime(df["date"])
df = df[df["continent"].notna()]

# Latest data per country
latest = df.sort_values("date").groupby("location").tail(1)

app = Dash(_name_)
server = app.server

app.layout = html.Div([
    html.H1("COVID-19 Public Health Trends Dashboard", style={"textAlign": "center"}),

    html.Label("Select Country:"),
    dcc.Dropdown(
        options=[{"label": c, "value": c} for c in sorted(df["location"].unique())],
        value="United States",
        id="country_dropdown"
    ),

    dcc.Graph(id="cases_trend"),
    dcc.Graph(id="deaths_trend"),
    dcc.Graph(id="stringency_trend"),

    html.H2("Global Comparisons", style={"textAlign": "center"}),
    dcc.Graph(
        figure=px.choropleth(
            latest,
            locations="location",
            locationmode="country names",
            color="total_cases_per_million",
            title="Total Cases per Million (Latest)"
        )
    ),

    dcc.Graph(
        figure=px.scatter(
            latest,
            x="stringency_index",
            y="new_cases_per_million",
            hover_name="location",
            title="Stringency Index vs New Cases per Million (Latest)"
        )
    )
])

# Callback for selected country
@app.callback(
    Output("cases_trend", "figure"),
    Output("deaths_trend", "figure"),
    Output("stringency_trend", "figure"),
    Input("country_dropdown", "value")
)
def update_country_charts(country):
    filtered = df[df["location"] == country]

    fig1 = px.line(filtered, x="date", y="total_cases",
                   title=f"Total Cases Over Time - {country}")

    fig2 = px.line(filtered, x="date", y="total_deaths",
                   title=f"Total Deaths Over Time - {country}")

    fig3 = px.line(filtered, x="date", y="stringency_index",
                   title=f"Stringency Index Over Time - {country}")

    return fig1, fig2, fig3


if _name_ == "_main_":
    app.run_server(debug=True)