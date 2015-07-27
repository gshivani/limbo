# -*- coding: utf-8 -*-
"""!standup returns a standup message"""

import re

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"(.*) !standup", text)
    if not match:
        return
    return "Alright, It's standup time!" 
