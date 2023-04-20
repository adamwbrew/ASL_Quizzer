import pandas as pd
import time
import dash
from dash import Input, Output, State, callback, dcc, html
import dash_bootstrap_components as dbc
from PIL import Image
import random 
from user_agents import parse
from flask import request

dash.register_page(__name__, path='/ASL_Decoder_Competition')


ASL_dict = {
'A' : Image.open("Letters/A.jpg"), 'B' : Image.open("Letters/B.jpg"), 'C' : Image.open("Letters/C.jpg"),
'D' : Image.open("Letters/D.jpg"), 'E' : Image.open("Letters/E.jpg"), 'F' : Image.open("Letters/F.jpg"),
'G' : Image.open("Letters/G.jpg"), 'H' : Image.open("Letters/H.jpg"), 'I' : Image.open("Letters/I.jpg"), 
'J' : Image.open("Letters/J.jpg"), 'K' : Image.open("Letters/K.jpg"), 'L' : Image.open("Letters/L.jpg"),
'M' : Image.open("Letters/M.jpg"), 'N' : Image.open("Letters/N.jpg"), 'O' : Image.open("Letters/O.jpg"),
'P' : Image.open("Letters/P.jpg"), 'Q' : Image.open("Letters/Q.jpg"), 'R' : Image.open("Letters/R.jpg"),
'S' : Image.open("Letters/S.jpg"), 'T' : Image.open("Letters/T.jpg"), 'U' : Image.open("Letters/U.jpg"),
'V' : Image.open("Letters/V.jpg"), 'W' : Image.open("Letters/W.jpg"), 'X' : Image.open("Letters/X.jpg"),
'Y' : Image.open("Letters/Y.jpg"), 'Z' : Image.open("Letters/Z.jpg"), " " : "newline"
}  # dictionary containing images of ASL letters

comp_imgs = [ASL_dict[c] for c in 'Welcome to ASL'.upper()]

sent_df = pd.read_csv("Sentences.csv")
list_of_sentences = sent_df["Sentence"].tolist()

def comp_img_maker(words_img, size):
    images = []
    img_div = html.Div(children=images, style={"height":f"{size}"})
    for img in words_img:
        if(img == "newline"):
            images.append(html.Div(style = {"margin-bottom":"30px"}))
        else:
            images.append(html.Img(src = img, style={"height":f"{size}", "width":f"{size}"}))
    return img_div


layout = html.Div(
    style={"text-align": "center"},
    children=[
    dcc.Location(id='url_4', refresh=False),
        html.Div([
            html.H1("ASL Decoding Competion"),
            dbc.Button(
                "Click here to collapse the introduction",
                id="collapse-button",
                className="mb-3",
                color="primary",
            ),
            dbc.Collapse(
                dbc.Card(dbc.CardBody(
                        "Welcome to the ASL Decoder Competition! Are you ready to put your ASL skills to the test? In this competition, you'll have one minute to decode as many ASL sentences as you can. The more sentences you decode correctly, the more points you'll earn, and the points will be based on the number of letters in each sentence. But, be careful! If you make even one mistake in your decoded message, you won't gain any points. So, pay attention and be accurate! Good luck to all the competitors!"
                        , style={'font-size': '20px'})
                ),
                id="collapse",
                is_open = True
            ),
            html.Br(),
            html.P(id="best_score", style={"textAlign":"left"}),
            html.P(id="points", style={"textAlign":"left"}),
            html.P(id = "timer"),
            dcc.Input(id="comp_guess", type="text", placeholder="Enter your guess", value="", autoComplete="off"),
            html.Button("Start", id="submit-btn-comp"),
            html.Br(),
            html.P(children = '', id="result_comp", style = {"margin-bottom":"40px"}),
            html.Div(children = [], id = "comp_img")
        ]),
        dcc.Interval(id='comp-timer-interval',
                         interval=1000,  # update the timer every second
                         n_intervals=0),
    ]
)


