from Scratch_Library_Main._scratch_website_lib import Scratcher, Studio, FOLLOWERS, NPY_PATH
import numpy as np

# MAIN

def start_ui():
    # Ask if the user wants to download followers or studio curators
    choice = input("Do you want to download followers or studio curators? (f/s): ").strip().lower()[0]

    if choice == "s":
        # Ask for the studio ID
        studio_id = input("Enter the studio ID: ").strip()
        if not studio_id.isdigit():
            print("Invalid studio ID")
            return
        
        studio_id = int(studio_id)

        # Create a scratcher object
        scratcher = Studio(studio_id)

        # Get the curators
        followers = scratcher.get_curators()

    elif choice == "f":
        # Ask for the username
        username = input("Enter the username of the scratcher to download followers from: ")

        # Create a scratcher object
        scratcher = Scratcher(username)

        # Get the followers
        followers = scratcher.get_followers_following(FOLLOWERS, )

    else:
        input("Invalid choice. Press [ENTER] to continue... ")

        return

    # Print a message
    print("\n{} followers gathered.".format(len(followers)))

    # Save the followers in a file
    np.save(NPY_PATH, followers)

    input("\nPress [ENTER] to continue... ")