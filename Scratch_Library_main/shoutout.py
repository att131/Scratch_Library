from Scratch_Library_main.Scratch_Library_main._scratch_website_lib import Studio, Scratcher, WEEKLY_SHOUTOUT_STUDIO_ID

from datetime import datetime, timedelta
import random
import pyperclip

# VARIABLES

USERNAME_TO_FOLLOW = "Crazy-Coderz"

MESSAGE = "Congratulations {}, you have been selected as the shoutout for the 'Weekly Shoutout' studio! If there is any text that you want to add under your username at the top of the studio description then reply to this comment with what you want it to say. It can be anything; a thank you, an advertisement, or simply saying hello to your fellow scratchers! You will remain the shoutout until {} when another user replaces you. I hope you enjoy your time as the shoutout!"

# FUNCTIONS

def get_saturday_date():
    # Get today's date
    today = datetime.today()

    # Calculate the number of days until the next Saturday
    days_until_saturday = (5 - today.weekday()) % 7

    # Find the next Saturday's date
    next_saturday = today + timedelta(days=days_until_saturday)

    return str(next_saturday.strftime("%A, %B %d, %Y")).strip(", 2025").strip(", 2026").strip(", 2027")

# MAIN

def start_ui():
    # Print a message
    print("Getting curators...\nThis might take a few minutes...")

    # Initalize the studio object
    studio = Studio(WEEKLY_SHOUTOUT_STUDIO_ID)

    # Get the curators from the studio
    curators = studio.get_curators()

    print("Curators found!\nSearching for someone following {}...".format(USERNAME_TO_FOLLOW))

    # Pick a random curator, check if they are following Crazy-Coderz
    while True:
        curator = random.choice(curators)

        try:
            if Scratcher(curator).is_following(USERNAME_TO_FOLLOW):
                print("Potential Shoutout: {}... Following Crazy-Coderz!".format(curator))
                break
            else:
                print("Potential Shoutout: {}... Not following Crazy-Coderz".format(curator))
        except:
            print("Failed to connect to: {}\nRetrying...".format(curator))
            continue

    # Print the curator
    print("\nTotal number of curators: {}".format(len(curators)))
    print("Weekly shoutout: {}".format(curator))

    print()

    # Print the formatted follower message
    message = MESSAGE.format(curator, get_saturday_date())

    print(message)

    # Ask if the user wants to copy the message
    copy_message = input("\nDo you want to copy the message to clipboard? (y/n): ").strip().lower()[0]

    if copy_message == "y":
        # Copy the message to the clipboard
        pyperclip.copy(message)
        print("Message copied to clipboard!")
