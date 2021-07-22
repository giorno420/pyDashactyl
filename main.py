import os
import sys
import api
import json
import time
import random
import bcrypt
import sqlite3
import requests
import discord
from discord.ext import commands
from pydactyl import PterodactylClient
from requests.exceptions import HTTPError
from flask import Flask, g, session, render_template, redirect, url_for, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized


app = Flask(__name__)

app.secret_key = api.configfile.discordsettings["secret_key"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = api.configfile.discordsettings["application_id"]
app.config["DISCORD_CLIENT_SECRET"] = api.configfile.discordsettings["secret_key"]
app.config["DISCORD_REDIRECT_URI"] = api.configfile.discordsettings["redirect_uri"]
pteroapplication = PterodactylClient(api.configfile.pteroURL, api.configfile.pteroAppKey)

discord = DiscordOAuth2Session(app)

def registerlogin(discordUUID):
    exec(f'discordUser_{discordUUID} = True')
@app.route('/callback')
def callback():
    discord.callback()
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return discord.create_session()

@app.route('/')
def index():
    if discord.authorized:
        return "authorized"
    elif not discord.authorized:
        return "u havent logged in <a href=\"/login\">click here to login</a>"

@app.route('/logout')
def logout():
    discord.revoke()
    return redirect(url_for('https://giornosmp.com/'))

@app.route('create')
@requires_authorization
def createuser():
    user = discord.fetch_user()
    if user.email in api.configfile.users:
        return "<script>alert('you already have an account lmao')</script><meta http-equiv=\"refresh\" content=\"0; URL='/'\" />"
    elif user.email not in api.configfile.users:
        api.userdata.create_user(user.username, user.email, user.id)
    return redirect(url_for('index'))
    

if __name__ == "__main__":
    app.run(debug=True)
