"""!poll will return 3 emoji for reactions"""

import re
from emojicodedictpoll import emojiCodeDictPoll

def poll():
    emoji = []
    for i in emojiCodeDictPoll:
        emoji.append(i)
    return " ".join(emoji)
        

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!poll (.*)", text)
    if not match:
        return
    return poll()