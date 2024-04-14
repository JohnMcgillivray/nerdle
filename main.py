from flask import Flask, request, render_template, session


from word_turd import Turdle

app = Flask(__name__)
app.secret_key = b"wawawewa"


@app.get("/")
def read_root():
    return render_template("home.html", title="home")


@app.get("/turdle/")
def turd():
    session.clear()
    return render_template("home.html", title="💩 Turdle 💩")

@app.get("/new_game/")
def new_game():
    session.clear()
    return render_template("game.html")


@app.post("/guess/")
def guess_turd():
    words = []
    if session.get("words"):
        words = session["words"]

    guess = request.form["guess"]
    guess = guess.lower()

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

    if turd.status == "guessed":
        return render_template("word_guessed.html",letters=guess, colors=color)

    session["words"] = words

    return render_template("word.html", letters=guess, colors=color)
