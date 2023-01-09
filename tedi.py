"""
[tEDI] - Text Edit

Python Module for multiple text based commands.
"""
from time import sleep
import random
import ast
import base64
import os

LWRCASE = 'abcdefghijklmnopqrstuvwxyz'
UPRCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '1234567890'
PUNCT = ['!','@','#','$','%','^','&','*','(',')','_',
'-','=','+','~','{',' ','}','|',':',';',"'",'<',',','>','.','/','?',]

class EmptyInp(Exception):
    """
    An argument was empty
    """
    def __init__(self, message="An argument was empty."):
        self.message = message
        super().__init__(self.message)

def encode_zte26(string: str) -> str:
    """
    Text encoder. Uses several methods combined to encode your text using
    a randomly generated key to prevent decryption from anything but this tool.
    (of course, you can strip this string of it's key to prevent that)

    Simply provide a string, and it will do the rest.
    """
    ## Generate the random KEY.
    key = ''.join(random.sample(UPRCASE, 5))
    ## Get rid of any line breaks as they interfere with the decoding process.
    string = string.replace('\n', '')

    ## Reverse the string, replace spaces with '_:-', encrypt the message with the key,
    ## then scramble the key before attaching it to the string.
    tmp = reverse(string)
    tmp = tmp.replace(' ', '_:-')
    output = _encrypt_message(tmp, key)
    key = _encrypt_message(key, 'potter')

    output = output + ';>;' + key

    return output

def decode_zte26(string: str) -> str:
    """
    Decodes a string.
    """
    key = "null"

    string = string.replace('\n', '')

    ## Detach the Key from the string, unscramble it, then reverse the encryption process.
    #try:
    string, key = string.split(";>;")
    #except K:
    #    pass
    key = _decrypt_message(key, 'potter')

    output = _decrypt_message(string, key)
    output = output.replace('_:-', ' ')
    output = reverse(output)

    return output

def txt_import(file: str, exclude='') -> str:
    """
    Imports a file and returns it's contents.

    The contents must be formatted in a Python like manner before being imported.

    Ex: Strings = '[string]', Dictionarys = ({[Dictionary1]}, {[Dictionary2]}) etc |
    Lines starting with # will be ignored and trying to import a Python script with this function
    will cause errors.

    Use the 'exclude' arguement to remove unwanted text. (CASE SENSITIVE.)
    """
    try:
        with open (file, 'r', encoding='UTF-8') as fnme:
            output = fnme.read()
            if exclude != '':
                for _ in output:
                    output = output.replace(exclude, '')
    except FileNotFoundError:
        print("[tEDI - Could not import. File does not exist.]")
        sleep(1.2)
        print("Verify that the requested file is spelled correctly and exists in the location given.")
        sleep(1)
        quit()

    try:
        output = ast.literal_eval(output)
    except:
        ## If there is an error in the data retrieval process, display a message before
        ## showing the exception.
        print("[tEDI] - Unable to retrieve data.")
        sleep(1.3)
        print("[tEDI] - Error was caused by the following Exception: ")
        print()
        sleep(2)
        raise

    return output

def contains(string: str, cnt: str, bol=False) -> int | bool:
    """
    Takes a input String and returns an integer based on how many times
    that character appeared in the input.

    Also returns a Bool value of True or False if the character is in the input.
    (set 'bool' to True)
    """
    num = 0
    cont = False

    if cnt == '':
        raise EmptyInp

    #For every occurance of the selected
    #character, add 1 to 'num' and set 'cont' to True.
    for char in string:
        if char == cnt:
            num += 1
            cont = True
    if bol is True:
        return cont
    return num

def reverse(string: str) -> str:
    """
    Reverses a string.
    """

    output = ""
    for char in string:
        output = char + output
    return output


def evr_other(string: str) -> str:
    """
    Capitalizes every other letter in a string.
    """
    cap = True
    output = ""
    ## makes all characters lowercase so they can be flip-flopped
    string = string.lower()

    #Flip flops between True and False.
    #If 'cap' is true, capitalize the letter and set 'cap' to False.
    #If it is not, set 'cap' to True and move on
    for char in string:
        if cap is True:
            output = output + char.capitalize()
            cap = False
        else:
            output = output + char
            cap = True
    return output

def one_word(string: str) -> str:
    """
    Remove all spaces from strings, making it one word.
    """
    # Simply remove all spaces in 'string'.
    string = string.replace(' ', '')
    return string

