import json
import time
# Playwright doit être installé
# You need to install playwright
# https://playwright.dev/python/docs/intro
from playwright.sync_api import sync_playwright

# WordPress credentials and URL
WORDPRESS_URL = "https://meetings.aa-quebec.org/wp-login.php"
with open("credentials.json", "r") as myfile:
    credentials = json.load(myfile)
if credentials['USERNAME'] == '':
    raise Exception('Please enter a username in /src/credentials.json')
if credentials['PASSWORD'] == '':
    raise Exception('Please enter a password in /src/credentials.json')

USERNAME = credentials['USERNAME']
PASSWORD = credentials["PASSWORD"]
SOURCE_COUNT = 4
time_before_next_download = 120
def wordpress_login_and_execute():
    with sync_playwright() as p:
        # Lance Firefox, Launch Firefox
        browser = p.firefox.launch(headless=True)  # Mettre à Faux pour les tests et Vrai si appellé par une job cron(sinon bug !)
        context = browser.new_context()
        page = context.new_page()

        # Va à la page de login, goto the login page
        page.goto(WORDPRESS_URL)

        # Entre le login et clique le bouton, Enter login credentials and click the button
        page.fill("#user_login", USERNAME)   # ID of username input
        page.fill("#user_pass", PASSWORD)    # ID of password input
        page.click("#wp-submit")             # ID of login button

        # Attend que la barre d'administration apparaîsse
        # Wait for the dashboard page to load (Ensure correct selector for successful login)
        page.wait_for_selector("#wpadminbar")  # Admin bar appears after successful login

        print("Loggé avec succès ! Successful login !")

        # Update les meetings, Update meetings ::
        # Ouvre la page de d'importation des réunion Open import meeting page
        page.goto("https://meetings.aa-quebec.org/wp-admin/edit.php?post_type=tsml_meeting&page=import")
        # Clique sur les boutons les un après les autres avec une pause entre chaque
        # Click on meeting import button with a pause between each click.
        for i in range(SOURCE_COUNT):
            print("Updating",str(i+1)," source")
            # Clique les boutons les uns après les autres. Aidé de chatgpt.
            # Click on each button one after the other. Chatgpt is good here.
            page.click('tr:nth-of-type(' + str(i+1) + ') input[type="submit"][value="Refresh"]')
            time.sleep(time_before_next_download)
# Execute the automation
wordpress_login_and_execute()