from Scratch_Library_main.Scratch_Library_main._scratch_website_lib import copy_luck_studio_update

# MAIN

def start_ui():
    error = copy_luck_studio_update()

    if error:
        print("Error: {}".format(error))
    else:
        print("Complete!")
