from msvcrt import getch
import getpass, sys

def enterPasswd(prompt='Password: '):
    """
        Prompt for a password and masks the input.
        Returns:
            the value entered by the user.
    """

    if sys.stdin is not sys.__stdin__:
        pwd = getpass.getpass(prompt)
        return pwd
    else:
        pwd = ""
        sys.stdout.write(prompt)
        sys.stdout.flush()
        while True:
            key = ord(getch())
            if key == 13:        # Return key
                sys.stdout.write('\n')
                return pwd
                break
            if key == 8:         # Backspace key
                if len(pwd) > 0:
                    # Erases previous character.
                    sys.stdout.write('\b' + ' ' + '\b')
                    sys.stdout.flush()
                    pwd = pwd[:-1]
            else:
                # Masks user input.
                char = chr(key)
                sys.stdout.write('*')
                sys.stdout.flush()
                pwd = pwd + char

mypwd=enterPasswd()
print(mypwd)