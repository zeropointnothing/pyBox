"""
Play a game of hangman.
"""
from time import sleep
import sys
import random
sys.dont_write_bytecode = True
try:
    import py_pgs
except ModuleNotFoundError: ## If py_pgs.py does not exist, catch the exception and print instead.
    print('Unable to find required script modules. Please verify they exist.')
    sleep(3)
    quit()

cor = []
inc = []
STRIKES = 0

words = [
    "pizza",
    "bread",
    "spiderman"
]

print("Welcome to Hangman!")
sleep(2)
py_pgs.cls()
print("Choosing a word...")
sleep(3)
word = random.choice(words)
py_pgs.cls()

print(word)
word_len = len(word)
GRID = '_'
for i in range(word_len - 1):
    GRID = GRID + ' _'

while True:
    print(f"The word is {len(word)} letters long.")
    print()
    print(GRID)
    print()
    ans = input("> ")

	# If the guessed letter is in the word, and it hasn't been guessed yet by the player,
    # then update the
	# GRID by placing this letter in the appropriate empty spaces on the GRID
    if len(ans) < 2:
        if ans in word.lower() and not(ans in cor):
            if not ans == '':
                cor.append(ans)
                GRID = word
                for letter in word:
                    if (not (letter.lower() in word) or not(letter.lower() in cor)) and letter != '':
                        GRID = GRID.replace(letter, ' _ ')

                if GRID == word:
                    GAME_WON = True
                else:
                    print(f"Nice! {ans.upper()} is in the word. Try another letter.")
            else:
                print("You must guess with one letter!")
                continue
        elif ans in cor:
            # This letter has already been guessed.
            print(f"You've already guessed {ans.upper()}. Try another letter.")
        else:
            # Wrong letter!
            cor.append(ans)
            STRIKES = STRIKES + 1
            print(f'{ans.upper()} is not in the word! Try another letter.')
    else:
        print("Please only guess with one letter.")
        sleep(3)
        py_pgs.cls()





