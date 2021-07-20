import random, time
import bcrypt, json
from discord.ext import commands
from pydactyl import PterodactylClient
from requests.exceptions import HTTPError
import json, time, requests, sqlite3, os, discord
from flask import Flask, g, session, render_template, redirect, url_for, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

with open('settings.json', 'r') as confg:
    settings = json.load(confg)
    discordsettings = settings["discord"]
    pterosettings = settings["pterodactyl"]

app = Flask(__name__)

app.secret_key = discordsettings["secret_key"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = discordsettings["application_id"]
app.config["DISCORD_CLIENT_SECRET"] = discordsettings["secret_key"]
app.config["DISCORD_REDIRECT_URI"] = discordsettings["redirect_uri"]
pteroapplication = PterodactylClient(pterosettings)

discord = DiscordOAuth2Session(app)

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
        return "u havent logged in :("

@app.route('/logout')
def logout():
    discord.revoke()
    return redirect(url_for('https://giornosmp.com/'))

def create_user_func(email, username):
    user = discord.fetch_user()
    url = pterosettings["url"]
    headers = {
        "Authorization": f'Bearer {pterosettings["key"]}',
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = '{"email": f"{user.email}", "username": f"{user.username}", "first_name": f"{user.username}", "last_name": f"{user.discriminator}"}'
    create_user_response = requests.post(url, data=payload, headers=headers)

@app.route('create')
@requires_authorization
def createuser():
    user = discord.fetch_user()


if __name__ == "__main__":
    app.run(debug=True)