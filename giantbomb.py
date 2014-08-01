import re

from util import hook, http
from datetime import datetime, date


@hook.api_key('giantbomb')
@hook.command('rd')
@hook.command
def release(inp, api_key=None):
    ".rd/.release -- searches the GiantBomb API for the release date of <query>"
    
    request_url = 'http://www.giantbomb.com/api/search?format=json&resources=game&limit=1'

    response = http.get_json(request_url, query=inp, api_key=api_key, field_list=name,site_detail_url,expected_release_day,expected_release_month,expected_release_year,original_release_date)

    if response['number_of_page_results'] == 0:
        return 'error: %s was not found on the Giant Bomb wiki' % inp

    results = response['results']
    result = results[0]

    name = result['name']
    rday = result['expected_release_day']
    rmonth = result['expected_release_month']
    ryear = result['expected_release_year']
    rurl = result['site_detail_url']

    if rmonth is None:
        fulldatetime = result['original_release_date']
        rdatetime = fulldatetime.split(' ')
        rdate = rdatetime[0]
    else:
        rdate = "%s-%s-%s" % (ryear, rmonth, rday)

    rdatedate = datetime.strptime(rdate, "%Y-%m-%d").date()
    todaydate = datetime.today().date()
        
    if rdatedate < todaydate:
        return '\x02%s\x02 was released on \x02%s\x02 | %s' % (name, rdatedate.strftime('%b %d, %Y'), rurl)
    else:
        return '\x02%s\x02 is releasing on \x02%s\x02 | %s' % (name, rdatedate.strftime('%b %d, %Y'), rurl)
