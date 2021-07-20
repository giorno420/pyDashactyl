import json
import random
import sqlite3
import requests
import discord
import configfile
from discord.ext import commands
from pydactyl import PterodactylClient

pteroclient = PterodactylClient(configfile.pteroURL, configfile.pteroAppKey)

with open('users.json', 'r') as __userfile__:
    data = json.load(__userfile__)

def create_user(discordUsername, discordEmail, discordUserID):
    passwordnumber = random.randint(100, 999)
    pteroclient.user.create_user(
        username=discordUsername,
        email=discordEmail,
        first_name=discordUsername,
        last_name=discordUserID,
        password=f"changeme{passwordnumber}"
    )

    pteroclient.user.list_users(email=discordEmail)
    data[discordUserID] = [
        '', discordEmail
    ]
