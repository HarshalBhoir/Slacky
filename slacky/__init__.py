from slacky.config import load_config as lc
from slacky.api.auth import authenticate
from colorama import init
from colorama import Fore, Back, Style
from time import time
import httpx, json, logging, getpass

class Prefixes:
    info = str('[' + Fore.GREEN + Style.BRIGHT + 'INFO' + Style.RESET_ALL + '] ')
    warning = str('[' + Fore.YELLOW + Style.BRIGHT + 'WARNING' + Style.RESET_ALL + '] ')
    event = str('[' + Fore.BLUE + Style.BRIGHT + 'EVENT' + Style.RESET_ALL + '] ')
    error = str('[' + Fore.RED + Style.BRIGHT + 'ERROR' + Style.RESET_ALL + '] ')
    start = str('[' + Fore.LIGHTBLUE_EX + Style.BRIGHT + 'SLACKY' + Style.RESET_ALL + '] ')

class Listeners:
    def __init__(self, config):
        self.listeners = config['listeners']

    def add(self, phrase):
        self.listeners.append(phrase)
        with open('config.json', 'r+') as file:
            obj = json.load(file)
            obj['listeners'] = self.listeners
            file.seek(0)
            json.dump(obj, file, indent=4)
            file.truncate()
    
    def delete(self, phrase):
        num = self.listeners.index(phrase)
        del self.listeners[num]
        with open('config.json', 'r+') as file:
            obj = json.load(file)
            obj['listeners'] = self.listeners
            file.seek(0)
            json.dump(obj, file, indent=4)
            file.truncate()

print(Prefixes.start + 'Welcome to Slacky v1 | The First Python Self-Bot for Slack!')
config = lc()
if not config:
    print(Prefixes.warning + 'No Config File Found. Starting Wizard.')
    print(Prefixes.start + 'Enter Legacy Workspace Token (Starts w/ xoxp)')
    token = input('> ')
    print(Prefixes.start + 'Enter User ID. Google How To Get This.')
    user_id = input('> ')
    print(Prefixes.info + 'Entered Token:', token)
    print(Prefixes.info + 'Entered User ID:', user_id)
    print(Prefixes.start + 'Press ENTER to Confirm Information or Ctrl+C to Quit.')
    getpass.getpass('')
    with open('config.json', 'w+') as file:
        config = {
            'token': token,
            'user': user_id,
            'listeners': []
        }
        json.dump(config, file, indent=4)
    print(Prefixes.event + 'Config Saved! Please Restart To Use Slacky')
    exit(0)

print(Prefixes.info + 'Config Loaded')
print(Prefixes.event + 'Attempting to Authenticate with Slack', end='\r')
listener = Listeners(config)
client = authenticate(config)
if not client:
    print(Prefixes.error + 'Could Not Authenticate with Slack! Please check your config and token!')
print(' ' * 65, end='\r')
print(Prefixes.info + 'Authentication Successful!')
