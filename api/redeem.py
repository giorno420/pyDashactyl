from pydactyl import PterodactylClient
import configfile
import paypalrestsdk
from paypalrestsdk import Payment, Order

client = PterodactylClient(configfile.pteroURL, configfile.pteroAppKey)
