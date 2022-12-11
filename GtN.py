"""
Guess the number game.
"""
import sys
import random
from time import sleep
sys.dont_write_bytecode = True
try:
    import pyPgs
except ModuleNotFoundError: ## If pyPgs.py does not exist, catch the exception and print instead.
    print('Unable to find required script modules. Please verify they exist.')
    sleep(3)
    quit()

def gtn_game():
    """
    The game itself.
    """
    print('Welcome to the Guess the Number game!')
    sleep(2)
    print('I will choose a number between 1 and 20. Then, you try and guess it!')
    sleep(1)
    print("Ready? Let's go!")
    sleep(2)
    pyPgs.cls()

    while True:
        print('Choosing a number...')
        num = random.randint(1, 20)
        sleep(2)
        try:
            while True:
                print("Your Choice?")
                print()
                ans = int(input("> "))
                if ans <= 0 or ans > 20:
                    print("That's not a valid number!")
                    sleep(2)
                    pyPgs.cls()
                    continue
                if ans == num:
                    print('Correct!')
                    sleep(3)
                    quit()
                if ans < num:
                    print('Higher!')
                    sleep(2)
                    pyPgs.cls()
                    continue
                if ans > num:
                    print("Lower!")
                    sleep(2)
                    pyPgs.cls()
                    continue
        except ValueError:
            print("That's not a number!")
            sleep(3)
            pyPgs.cls()
            continue



gtn_game()
