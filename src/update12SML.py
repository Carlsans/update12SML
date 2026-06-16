import json
import os
import time
from datetime import datetime

import notify2
from pathlib import Path


# Playwright doit être installé
# You need to install playwright
# https://playwright.dev/python/docs/intro
from playwright.sync_api import sync_playwright
dir_path = os.path.dirname(os.path.realpath(__file__))
# WordPress credentials and URL
WORDPRESS_URL = "https://meetings.aa-quebec.org/wp-login.php"
MEETING_IMPORT_PAGE_URL = "https://meetings.aa-quebec.org/wp-admin/edit.php?post_type=tsml_meeting&page=import"
with open(dir_path + "/credentials.json", "r") as myfile:
    credentials = json.load(myfile)
if credentials['USERNAME'] == '':
    raise Exception('Please enter a username in /src/credentials.json')
if credentials['PASSWORD'] == '':
    raise Exception('Please enter a password in /src/credentials.json')

USERNAME = credentials['USERNAME']
PASSWORD = credentials["PASSWORD"]
SOURCE_COUNT = 4
time_before_next_download = 120

def set_program_state(state: str,setdetailed=False):
    # Gets the absolute directory of the current script
    file_dir = Path(__file__).parents[1].resolve()
    file_dir = file_dir/ "logging/program_state.txt"
    print(file_dir)

    with open(file_dir, "w") as file:
        file.write(state)
    if setdetailed:
        set_program_state_detailed(state)
def set_program_state_detailed(state: str):
    file_dir = Path(__file__).parents[1].resolve()
    file_dir = file_dir / "logging/program_state_detailed.txt"
    print(file_dir)
    with open(file_dir, "w") as file:
        file.write(state)
def notify(summary,message):
    notify2.init("12SML Updater")
    n = notify2.Notification(summary, message)
    n.show()
def process_exception(e,explanation= "",stop_program=True):
    # Catches standard errors and lets you inspect them
    print(f"An error occurred: {explanation} {e}")
    print(f"Error type: {type(e)}")

    # Get only the error
    if explanation == "":
        summary = f"{type(e)}".rsplit('.', 1)[-1][0:-2]
    else:
        summary = explanation
    set_program_state(summary)
    detailed = f"An error occurred: {e}\nError type: {type(e)}"
    set_program_state_detailed(detailed)
    notify(summary,detailed)

    if stop_program:
        exit(1)
def is_running_from_cron() -> bool:
    return os.environ.get("RUNNING_FROM_CRON") == "1"

def wordpress_login_and_execute():
    set_program_state("Launching playwright...",setdetailed=True)
    with sync_playwright() as p:
        # Lance Firefox, Launch Firefox
        browser = p.firefox.launch(headless=is_running_from_cron())  # Si on est en cron, on roule headless sinon le programme plante

        context = browser.new_context()
        page = context.new_page()

        # Va à la page de login, goto the login page
        try:
            page.goto(WORDPRESS_URL)
        except Exception as e:
            process_exception(e,explanation="Can't open wordpress URL : " + WORDPRESS_URL)
        try:
            # Entre le login et clique le bouton, Enter login credentials and click the button
            page.fill("#user_login", USERNAME)   # ID of username input
            page.fill("#user_pass", PASSWORD)    # ID of password input
            page.click("#wp-submit")             # ID of login button
        except Exception as e:
            process_exception(e,explanation="Can't enter and submit password and username/bad URL")

        # Attend que la barre d'administration apparaîsse
        # Wait for the dashboard page to load (Ensure correct selector for successful login)
        try:
            page.wait_for_selector("#wpadminbar")  # Admin bar appears after successful login
        except Exception as e:
            process_exception(e,explanation="Can't access admin bar")


        print("Loggé avec succès ! Successful login !")

        # Update les meetings, Update meetings ::
        # Ouvre la page de d'importation des réunion Open import meeting page
        try:
            page.goto(MEETING_IMPORT_PAGE_URL)
            time.sleep(30)
        except Exception as e:
            process_exception(e,explanation="Error accessing the tsml meeting page")
        # Si vous avec des problemes de timeout, augmenter la valeur suivante.
        # If you have timeout issues, use a bigger value. Bigger meeting list take more time..
        page.set_default_timeout(120000)
        # Clique sur les boutons les un après les autres avec une pause entre chaque
        # Click on meeting import button with a pause between each click.
        for i in range(SOURCE_COUNT):
            print("Updating",str(i+1)," source")
            # Clique les boutons les uns après les autres. Aidé de chatgpt.
            # Click on each button one after the other. Chatgpt is good here.
            try:
                page.click('tr:nth-of-type(' + str(i+1) + ') input[type="submit"][value="Refresh"]')
                time.sleep(time_before_next_download)
            except Exception as e:
                process_exception(e, explanation="Error clicking submit button #"+str(i+1))

# Execute the automation
try:
    wordpress_login_and_execute()
except Exception as e:
    print("Unknown error !")
    process_exception(e)

now = datetime.now()
formatted_time = now.strftime("Le %d %B à %H:%M:%S")
set_program_state("Program Succeeded "+ formatted_time, setdetailed=True)
notify("Mise à jour TSML Succès",formatted_time)

