"""
Password generator.
"""
import random
import sys
from time import sleep
sys.dont_write_bytecode = True

##words that can be used for the beginning portion of the password.
word_start = [
    "stupendous",
    "superb",
    "strange",
    "exotic",
    "interesting",
    "stunning",
    "super",
    "lopsided"
]
##words that can be used for the end portion of the password.
word_end = [
    "bread",
    "chicken",
    "pizza",
    "cheese",
    "tornado",
    "house",
    "kitchen",
    "butters",
    "mountain",
    "dinosaur",
    "meats",
    "burrito",
    "wacko",
    "grandpa"
]


def pass_word():
    """
    Creates five passwords using combinations of words, four random numbers,
    three exclaimation marks, and a random capital letter.
    """
    
    print ("Creating Five Passwords...")
    sleep(3)
    print()
    passnum=0
    for _ in range(0,5):
        start = random.choice(word_start) #Chooses a random value from the list.
        end = random.choice(word_end)
        ##Joins start and end together to make the word combo.
        comb = "_".join([start, end])
        num = "".join(random.sample("1234567894254936747", 4)) #Grabs characters randomly.
        char = "".join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", 1))
        output = comb + '!!!' + num + char
        passnum=passnum+1
        print("Generated Password", passnum, ": ")
        print(output)
        print()
        sleep(0.5)
    dummyvar = input("Press ENTER to Continue...")
    sys.exit()

def pass_string():
    """
    Creates five passwords using a combination of letters, numbers, and symbols.
    """
    
    pass_length = int(input("Enter Password Length:  "))
    if pass_length < 0:
        print()
        print("Password Password length cannot be Negative!")
        sleep(2)
        sys.exit()

    if pass_length==0:
        print()
        print("Please input a value.")
        sleep(2)
        sys.exit()

    if pass_length > 150:
        print()
        print("Too Long! (Why are you even trying to make a password this long?)")
        sleep(2)
        sys.exit()

    print ("Creating Five Passwords...")
    sleep(3)
    print()
    passnum = 0


    ##Creates the password.
    for _ in range(0,5):
        ##Characters that can appear in the password.
        ##The more of one that exists, the more common it will be.
        lower_case = "aaabbccddddefghiiijkllllmnoooopppqrrrrstuuuvwxxxxyz"
        upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        number = "123456789873458734587634567834867678"
        symbols = "!!!___##"
        tag = '_' + "".join(random.sample(upper_case, 1))
        ##Combines the possible characters.
        comb = symbols + lower_case + upper_case + number
        ##Takes the 'comb' variable and randomly selects characters to keep
        ##with the max amount determined by pass_length
        password = "".join(random.sample(comb, pass_length))
        password = password + tag

        passnum=passnum+1
        print ("Password" ,passnum ,": ")
        print (password)
        print()
        sleep(0.5)
    dummyvar = input("Press ENTER to close ")
    sys.exit()







##script begin -
while True:
    print("Enter password type. (word/string)")
    pass_type = input('> ').lower()

    if not pass_type in ['word', 'string']:
        print('Invalid response!')
        sleep(2)
        
    else:
        if pass_type == 'word':
            pass_word()
        if pass_type == 'string':
            pass_string()
