from Scratch_Library_Main.Scratch_Library_Main._scratch_website_lib import Studio, MANUAL_PATH

# FUNCTIONS

def save_username_file(usernames):
    with open(MANUAL_PATH, "w") as f:
        for username in usernames:
            f.write(username + "\n")

# MAIN

def start_ui():
    # Ask for the studio ID and validate it
    studio_id = input("Enter the studio ID: ").strip()
    if not studio_id.isdigit():
        print("Invalid studio ID")
        return
    
    studio_id = int(studio_id)
    
    # Initalize the studio object
    studio = Studio(studio_id)

    # Get the names from the list
    with open(MANUAL_PATH, "r") as f:
        usernames = f.read().splitlines()

    usernames = [username.strip() for username in usernames if username.strip()]
    usernames = list(set(usernames))

    # Invite the users to the studio
    studio.invite_curators(usernames, func = save_username_file)

    # Print a message
    print("Complete! Invited {} users.".format(len(usernames)))

    input("\nPress [ENTER] to continue... ")