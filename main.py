from flask import Flask, request, render_template, session


from word_turd import Turdle

app = Flask(__name__)
app.secret_key = b"wawawewa"


@app.get("/")
def read_root():
    return "Hello, World!"


@app.get("/turdle/")
def turd():
    session.clear()
    return render_template("home.html.j2")


@app.get("/new_game/")
def new_game():
    session.clear()
    session["guesses"] = 0
    return render_template("game.html")


@app.post("/guess/")
def guess_turd():

    if not session.get("words"):
        session["words"] = []
        session["guesses"] = 0

    words = session["words"]

    if len(request.form["guess"]) != 5:
        return ""

    guess = request.form["guess"]
    guess = guess.lower()

    len_words_before = len(words)

    turd = Turdle()
    answer, words = turd.guess(guess, words)

    color = []
    for x in answer:
        if x == "-":
            color.append("rgb(234, 216, 192)")
        elif x == "+":
            color.append("rgb(255, 165, 0)")
        else:
            color.append("green")

    session["guesses"] += 1

    dumbass = False

    if turd.status == "guessed":
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
            "word_guessed.html.j2", letters=guess, colors=color, flavor_text=flavor_text, dumbass=dumbass
        )

    session["words"] = words
    flavor_text = f"There {'is' if len(words) == 1 else 'are'} {len(words)} possible word{'s' if len(words) != 1 else ''} remaining."
    if session["guesses"] == 1 and len(words) > 500:
        flavor_text += f" Perhaps you should consider a different starting word."
    elif session["guesses"] == 6:
        flavor_text = "If this was Wordle, you'd be out of guesses. 🤡🤡🤡"
    elif len(words) == len_words_before:
        flavor_text = "Nice work, bozo. " + flavor_text + ".. still"
        if len_words_before == 1:
            dumbass = True
    elif len(words) == 69:
        flavor_text += " Nice."


    return render_template(
        "word.html.j2", letters=guess, colors=color, flavor_text=flavor_text,dumbass=dumbass
    )
