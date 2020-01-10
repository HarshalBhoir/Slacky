from slackself import config, client, Prefixes
from slack.errors import SlackApiError
from terminaltables import AsciiTable
import slack
import httpx

def check_user(user):
    if user == config['user']:
        return True
    else:
        return False

def help(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        rtm_client = payload['rtm_client']
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~help':
                print(Prefixes.event + 'Ran Command: help')
                table = [
                    ['Command', 'Description', 'Usage'],
                    ['heartbeat', 'Check if bot is up or not', '~heartbeat'],
                    ['info', 'Get info about the bot', '~info'],
                    ['shift', 'CrEaTe ShIfT tExT lIkE tHiS', '~shift <phrase>'],
                    ['subspace', 'Replace spaces with emojis', '~subspace :smile: <msg>'],
                    ['xkcd', 'Get Daily xkcd comic', '~xkcd'],
                    ['react', 'React to last sent message', '~react :emoji:'],
                    ['help', 'Display this message', '~help']
                ]
                ttable = AsciiTable(table)
                str_table = str(ttable.table)
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text="```{}```".format(str_table),
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')

def sub_space(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        rtm_client = payload['rtm_client']
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~subspace':
                print(Prefixes.event + 'Ran Command: subspace')
                emoji = text_split[1]
                rest = ' '.join(text_split[2:])
                rest = rest.replace(' ', ' {} '.format(emoji))
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text=rest,
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')

def shift(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        rtm_client = payload['rtm_client']
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~shift':
                print(Prefixes.event + 'Ran Command: shift')
                rest = ' '.join(text_split[1:])
                new_text = ""
                count = 0
                for char in rest:
                    if count == 0:
                        new_text += char.upper()
                        count = 1
                    else:
                        new_text += char.lower()
                        count = 0
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        text=new_text,
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')

def info(**payload):
    data = payload['data']
    channel_id = data['channel']
    user = data.get('user')
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        rtm_client = payload['rtm_client']
        if '~info' == data.get('text', []):
            print(Prefixes.event + 'Ran Command: info')
            try:
                web_client.chat_update(
                    channel=channel_id,
                    blocks=[{
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": """\
Running :slack: *Slacky* by <https://twitter.com/maxbridgland|Max Bridgland>

To See Commands Run: *~help*

*Source Code*: <https://github.com/M4cs/Slacky|GitHub>"""
                        }
                    }],
                    ts=timestamp
                )
            except SlackApiError:
                print(Prefixes.error + 'Failed To Send Message!')

def heartbeat(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        rtm_client = payload['rtm_client']
        if '~heartbeat' == data.get('text', []):
            print(Prefixes.event + 'Ran Command: heartbeat')
            try:
                web_client.chat_update(
                    channel=channel_id,
                    text="I'm Alive!",
                    ts=timestamp
                )
            except SlackApiError:
                print(Prefixes.error + 'Failed To Send Message!')

def react(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        rtm_client = payload['rtm_client']
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~react':
                try:
                    web_client.chat_delete(
                        channel=channel_id,
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Delete Your Message!')
                emoji = text_split[1]
                print(Prefixes.event + 'Ran Command: react')
                conv_info = client.conversations_info(channel=channel_id)
                latest = conv_info['channel']['latest']
                latest_ts = latest['ts']
                try:
                    web_client.reactions_add(
                        channel=channel_id,
                        timestamp=latest_ts,
                        name=emoji
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To React To Message!')

def xkcd(**payload):
    data = payload['data']
    user = data.get('user')
    channel_id = data['channel']
    timestamp = data['ts']
    if check_user(user):
        web_client = client
        rtm_client = payload['rtm_client']
        text = data.get('text')
        if text:
            text_split = text.split(' ')
            cmd = text_split[0]
            if cmd == '~xkcd':
                print(Prefixes.event + 'Ran Command: xkcd')
                res = httpx.get('https://xkcd.com/info.0.json').json()
                link = res['img']
                alt_text = res['alt']
                try:
                    web_client.chat_update(
                        channel=channel_id,
                        blocks=[
                            {
                                "type": "image",
                                "title": {
                                    "type": "plain_text",
                                    "text": "Today's xkcd Comic",
                                    "emoji": True
                                },
                                "image_url": link,
                                "alt_text": alt_text
                            }
                        ],
                        ts=timestamp
                    )
                except SlackApiError:
                    print(Prefixes.error + 'Failed To Send Message!')