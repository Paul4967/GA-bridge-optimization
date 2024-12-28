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
y_data_1 = []  # First plot y-values (single random value)
y_data_2 = []  # Second plot y-values (average of multiple random values)

# Layout of the Dash app
app.layout = html.Div([
    dcc.Graph(id='real-time-plot-1'),  # First plot
    dcc.Graph(id='real-time-plot-2'),  # Second plot
    dcc.Interval(
        id='interval-component',
        interval=500,  # Time in milliseconds (500 ms = 0.5 seconds)
        n_intervals=0  # Initial count of intervals
    )
])

# Update the plots at each interval
@app.callback(
    [Output('real-time-plot-1', 'figure'),
     Output('real-time-plot-2', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_plot(n_intervals):
    # First plot: generate a random value between 0 and 100
    random_value_1 = random.randint(0, 100)
    
    # Append the new value to the data lists
    x_data.append(n_intervals)
    y_data_1.append(random_value_1)
    
    # Second plot: generate between 1 to 5 random y-values and calculate the average
    random_values_2 = [random.randint(0, 100) for _ in range(random.randint(1, 5))]
    avg_value_2 = sum(random_values_2) / len(random_values_2)  # Calculate the average
    
    # Append the average value for the second plot
    y_data_2.append(avg_value_2)
    
    # Create the first plot with the random value
    figure_1 = {
        'data': [go.Scatter(x=x_data, y=y_data_1, mode='lines+markers')],
        'layout': go.Layout(
            title="Real-Time Random Value Generation (Plot 1)",
            xaxis={'title': 'Time (seconds)'},
            yaxis={'title': 'Random Value'},
            showlegend=False
        )
    }

    # Create the second plot with the average value
    figure_2 = {
        'data': [go.Scatter(x=x_data, y=y_data_2, mode='lines+markers')],
        'layout': go.Layout(
            title="Average of Random Values (Plot 2)",
            xaxis={'title': 'Time (seconds)'},
            yaxis={'title': 'Average Random Value'},
            showlegend=False
        )
    }

    return figure_1, figure_2

# Run the Dash app
if __name__ == '__main__':
    # Start the server and open the browser
    app.run_server(debug=True, use_reloader=False, port=8050)
    webbrowser.open("http://127.0.0.1:8050")  # Open the app in the browser
