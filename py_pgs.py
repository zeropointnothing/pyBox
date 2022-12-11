"""
Contains code for many, newer projects.

.cls

.auto_endec
"""
import os


# Every possible symbol that can be encrypted/decrypted:
# auto_endec
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def auto_endec(string, mode, key):
    """
    py_pgs.auto_endec(string=[string], mode=[encrypt/decrypt], key=[decryption/encryption key])

    Automatically encrypt or decrypt the message using the supplied key.
    """
    translated = []  # Stores the encrypted/decrypted message string.
    key_index = 0
    key = key.upper()

    for symbol in string:  # Loop through each character in message.
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
    py_pgs.cls()

    Clears the screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
