# Nerdle
A game like Wordle, except the computer makes your guesses as unhelpful as possible.
Similar to malicious hangman, the computer doesn't pick a word until forced to by the player's guesses. 
With each guess it will preserve the largest subset of the word list as posible, until only one word is left.

## Installation 
```
pip3 install requirements.txt
```

## Playing the game
The GUI is a webapp using flask and HTMX. You can start up the sever by running 
```
flask --app main run
```
then navigate to the URL shown. You can also play from the command line TUI, just run the word_nerd.py file.
```
./word_nerd.py
```

