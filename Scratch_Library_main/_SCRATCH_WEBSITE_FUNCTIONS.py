from Scratch_Library_main.Scratch_Library_main.shoutout import start_ui as shoutout_ui
from Scratch_Library_main.Scratch_Library_main.invite_to_studio_manual import start_ui as invite_to_studio_ui
from Scratch_Library_main.Scratch_Library_main.download_usernames import start_ui as download_usernames_ui
from Scratch_Library_main.Scratch_Library_main.lucky_studio_update import start_ui as lucky_studio_update_ui
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
E = "e"

code_to_function = {
    A: lucky_studio_update_ui,
    B: invite_to_studio_ui,
    C: shoutout_ui,
    D: scroll_through_curators_ui,
    E: download_usernames_ui,
}

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

A) Update the Luck Leaderboard.
B) Invite curators from the notepad.
C) Update the Weekly Shoutout.
D) Scroll through curators list.
E) Automatically download usernames.

""")

    # Get the input from the user
    choice = input("Enter your choice: ").strip().lower()

    # Check if the choice is valid
    if choice not in code_to_function:
        print("Invalid choice")
        return

    # Call the function associated with the choice
    clear()
    code_to_function[choice]()

if __name__ == "__main__":
    while True:
        main()
