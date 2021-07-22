import json
import random
import discord
import requests
import configfile
from urllib.parse import quote
from pydactyl import PterodactylClient
from requests.exceptions import HTTPError

"""
Creates Pterodactyl users and links their
main email with their Pterodactyl panel
user ID, and their Discord ID.

Links in json file. It's not in the `templates` directory, 
so it wont be accessable from the web page.

Make a pull request if you think anything can be improved.
"""

def create_user(discordUsername, discordEmail, discordUserID):

    # Main function #

    with open('users.json', 'r') as __userfile__:
        data = json.load(__userfile__)

    userdataHeaders = {
        "Authorization": "Bearer apikey",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    pteroclient = PterodactylClient(configfile.pteroURL, configfile.pteroAppKey)

    passwordnumber = random.randint(100, 999)
    pteroclient.user.create_user(
        username=discordUsername,
        email=discordEmail,
        first_name=discordUsername,
        last_name=discordUserID,
        password=f"changeme{passwordnumber}"
    )
    userdataURL = f'{configfile.pteroURL}api/application/users?filter[email]={discordEmail}'
    userdataURL = str(quote(userdataURL))

    userdataResponse = requests.request('GET', url=userdataURL, headers=userdataHeaders)
    userdataResponse = str(userdataResponse['data']['attributes']['id'])

    pteroclient.user.list_users(email=discordEmail)
    data[f'{discordEmail}'] = [
        userdataResponse, discordUserID
    ]

    with open('users.json', 'w') as userdatafile:
        json.dumps(data, userdatafile, indent=4)