# -*- coding: utf-8 -*-
"""!aws help returns syntax of messages that eve would respond to for aws plugin."""

import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!aws help", text)
    if not match:
        return
    return "!aws count server" + "\n" + \
    "!aws count server running" + "\n" + \
    "!aws count server with tag <key:value>" + "\n" + \
    "!aws details server with tag <key:value>" + "\n" + \
    "!aws details server with age days <days_to_subtract>"