import json

with open('settings.json', 'r') as confg:
    settings = json.load(confg)
    discordsettings = settings["discord"]
    pterosettings = settings["pterodactyl"]


clientID = discordsettings['application_id']
clientSecret = discordsettings['secret_key']
redirectURI = discordsettings['redirect_uri']

pteroURL = pterosettings['url']
pteroAppKey = pterosettings['key']

# ------------------------------------------------------------------------------------------- #
# with open('test.json', 'r') as filee:
#     data = json.load(filee)
# data['among'] = "us"
# with open('test.json', 'w') as fil:
#     json.dump(data, fil)
#   ^
#   |
# this is how you write to a json dictionary in python