# Callback to toggle the collapse and change button text
@callback(
    [dash.dependencies.Output("collapse", "is_open"),
     dash.dependencies.Output("collapse-button", "children")],
    [dash.dependencies.Input("collapse-button", "n_clicks")],
    [dash.dependencies.State("collapse", "is_open")],
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open, "Click here to {} the introduction".format("expand" if is_open else "collapse")
    return is_open, "Click here to {} the introduction".format("collapse" if is_open else "expand")


def format_timer(seconds):
    seconds %= 60
    return f"Seconds remaining: {int(round(seconds,0))}"

best = 0
time_change = 0
time_end = 60
reset_game, played = False, False
score = 0

@callback(
    Output("timer", "children"),
    [Input("submit-btn-comp", "n_clicks"), Input("submit-btn-comp", "children"), Input('comp-timer-interval', 'n_intervals')],
)
def comp_timer(n_clicks, label, interval):
    global time_end, time_change, reset_game, played
    if n_clicks:
        if label == "Start":
            played = True
            time_change = 0
            time_end = 60
            score = 0
            time_end = time.time() + time_end # update the end time
            time_change = time.time()  # reset the start time
            return format_timer(time_end - time_change)  # format the timer value and return it
        elif label == "Submit":
            time_change = time.time()  # update the start time
            if(time_change >= time_end):
                time_change = 0
                time_end = 60
                reset_game = True
                return "Times Up!"
            else:
                return format_timer(time_end - time_change)
    else:
        if label == "Start":
            time_change = 0
            time_end = 60
            score = 0
            return ""  # show an empty timer before the game starts
        else:
            time_change = time.time()
            if(time_change < time_end):
                return format_timer(time_end - time_change)  # format the timer value and return it
            else:
                time_change = 0
                time_end = 60
                reset_game = True
                return "Times Up!"  # show an empty timer after the game ends

            

def generate_new_sentence():
    option = random.choice(list_of_sentences)
    words = option.split(" ")
    sentence = []
    for word in words:
        sentence += [word.upper()]
    return ' '.join(sentence)


current_word = ''
current_image = ''


@callback(
    [Output("comp_img", "children", allow_duplicate=True),  Output("submit-btn-comp", "children", allow_duplicate=True), Output("result_comp", "children", allow_duplicate=True), Output("comp_guess", "value", allow_duplicate=True), Output("points", "children"), Output("best_score", "children")],
    [Input("submit-btn-comp", "n_clicks"), Input("submit-btn-comp", "children"), Input('url_4', 'pathname')],
    [State("comp_guess", "value")], 
    prevent_initial_call=True
)

def update_asl_letter(n_clicks, label, pathname, guess):
    global current_word, current_image, reset_game, played, score, best
    user_agent = parse(request.headers['User-Agent'])
    image_size = "60px" if not user_agent.is_mobile else "40px"
    if n_clicks:
        if label == "Play Again":
            played = False
            reset_game = False
            score = 0
            return  '', "Start", "", "", "", f"Best Score: {best}"
        if(played == True and reset_game == True):
            if(best < score):
                best = score
            return '', "Play Again", "Game Over!!", "", f"Total Score: {score}", f"Best Score: {best}"
        if(label == "Start"):
            word = generate_new_sentence()
            current_word = word
            word_images = [ASL_dict[c] for c in current_word]
            current_image = comp_img_maker(word_images, image_size)
            return current_image, "Submit", "", "", f"Current Score: {score}", f"Best Score: {best}"
        guess = ' '.join([i.upper() for i in guess.strip().split(" ")])
        if(guess == current_word):
            prev = current_word
            score += len(prev.split(" "))
            word = generate_new_sentence()
            current_word = word
            word_images = [ASL_dict[c] for c in current_word]
            current_image = comp_img_maker(word_images, image_size)
            return current_image, "Submit", f"Correct! The previous ASL sentence was {prev.upper()}.", "", f"Current Score: {score}", f"Best Score: {best}"
        else:
            prev = current_word
            word = generate_new_sentence()
            current_word = word
            word_images = [ASL_dict[c] for c in current_word]
            current_image = comp_img_maker(word_images, image_size)
            return current_image, "Submit", f"Sorry, that is not correct. The previous ASL sentence was {prev.upper()}.", "", f"Current Score: {score}", f"Best Score: {best}"

    else:
        if(played == True and reset_game == True):
            if(best < score):
                best = score
            return '', "Play Again", "Game Over!!", "", f"Total Score: {score}", f"Best Score: {best}"
        else:
            return '', "Start", "", ""