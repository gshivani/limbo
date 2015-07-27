"""!search <query> will return the top google result for that query (!google is an alias)"""

import re
import json
import urllib2

CATEGORIES = ['inspire', 'management', 'sports', 'life', 'funny', 'love', 'art']

def inspire(category):
    url = urllib2.urlopen("http://api.theysaidso.com/qod.json?category=#{0}".format(category))
    resp = json.load(url)
    if not resp:
        return ":crying_cat_face: Sorry, eve doesn't have a quote for you :crying_cat_face:"
    
    author = resp["contents"]["quotes"][0]["author"]
    quote  = resp["contents"]["quotes"][0]["quote"]
    return "{} - {}".format(quote, author)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"^!quote (.*)$", text)
    if not match:
        return
    category = match[0]
    
    if category:
        if category not in CATEGORIES:
            return "Sorry, eve can get quotes only from {} categories".format(", ".join(CATEGORIES))
     
    return inspire(match[0])
