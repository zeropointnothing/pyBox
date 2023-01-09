"""
Password manager.
Encrypts passwords with a KEY in order to keep them more secure.
Is now a decent replacement, due to the several layers causing the second
layer to fail completely if the key is incorrect.
"""
import sys
import os
import base64
from time import sleep
print(os.getcwd())
sys.dont_write_bytecode = True

try:
    import tedi
    import py_pgs

except ModuleNotFoundError: ## If v.py does not exist, catch the exception and print instead.
    print('Unable to find required script modules. Please verify they exist.')
    sleep(3)
    quit()

##Master password determines whether or not your passwords can be accessed.
print('Make sure to remember your password! Your passwords will be inaccessible without it!')
mas_pwd = input("Please enter Master Password: ")

def view():
    """
    Views current passwords.
    """

    try:
        ##Open passwords.zro in Read mode. using with open makes it close at the end of the block.
        with open('passwords.zro', 'r', encoding='UTF-7') as file:
            print()

            for line in file.readlines(): ##Reads every line.
                data = line.rstrip() ##Removes any \n's present.
                user, passw = data.split(" | ") ##Removes all instances of ' | '.

                ##Calls the imported function auto_endec.
                try:
                    ##Attempt to decode the password.
                    passw = py_pgs.auto_endec(passw, 'decrypt', mas_pwd)
                    base64_string =passw
                    base64_bytes = base64_string.encode("ascii")
                    sample_string_bytes = base64.b64decode(base64_bytes)
                    string = sample_string_bytes.decode("ascii")
                    passw = py_pgs.auto_endec(string, 'decrypt', mas_pwd)
                    passw = tedi.decode_zte26(passw)
                except UnicodeDecodeError:
                    passw = 'err. malformed string.'

                print(f"Username: {user} | Password: {passw}")

            print()
            input("Press Enter to continue... ")

    ##If passwords.zro does not exist, catch exception and print this instead before returning.

    except FileNotFoundError:

        print("Could not find passwords file.")
        print("Please double check that it exists, and has the proper name. (passwords.zro)")
        print()

        sleep(3)

def add():
    """
    Adds passwords.
    """
    name = input('Account name: ')
    pwd = input('Password: ')

    with open('passwords.zro', 'a', encoding='UTF-8') as file:

        pwd = tedi.encode_zte26(pwd)
        pwd = py_pgs.auto_endec(pwd, 'encrypt', mas_pwd)
        string = pwd
        string = string.encode("ascii")
        base64_bytes = base64.b64encode(string)
        base64_string = base64_bytes.decode("ascii")
        base64_string = py_pgs.auto_endec(base64_string, 'encrypt', mas_pwd)
        file.write(name + " | " + base64_string + "\n")


while True:

    tedi.cls()

    print("Would you like add a new password or view existing ones (view/add)? Press q to quit.")

    mode = input('> ').lower()

    if mode == 'q':

        quit()



    if mode == "view":

        view()

    elif mode == "add":

        add()

    else:

        print("Invalid option.")

        continue
