from flask import Flask, request, render_template, session


from word_nerd import Nerdle 

app = Flask(__name__)
# bad, but I'm not storing any data and I don't care if someone cheats ¯\_(ツ)_/¯
app.secret_key = b"wawawewa"  


@app.get("/")
def read_root():
    return "<a href=/nerdle> try a game</a>"


@app.get("/nerdle/")
def nerd():
    session.clear()
    return render_template("home.html.j2")


@app.get("/new_game/")
def new_game():
    session.clear()
    session["guesses"] = 0
    return render_template("game.html")


@app.post("/guess/")
def guess_word():

    if not session.get("words"):
        session["words"] = []
        session["guesses"] = 0

    # don't really feel like setting up a db, just shove everything in the cookie
    words = session["words"]

    if len(request.form["guess"]) != 5:
        return ""

    guess = request.form["guess"]
    guess = guess.lower()

    len_words_before = len(words)

    nerd = Nerdle()
    # works for now, but should probably refactor to split TUI stuff out from game logic
    answer, words = nerd.guess(guess, words)

    color = []
    for x in answer:
        if x == "-":
            color.append("rgb(57, 62, 70)")
        elif x == "+":
            color.append("rgb(255, 165, 0)")
        else:
            color.append("green")

    session["guesses"] += 1


    if nerd.status == "guessed":
        flavor_text = f"You guessed the word in {session['guesses']} tries. "

        match session["guesses"]:
            case 5:
                flavor_text += "🤓🤓🤓"
            case 6 | 7 | 8 | 9:
                flavor_text += "Not bad!"
            case 10 | 11 | 12:
                flavor_text += "Don't quit your day job!"
            case 13 | 14 | 15:
                flavor_text += "🗿🗿🗿"
            case 69:
                flavor_text += "Nice."
            case _:
                flavor_text += "🤡🤡🤡"

        return render_template(
            "word_guessed.html.j2", letters=guess, colors=color, flavor_text=flavor_text
        )

    session["words"] = words
    flavor_text = f"There {'is' if len(words) == 1 else 'are'} {len(words)} possible word{'s' if len(words) != 1 else ''} remaining."
    if session["guesses"] == 1 and len(words) > 500:
        flavor_text += f" Perhaps you should consider a different starting word."
    elif session["guesses"] == 6:
        flavor_text = "If this was Wordle, you'd be out of guesses. 🤡🤡🤡"
    elif len(words) == len_words_before:
        flavor_text = "Nice work, bozo. " + flavor_text + ".. still"
    elif len(words) == 69:
        flavor_text += " Nice."


    return render_template(
        "word.html.j2", letters=guess, colors=color, flavor_text=flavor_text
    )
