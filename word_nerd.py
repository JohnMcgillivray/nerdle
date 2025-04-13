#!/usr/bin/env python3


class Nerdle:

    def __init__(self) -> None:
        with open("wordle.txt") as f:
            self.WORD_LIST = f.readlines()
        self.WORD_LIST = [word.strip() for word in self.WORD_LIST]
        self.status = "playing"

    def guess(self, guess: str, words: list[str]) -> tuple[str, list[str]]:
        if len(guess) != 5:
            raise ValueError("Guess must be a 5-letter word!")

        guess = guess.lower()

        match_groups = {}

        if not words:
            words = self.WORD_LIST

        for word in words:
            s = self._find_matches(guess, word)
            if s not in match_groups:
                match_groups[s] = []
            match_groups[s].append(word)

        best_pattern = max(
            match_groups, key=lambda x: len(match_groups[x]) if x != guess else 0
        )

        if best_pattern == guess:
            self.status = "guessed"

        words = match_groups[best_pattern]
        return best_pattern, words

    def _find_matches(self, guess : str, word : str):
        match_string = ""
        for i in range(5):
            if guess[i] == word[i]:
                match_string += guess[i]
            elif guess[i] in word:
                amount_in_word = word.count(guess[i])
                amount_in_guess = guess.count(guess[i])
                if amount_in_word >= amount_in_guess:
                    # has at least as many occurences as guess, can be yellow
                    match_string += "+"
                else:
                    amount_correct_in_guess = 0
                    for j in range(5):
                        if guess[j] == guess[i] and guess[j] == word[j]:
                            amount_correct_in_guess += 1
                    if amount_correct_in_guess == amount_in_word:
                        # all occurences correctly guessed, show all additional as wrong
                        match_string += "-"
                    else:
                        # only show yellow for first (amount in word - amount correct in guess)
                        amount_to_show_yellow = amount_in_word - amount_correct_in_guess
                        amount_yellow = 0
                        for j in range(i):
                            if guess[j] == guess[i] and guess[j] != word[j]:
                                amount_yellow += 1
                        if amount_yellow < amount_to_show_yellow:
                            match_string += "+"
                        else:
                            match_string += "-"
            else:
                match_string += "-"
        return match_string


def main():

    nerd = Nerdle()
    words = []

    while nerd.status == "playing":
        guess = ""
        while len(guess) != 5:
            guess = input("Please enter a 5-letter word! ")

        res, words = nerd.guess(guess, words)
        print(res)

        if nerd.status == "playing":
            print(f"Words left: {len(words)}")
            if len(words) < 30:
                print("Words left: ", words)

    print("You guessed the word!")

    if input("Play again? (y/n) ").lower() in ["y", "yes"]:
        main()


if __name__ == "__main__":
    main()
