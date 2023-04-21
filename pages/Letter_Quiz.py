import random
import dash
from dash import Input, Output, State, callback, dcc, html
from PIL import Image
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/')

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


layout = html.Div(
    style={"text-align": "center"},
    children=[
        html.Div([
            html.H1("ASL Letter Quiz"),
            dbc.Button(
                "Click here to collapse the introduction",
                id="collapse-button-letter",
                className="mb-3",
                color="primary",
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(
                        "Welcome to the ASL Letter Quiz! Are you ready to test your American Sign Language knowledge? You have 3 guesses to figure out what ASL letter is being represented by the image shown on the page. Simply enter your guess in the input field and click 'Submit'. If you guess correctly, you'll win the game! If you're having trouble, don't worry. You can play again as many times as you want. Good luck and have fun!"
                        , style={'font-size': '20px'})
                ),
                id="collapse-letter",
                is_open = True
            ),
            html.Br(),
            html.Img(src = ASL_dict["A"], id="asl-letter"),
            html.Br(),
            dcc.Input(id="guess", type="text", placeholder="Enter your guess", value="", autoComplete="off"),
            html.Button("Submit", id="submit-btn"),
            html.Br(),
            html.P(id="result")
        ])
    ]
)

# Callback to toggle the collapse and change button text
@callback(
    [dash.dependencies.Output("collapse-letter", "is_open"),
     dash.dependencies.Output("collapse-button-letter", "children")],
    [dash.dependencies.Input("collapse-button-letter", "n_clicks")],
    [dash.dependencies.State("collapse-letter", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open, "Click here to {} the introduction".format("expand" if is_open else "collapse")
    return is_open, "Click here to {} the introduction".format("collapse" if is_open else "expand")


remaining_guesses = 3
current_letter = 'A'
previous_letter = ''

def generate_new_letter():
    global previous_letter
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    while(True):
        letter = random.choice(letters)
        if(letter != previous_letter): break
        else: continue
    return letter


@callback(
    [Output("result", "children", allow_duplicate=True), Output("asl-letter", "src"), Output("submit-btn", "children"), Output("guess", "value")],
    [Input("submit-btn", "n_clicks"), Input("submit-btn", "children")],
    [State("guess", "value")],
    prevent_initial_call=True
)
def check_guess(n_clicks, label, guess = ''):
    global remaining_guesses, current_letter, previous_letter
    if n_clicks:
        if label == "Play Again":
            previous_letter = current_letter
            current_letter = generate_new_letter()
            current_image = ASL_dict[current_letter]
            return "", current_image, "Submit", ""
        else:
            if guess.upper() == current_letter:
                # Correct guess - generate new letter and update image
                remaining_guesses = 3
                return f"Correct! The ASL letter above is '{current_letter.upper()}'.", ASL_dict[current_letter], "Play Again", ""
            else:
                # Incorrect guess - prompt user to try again
                remaining_guesses -= 1
                if remaining_guesses == 0:
                    # Game over - reset guesses and generate new letter
                    remaining_guesses = 3
                    return f"Sorry, you have run out of guesses. The ASL letter was '{current_letter.upper()}'. Try again!", ASL_dict[current_letter], "Play Again", ""
                else:
                    # Incorrect guess but not game over - prompt user to try again
                    current_image = ASL_dict[current_letter]
                    return f"Sorry, that is not correct. You have {remaining_guesses} guesses remaining.", current_image, "Submit", ""
    else:
        current_image = ASL_dict[current_letter]
        return "", current_image, "Submit", ""
