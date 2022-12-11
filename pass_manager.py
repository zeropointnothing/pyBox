import sys
from time import sleep
sys.dont_write_bytecode = True
try:
    import py_pgs
except ModuleNotFoundError: ## If v.py does not exist, catch the exception and print instead.
    print('Unable to find required script modules. Please verify they exist.')
    sleep(3)
    quit()

mas_pwd = input("Please enter Master Password: ") ##Master password determines whether or not your passwords can be accessed.




def view():
    """
    Views current passwords.
    """
    try:
        with open('passwords.zro', 'r') as f: ##Open passwords.zro in Read mode. using with open makes it close at the end of the block.
            print()
            for line in f.readlines(): ##Reads every line.
                data = line.rstrip() ##Removes any \n's present.
                user, passw = data.split(" | ") ##Removes all instances of ' | '.
                passw = py_pgs.auto_endec(string=passw, mode='decrypt', key=mas_pwd) ##Calls the imported function auto_endec.
                print(f"Username: {user} | Password: {passw}")
            print()
    except FileNotFoundError: ##If passwords.zro does not exist, catch exception and print this instead before returning.
        print("Could not find any passwords. Please double check that it exists, and has the proper name. (passwords.zro)")
        print()


def add():
    """
    Adds passwords.
    """
    name = input('Account name: ')
    pwd = input('Password: ')

    with open('passwords.zro', 'a') as f:
        
        pwd = py_pgs.auto_endec(string=pwd, mode='encrypt', key=mas_pwd)
        f.write(name + " | " + pwd + "\n")


while True:
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
