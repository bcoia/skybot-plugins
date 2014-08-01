import re
from util import hook, http


@hook.command
def twitch(inp, url_pasted=None):
    ".twitch -- gets TwitchTV channel info for <user>"
    
    request_url = "https://api.twitch.tv/kraken/streams/%s" % inp
    stream_url = "http://www.twitch.tv/%s" % inp

    try:
        response = http.get_json(request_url)
    except http.HTTPError, e:
        errors = {400: 'bad request (rate limited?)',
                  401: 'unauthorized',
                  403: 'forbidden',
                  404: 'invalid user/id',
                  500: 'twitch is broken',
                  502: 'twitch is down',
                  503: 'twitch is overloaded',
                  410: 'twitch shut off the api'}
        if e.code == 404:
            return 'error: channel %s does not exist' % inp
        if e.code in errors:
            return 'error: ' + errors[e.code]
        return 'error: unknown %s' % e.code

    stream = response['stream']
    if not stream:
        request_url = "https://api.twitch.tv/kraken/channels/%s" % inp
        response = http.get_json(request_url)
        title = response['status']
        game = response['game']
        if game is None:
            game = ''
        else:
            game = ' is playing \x02%s\x02' % game
        if url_pasted is None:
            return '\x02%s\x02%s | \x02%s\x02 | %s' % (inp, game, title, stream_url)
        else:
            return '\x02%s\x02%s | \x02%s\x02' % (inp, game, title)
    else:
        channel = stream['channel']
        name = channel['display_name']
        game = stream['game']
        if game is None:
            game = ''
        else:
            game = ' playing \x02%s\x02' % game
        viewers = stream['viewers']
        if viewers == 0:
            viewers = '\x02no\x02 viewers'
        if viewers == 1:
            viewers = '\x021\x02 viewer'
        else:
            viewers = '\x02%s\x02 viewers' % viewers
        title = channel['status']
        if url_pasted is None:
            return '\x02%s\x02 is \x02LIVE\x02%s | \x02%s\x02 | %s | %s' % (name, game, title, viewers, stream_url)
        else:
            return '\x02%s\x02 is \x02LIVE\x02%s | \x02%s\x02 | %s' % (name, game, title, viewers)

@hook.regex(r'twitch.tv/([_0-9a-zA-Z]+)')
def show_channel(match, url_pasted=None):
    return twitch(match.group(1), 'yes')
