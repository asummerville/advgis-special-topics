from dash import Dash, dcc, html, Input, Output, State

app = Dash(__name__)

app.layout = html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit')
])


@app.callback(
    Output('container-button-basic', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value')
)
def update_output(value, n_clicks):
    return 'The input value was "{}"'.format(
        value
    )


if __name__ == '__main__':
    app.run_server(debug=True)