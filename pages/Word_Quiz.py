import nltk
nltk.download('words')
from nltk.corpus import words
english_words = words.words('en')
import dash
from dash import Input, Output, State, callback, dcc, html
from PIL import Image
import random 
from user_agents import parse
from flask import request
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/Word_Quiz')


ASL_dict = {
'A' : Image.open("Letters/A.jpg"), 'B' : Image.open("Letters/B.jpg"), 'C' : Image.open("Letters/C.jpg"),
'D' : Image.open("Letters/D.jpg"), 'E' : Image.open("Letters/E.jpg"), 'F' : Image.open("Letters/F.jpg"),
'G' : Image.open("Letters/G.jpg"), 'H' : Image.open("Letters/H.jpg"), 'I' : Image.open("Letters/I.jpg"), 
'J' : Image.open("Letters/J.jpg"), 'K' : Image.open("Letters/K.jpg"), 'L' : Image.open("Letters/L.jpg"),
'M' : Image.open("Letters/M.jpg"), 'N' : Image.open("Letters/N.jpg"), 'O' : Image.open("Letters/O.jpg"),
'P' : Image.open("Letters/P.jpg"), 'Q' : Image.open("Letters/Q.jpg"), 'R' : Image.open("Letters/R.jpg"),
'S' : Image.open("Letters/S.jpg"), 'T' : Image.open("Letters/T.jpg"), 'U' : Image.open("Letters/U.jpg"),
'V' : Image.open("Letters/V.jpg"), 'W' : Image.open("Letters/W.jpg"), 'X' : Image.open("Letters/X.jpg"),
'Y' : Image.open("Letters/Y.jpg"), 'Z' : Image.open("Letters/Z.jpg")
}  # dictionary containing images of ASL letters

word_images = [ASL_dict[c] for c in 'ASL']

def word_image_maker(words_img, size):
    images = []
    img_div = html.Div(children=images, style={"height":f"{size}"})
    for img in words_img:
        images.append(html.Img(src = img, style={"height":f"{size}", "width":f"{size}"}))
    return img_div


layout = html.Div(
    style={"text-align": "center"},
    children=[
    dcc.Location(id='url_2', refresh=False),
        html.Div([
            html.H1("ASL Word Quiz"),
            dbc.Button(
                "Click here to collapse the introduction",
                id="collapse-button-word",
                className="mb-3",
                color="primary",
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(
                        "Welcome to the ASL Word Quiz! Are you ready to test your American Sign Language knowledge? You have 3 guesses to figure out what ASL word is being represented by the images shown on the page. Simply enter your guess in the input field and click 'Submit'. If you guess correctly, you'll win the game! If you're having trouble, don't worry. You can play again as many times as you want. Good luck and have fun!"
                        ,style={'font-size': '20px'})
                ),
                id="collapse-word",
                is_open = True
            ),
            html.Br(),
            dcc.Input(id="word_guess", type="text", placeholder="Enter your guess", value="", autoComplete="off"),
            html.Button("Submit", id="submit-btn_word"),
            html.Br(),
            html.P(children = '', id="result_word", style = {"margin-bottom":"40px"}),
            html.Div(children = [], id = "word_image")
        ])
    ]
)


# Callback to toggle the collapse and change button text
@callback(
    [dash.dependencies.Output("collapse-word", "is_open"),
     dash.dependencies.Output("collapse-button-word", "children")],
    [dash.dependencies.Input("collapse-button-word", "n_clicks")],
    [dash.dependencies.State("collapse-word", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open, "Click here to {} the introduction".format("expand" if is_open else "collapse")
    return is_open, "Click here to {} the introduction".format("collapse" if is_open else "expand")


def generate_new_word():
    while(True):
        word = random.choice(english_words).upper()
        if(11 > len(word) > 2):break
        else: continue
    return word

remaining_guesses = 3
current_word = 'ASL'
current_image = ''

@callback(
    [Output("word_image", "children"),  Output("submit-btn_word", "children"), Output("result_word", "children"), Output("word_guess", "value")],
    [Input("submit-btn_word", "n_clicks"), Input("submit-btn_word", "children"), Input('url_2', 'pathname')],
    [State("word_guess", "value")], 
)
def update_asl_letter(n_clicks, label, pathname, guess):
    global current_word, current_image, remaining_guesses
    user_agent = parse(request.headers['User-Agent'])
    image_size = "60px" if not user_agent.is_mobile else "40px"
    if n_clicks:
        if label == "Play Again":
            remaining_guesses = 3
            word = generate_new_word()
            current_word = word
            word_images = [ASL_dict[c] for c in current_word]
            current_image = word_image_maker(word_images, image_size)
            return current_image, "Submit", "", ""
        
        else:
            
            if(guess.upper() == current_word.upper()):
                remaining_guesses = 3
                return current_image, "Play Again", f"Correct! The ASL word above is {current_word.upper()}.", ""
            
            else:
                remaining_guesses -= 1
                if(remaining_guesses == 0):
                    remaining_guesses = 3
                    return current_image, "Play Again", f"Sorry, you have run out of guesses. The ASL word was {current_word.upper()}", ""
                if(guess.upper() != current_word.upper()):
                    return current_image, "Submit", f"Sorry, that is not correct. You have {remaining_guesses} guesses remaining.", ""

    else:
        word_images = [ASL_dict[c] for c in current_word]
        current_image = word_image_maker(word_images, image_size)
        return current_image, "Submit", "", ""