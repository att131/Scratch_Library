from Scratch_Library_main.Scratch_Library_main._scratch_website_lib import Studio, NAMES_PATH

# FUNCTIONS

def save_username_file(usernames):
    with open(NAMES_PATH, "w") as f:
        f.write("\n\n".join(usernames))

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
    with open(NAMES_PATH, "r") as f:
        usernames = f.read().splitlines()

    usernames = [username.strip() for username in usernames if username.strip()]
    usernames = list(set(usernames))

    # Invite the users to the studio
    studio.invite_curators(usernames, func = save_username_file)

    # Print a message
    print("Complete! Invited {} users.".format(len(usernames)))

    input("\nPress [ENTER] to continue... ")
