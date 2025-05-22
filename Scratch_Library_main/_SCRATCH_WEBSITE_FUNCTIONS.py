from Scratch_Library_main.Scratch_Library_main.shoutout import start_ui as shoutout_ui
from Scratch_Library_main.Scratch_Library_main.invite_to_studio_manual import start_ui as invite_to_studio_ui
from Scratch_Library_main.Scratch_Library_main.download_usernames import start_ui as download_usernames_ui
#from Scratch_Library_main.Scratch_Library_main.lucky_studio_update import start_ui as lucky_studio_update_ui
from Scratch_Library_main.Scratch_Library_main.scroll_through_curators import start_ui as scroll_through_curators_ui

import os

# Notes

"""
Functions:
- Pick weekly shoutout
- Invite to a studio
- Download usernames automatically
- Update the luck studio
"""

# VARIABLES

A = "a"
B = "b"
C = "c"
D = "d"
#E = "e"

code_to_function = {
    #A: lucky_studio_update_ui,
    A: invite_to_studio_ui,
    B: shoutout_ui,
    C: scroll_through_curators_ui,
    D: download_usernames_ui,
}

ERROR_PATH = "Error_Log.txt"

# FUNCTIONS

def clear():
    # Clear the screen
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# MAIN

def main():
    clear()

    print("""
Which Scratch tool would you like to use?

A) Invite Scratchers to a studio from the notepad.
B) Update the Weekly Shoutout.
C) Scroll through the entire curators list of a studio.
D) Automatically download usernames.

""")

    # Get the input from the user
    choice = input("Enter your choice: ").strip().lower()

    # Check if the choice is valid
    if choice not in code_to_function:
        print("Invalid choice")
        return

    # Call the function associated with the choice
    clear()

    while True:
        try:
            code_to_function[choice]()
            break
        except Error as e:
            print("Error, retrying...")

            # Create the file
            with file(ERROR_PATH, "w") as f:
                pass
            with file(ERROR_PATH, "a") as f:
                f.write(e)

if __name__ == "__main__":
    while True:
        main()
