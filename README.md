# Skybot Plugins

Plugins for your [Skybot](http://github.com/rmmh/skybot)!

## twitch.py
Unfurls Twitch URLs with title, game, status and viewers.

### Usage
```
<bcoia> twitch.tv/twitchplayspokemon
<skybot> TwitchPlaysPokemon is LIVE playing Pokémon Battle Revolution | Twitch Plays Pokemon (Enter moves via chat!!!) | 557 viewers
```

Also adds `.twitch [username]` command to search a username manually. Output includes the channel's URL.
```
<bcoia> .twitch saltybet
<skybot> SaltyBet is LIVE playing M.U.G.E.N | Salty's Dream Cast Casino! Place your bets at www.saltybet.com | 351 viewers | http://www.twitch.tv/saltybet
```

### Installation
1. Place `twitch.py` in your Skybot's `/plugins/` directory. That's it!

## hearthstone.py
Queries local Hearthstone JSON database (provided by hearthstonejson.com) for a given card name and returns information. Returns closest match for partial names.

### Usage
```
<bcoia> .hs argent
<skybot> (6) Argent Commander | Rare Neutral Minion, Expert set | 4/2, Charge, Divine Shield
```

### Installation
1. Place `AllSets.json` from hearthstonejson.com in your Skybot's root directory.
2. Place `hearthstone.py` into your Skybot's `/plugins/` directory.
