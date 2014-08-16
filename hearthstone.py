import re

from util import hook, http

@hook.command('hs')
@hook.command
def hearthstone(inp):
    ".hs/.hearthstone -- searches the Hearthstone API for info on a card named <query>"
    
    inp = inp.replace(" ", "%20")
    request_url = 'http://hearthstoneapi.com/cards/name/%s' % inp

    response = http.get_json(request_url)
    result = response[0]
    if not result:
        return 'error: cannot find a card named %s' % inp

    name = result['name']
    description = result['description']
    cost = result['cost']
    qualities = {0: 'Common',
                 1: 'Uncommon',
                 3: 'Rare',
                 4: 'Epic',
                 5: 'Legendary'}
    quality = qualities[result['quality']]
    cardtypes = {4: 'minion',
                 5: 'spell',
                 7: 'weapon'}
    cardtype = cardtypes[result['type']]
    try:
        classs = result['classs']        
    except KeyError, e:
        classs = 99
    classtypes = {1: 'Warrior',
                  2: 'Paladin',
                  3: 'Hunter',
                  4: 'Rogue',
                  5: 'Priest',
                  7: 'Shaman',
                  8: 'Mage',
                  9: 'Warlock',
                 11: 'Druid',
                 99: 'Neutral'}
    classs = classtypes[classs]
    cardsets = {2: 'Basic',
            3: 'Expert',
            4: 'Reward',
            5: 'Missions',
            11: 'Promotion'}
    cardset = cardsets[result['set']]
    
    if cardtype == 'minion':
        health = result['health']
        attack = result['attack']
        try:
            race = result['race']        
        except KeyError, e:
            race = 1
        races = { 1: 'Minion',
                 14: 'Murloc',
                 15: 'Demon',
                 20: 'Beast',
                 21: 'Totem',
                 23: 'Pirate',
                 24: 'Dragon'}
        race = races[race]
        return '(%s) \x02%s\x02 | %s %s %s, %s set | %s/%s, %s' % (cost, name, quality, classs, race, cardset, attack, health, description)
    elif cardtype == 'spell':
        return '(%s) \x02%s\x02 | %s %s Spell, %s set | %s' % (cost, name, quality, classs, cardset, description)
    elif cardtype == 'weapon':
        attack = result['attack']
        durability = result['durability']
        return '(%s) \x02%s\x02 | %s %s Weapon, %s set | %s/%s, %s' % (cost, name, quality, classs, cardset, attack, durability, description)
    else:
        return '(%s) \x02%s\x02 | %s' % (cost, name, description)