def is_ev_od(inp: int, evod='even') -> bool:
    """
    Returns a bool value if the input is either Even or Odd
    (chosen by the user, but will default to even.)
    """
    if (inp%2) == 0:
        if evod.lower() == 'even':
            return True
        else:
            return False
    else:
        if evod.lower() == 'odd':
            return True
        else:
            return False

# Every possible symbol that can be encrypted/decrypted:
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'




def _encrypt_message(message, key):
    """
    INTERNAL FUNCTION
    """
    return _translate_message(message, key, 'encrypt')


def _decrypt_message(message, key):
    """
    INTERNAL FUNCTION
    """
    return _translate_message(message, key, 'decrypt')


def _translate_message(message, key, mode):
    """
    INTERNAL FUNCTION
    """
    translated = []  # Stores the encrypted/decrypted message string.
    key_index = 0
    key = key.upper()

    for symbol in message:  # Loop through each character in message.
        num = LETTERS.find(symbol.upper())
        if num != -1:  # -1 means symbol.upper() was not in LETTERS.
            if mode == 'encrypt':
                # Add if encrypting:
                num += LETTERS.find(key[key_index])
            elif mode == 'decrypt':
                # Subtract if decrypting:
                num -= LETTERS.find(key[key_index])

            num %= len(LETTERS)  # Handle the potential wrap-around.

            # Add the encrypted/decrypted symbol to translated.
            if symbol.isupper():
                translated.append(LETTERS[num])
            elif symbol.islower():
                translated.append(LETTERS[num].lower())

            key_index += 1  # Move to the next letter in the key.
            if key_index == len(key):
                key_index = 0
        else:
            # Just add the symbol without encrypting/decrypting:
            translated.append(symbol)

    return ''.join(translated)

def cls():
    """
    Clears the screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def characterinsert(string, position, insertion):
    """
    Insert a character into a string.

    [TIP: The first character is at the position 0.]
    """
    length = len(string)
    if (position > length or position < 0):
        return string
    return string[:position] + insertion + string[position:]

def lst_ltr_ext(string: str, num: int) -> str:
    """
    Extends the last letter in a string to a specified amount.

    Will seek for the last letter it can find, skipping over symbols.
    """
    last = len(string) - 1
    while True:
        ## Seek for the last letter in the String.
        if string[last] in PUNCT:
            last -= 1
            continue

        stadd = string[last] * num
        string = characterinsert(string, last, stadd)
        return string

def scramble(string: str | list) -> str|list:
    """
    Scrambles a string or a list of strings.
    """

    if isinstance(string, list) is True:
        newstr = [''.join(random.sample(item, len(item))) for item in string]
    elif isinstance(string, str) is True:
        maxn = len(string)
        newstr = ''.join(random.sample(string, maxn))
    else:
        return 'error'
    return newstr

def glitch_conv(string):
    """
    Converts a string into glitchy text. (somewhat like DDLC.)
    """
    characters = 'ëçûĔŒƩǢỠɸβз'
    output = ''
    conv = False

    ## Converts the string.
    for char in string:
        ## Decides whether or not to convert the String. Favors True.
        num = random.randint(0, 5)

        if num >= 1:
            ## Yes.
            conv = True
        elif num == 0:
            ## No,
            conv = False

        ## Replace all spaces with ç.
        if char == ' ':
            char = 'ç'

        if char not in ['!', '.']:
            # Only convert character if it is not in this list.
            if conv is True:
                char = random.choice(characters)
                #print('True', char)
                output += char
            else:
                #print('False', char)
                output += char
        else:
            output += char

    return output

def glitch_gen(leng: int) -> str:
    """
    Similar to glitConv, but simply generates a string of text with a specified length.
    """
    characters = 'ëçûĔŒƩǢỠɸβз'
    output = ''

    for _ in range(0, leng):
        char = random.choice(characters)
        output += char
    return output

def b64_decode(string):
    """
    Decodes a string with Base64.
    """
    string = string.encode("ascii")
    base64_bytes = base64.b64encode(string)
    base64_string = base64_bytes.decode("ascii")
    return base64_string

def b64_encode(string):
    """
    Encodes a string with base64
    """
    string = string.encode("ascii")
    base64_bytes = base64.b64encode(string)
    base64_string = base64_bytes.decode("ascii")
    return base64_string