import dash
from dash import html, dcc

dash.register_page(__name__, path='/About')

layout = html.Div(children=[
    html.Div(children=[
        dcc.Markdown(
            '''
            Welcome to our American Sign Language (ASL) learning website! 
            
            Here, you can test your knowledge of ASL with our fun and interactive quizzes and games. If you're new to ASL, we recommend starting with the Letter Quiz, where you'll have 3 chances to guess the correct ASL letter based on the image shown. Once you're comfortable with the letters, move on to the Word Quiz, where you'll have to guess the ASL word based on the images shown. Next, try the Sentence Quiz, where you'll have to guess the ASL sentence based on the images shown. Finally, for the ultimate challenge, test your ASL skills in our Decoder Competition, where you'll have one minute to decode as many ASL sentences as you can.

            To help you along the way, we've included a chart of ASL letters and their corresponding English letters. Our quizzes and games are designed to be both fun and educational, so we hope you enjoy them and challenge yourself to improve your ASL skills. Good luck, and have fun!
            '''
        ),
        html.Br(),
        html.Div([
            html.Img(src="assets/ASL_chart.jpeg", height="500px"),
            ],
            style={'textAlign': 'center'}
        )
    ], style={'fontSize': '20px'})
])