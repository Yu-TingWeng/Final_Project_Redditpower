'''
Page for the Text Predictions
'''

import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
import sentiment_analysis as sa

dash.register_page(__name__)


layout = html.Div([
    dbc.Row([
        dbc.Col(html.H1("Text Classification App"), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Textarea(id='input_text', placeholder='Enter text to classify...', rows=4, style={'width': '100%'}), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.Button('Classify', id='classify_button', n_clicks=0), width=12),
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='output_classification'), width=12),
    ]),
]) 


@callback(
    Output('output_classification', 'children'),
    [Input('classify_button', 'n_clicks')],
    [State('input_text', 'value')]
)
def classify_text(n_clicks, input_text):
    if n_clicks > 0 and input_text:
        # Transform the input text using the same vectorizer
        input_tfidf = sa.tfidf_vectorizer.transform([input_text])

        # Use the pre-trained model to predict the sentiment
        prediction = sa.svm_model.predict(input_tfidf)[0]

        return f'Predicted Sentiment: {prediction}'

    return ''


