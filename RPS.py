"""
Rock paper scissors. That's what it is.
"""
from time import sleep
import random
import sys
sys.dont_write_bytecode = True
try:
    import py_pgs
except ModuleNotFoundError: ## If v.py does not exist, catch the exception and print instead.
    print('Unable to find required script modules. Please verify they exist.')
    sleep(3)
    quit()




chss = [
    'rock',
    'paper',
    'scissors'
]


def play():
    """
    Looped code for playing RPS.
    """
    us_wins = 0
    ai_wins = 0
    while True:
        py_pgs.cls()
        if play_to in (us_wins, ai_wins):
            if us_wins == play_to:
                winner = 'User'
            else:
                winner = 'AI'


            print('Game Over!')
            print()
            print(f"Winner: {winner}")
            sleep(2)
            print()
            print(f"You won {us_wins} time(s) and the AI won {ai_wins} time(s).")
            print()
            print("Play again? (y/n)")
            while True:
                dummy = input('> ')
                if dummy.lower() == 'y':
                    us_wins = 0
                    ai_wins = 0
                    play()
                else:
                    quit()



        print('AI is choosing . . .')
        sleep(2)
        ai_chs = random.choice(chss)
        print()
        print('Your choice?')
        print()
        us_chs = input('> ').lower()
        if us_chs not in chss:
            print('Not an answer!')
            sleep(1)
            continue
        print()

        if us_chs == ai_chs:
            print("Tie!")
            sleep(1)
            continue
        if us_chs == 'paper' and ai_chs == 'rock':
            print('You win! [Paper beats rock!]')
            sleep(1)
            us_wins += 1
        if us_chs == 'rock' and ai_chs == 'scissors':
            print('You win! [Rock beats scissors!]')
            sleep(1)
            us_wins += 1
        if us_chs == 'scissors' and ai_chs == 'paper':
            print('You win! [Scissors beat paper!]')
            sleep(1)
            us_wins += 1
        ## If statements for AI wins.
        if ai_chs == 'paper' and us_chs == 'rock':
            print('You Lose! [Paper beats rock!]')
            sleep(1)
            ai_wins += 1
        if ai_chs == 'rock' and us_chs == 'scissors':
            print('You Lose! [Rock beats scissors!]')
            sleep(1)
            ai_wins += 1
        if ai_chs == 'scissors' and us_chs == 'paper':
            print('You Lose! [Scissors beat paper!]')
            sleep(1)
            ai_wins += 1


print("Welcome to Rock, Paper, Scissors!")
print("What would you like to play to?")
print()
while True:
    try:
        play_to = int(input("> "))
        py_pgs.cls()
        break
    except ValueError:
        print("That's not a number!")
        sleep(2)
        continue

print(f"Let's see how well you do out of {play_to}! >:D")
sleep(2)
print()
print("Ready?")
print()

while True:
    dummy = input('> ')
    if dummy.lower() != 'y':
        continue
    break
play()
