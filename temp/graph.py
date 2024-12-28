import random
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import webbrowser

# Create the Dash app
app = dash.Dash(__name__)

# Initial data
x_data = []
y_data = []

# Layout of the Dash app
app.layout = html.Div([
    dcc.Graph(id='real-time-plot'),
    dcc.Interval(
        id='interval-component',
        interval=500,  # Time in milliseconds (500 ms = 0.5 seconds)
        n_intervals=0  # Initial count of intervals
    )
])

# Update the plot at each interval
@app.callback(
    Output('real-time-plot', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_plot(n_intervals):
    # Generate a random value between 0 and 100
    random_value = random.randint(0, 100)
    
    # Append the new value to the data lists
    x_data.append(n_intervals)
    y_data.append(random_value)
    
    # Create the plot with the updated data
    figure = {
        'data': [go.Scatter(x=x_data, y=y_data, mode='lines+markers')],
        'layout': go.Layout(
            title="Real-Time Random Value Generation",
            xaxis={'title': 'Time (seconds)'},
            yaxis={'title': 'Random Value'},
            showlegend=False
        )
    }
    return figure

# Run the Dash app
if __name__ == '__main__':
    # Start the server and open the browser
    app.run_server(debug=True, use_reloader=False, port=8050)
    webbrowser.open("http://127.0.0.1:8050")  # Open the app in the browser
