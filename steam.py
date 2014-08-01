import re
from util import hook, http


@hook.command
def steam(inp, url_pasted=None):
    ".steam -- gets Steam store info for <game>"
    
    url = "http://store.steampowered.com/app/%s" % inp

    try:
        doc = http.get_html(url)
    except http.HTTPError, e:
        errors = {400: 'bad request (rate limited?)',
                  401: 'unauthorized',
                  403: 'forbidden',
                  404: 'invalid user/id',
                  500: 'steam is broken',
                  502: 'steam is down',
                  503: 'steam is overloaded'}
        if e.code == 404:
            return 'error: game %s does not exist' % inp
        if e.code in errors:
            return 'error: ' + errors[e.code]
        return 'error: unknown %s' % e.code

    title = doc.find_class('apphub_AppName')[0].text_content()
    if not doc.find_class('discount_prices'):
        price = doc.find_class('game_purchase_price')[0].text_content()
    else:
        fullprice = doc.find_class('discount_original_price')[0].text_content()
        discountprice = doc.find_class('discount_final_price')[0].text_content()
        discountpct = doc.find_class('discount_pct')[0].text_content()
        price = '%s (%s, originally %s)' % (discountprice, discountpct, fullprice)

    if url_pasted is None:
        return '%s | %s | %s' % (title, price, url)
    else:
        return '%s | %s' % (title, price)

@hook.regex(r'store.steampowered.com/app/([0-9]+)')
def show_channel(match, url_pasted=None):
    return steam(match.group(1), 'yes')
