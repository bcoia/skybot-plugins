import re

from util import hook
import json

@hook.command('hs')
@hook.command
def hearthstone(inp):
    ".hs/.hearthstone -- searches the Hearthstone API for info on a card named <query>"
    
    json_file = 'AllSets.json'
    try:
        json_f = open(json_file, "r")
    except IOError, e:
        return "error: can't load json file, did you download it from hearthstonejson.com?"

    result = searchCard(json_f, inp)
    
    if not result:
        return 'error: cannot find a card named %s' % inp

    name = result['name']
    cost = result['cost']
    ctype = result['type']
    try:
        rarity = result['rarity']
    except KeyError, e:
        rarity = "Rarityless"
    try:
        cclass = result['playerClass']
    except KeyError, e:
        cclass = "Neutral"
    try:
        text = result['text']
        for bad in ["<b>", "</b>", "<i>", "</i>", "$"]:
	    text = text.replace(bad, "")
    except KeyError, e:
        text = " "

    cardset = result['set']
    
    if ctype == 'Minion':
        try:
            race = result['race']
        except KeyError, e:
            race = "Minion"
        health = result['health']
        attack = result['attack']
	if (text != " "): return '(%s) \x02%s\x02 | %s %s %s, %s set | %s/%s, %s' % (cost, name, rarity, cclass, race, cardset, attack, health, text)
        else: return '(%s) \x02%s\x02 | %s %s %s, %s set | %s/%s' % (cost, name, rarity, cclass, race, cardset, attack, health)
    elif ctype == 'Spell':
        return '(%s) \x02%s\x02 | %s %s Spell, %s set | %s' % (cost, name, rarity, cclass, cardset, text)
    elif ctype == 'Weapon':
        attack = result['attack']
        durability = result['durability']
        if (text != " "): return '(%s) \x02%s\x02 | %s %s Weapon, %s set | %s/%s, %s' % (cost, name, rarity, cclass, cardset, attack, durability, text)
        else: return '(%s) \x02%s\x02 | %s %s Weapon, %s set | %s/%s' % (cost, name, rarity, cclass, cardset, attack, durability)
    else:
        return '(%s) \x02%s\x02 | %s' % (cost, name, text)

def searchCard(file, inp):
    setList = ['Basic', 'Expert', 'Curse of Naxxramas', 'Goblins vs Gnomes', 'The Grand Tournament', 'League of Explorers', 'Tavern Brawl', 'Promotion', 'Reward']
    final_json = json.load(file)
    card = None
    bestMatchNum = 9999 #im lazy
    bestMatchCard = None

    for nextSet in setList:
        cset = final_json[nextSet]
        for item in cset:
            if item["type"] == "Enhancement": continue
	    tmp = item["name"].lower().find(inp.lower())
            if tmp == 0:
		item['set'] = nextSet #tacking set to card
		return item
            if tmp != -1 and tmp < bestMatchNum:
		 bestMatchNum = tmp
                 bestMatchCard = item
                 bestMatchCard['set'] = nextSet
    return bestMatchCard #will return none for no matches
    
