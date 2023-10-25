"""
Program to analize the logs files of an apache server.
An example of file acommpanies this file: access.log

Date: 22 Oct, 2024.
By: Santiago Romo G. 

"""

import re, logging, doctest
from datetime import datetime

def get_user_agent(line: str) -> str:
    """
    Get the user agent of the line.

    Expamples
    ---------
    >>> 
    get_user_agent('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

    >>> get_user_agent('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0'
    """
    user_to_seek = line.split('" ')[-1].strip('" \n')
    if len(user_to_seek) > 2: return user_to_seek


def is_bot(line: str) -> bool:
    '''
    Check of the access in the line correspons to a bot

    Examples
    --------
    >>> is_bot('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    False

    >>> is_bot('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    True

    >>> is_bot('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
    True
    '''
    pattern_to_seek = re.compile(r'bot')

    if line: return bool( pattern_to_seek.search(line.lower()))
    else: return False


def get_ipaddr(line: str) -> str:
    '''
    Gets the IP address of the line

    >>> get_ipaddr('213.180.203.109 - - [15/Sep/2023:00:12:18 +0200] "GET /robots.txt HTTP/1.1" 302 567 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)"')
    '213.180.203.109'

    >>> get_ipaddr('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antares.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    '147.96.46.52'
    '''
    pattern_to_seek = re.compile(r'^([0-9]+\.)+[0-9]+\b')
    return pattern_to_seek.search(line).group(0)


def get_hour(line: str) -> int:
    """
    Get the user agent of the line.

    Examples
    ---------
    >>> get_hour('66.249.66.35 - - [15/Sep/2023:00:18:46 +0200] "GET /~luis/sw05-06/libre_m2_baja.pdf HTTP/1.1" 200 5940849 "-" "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"')
    0

    >>> get_hour('147.96.46.52 - - [10/Oct/2023:12:55:47 +0200] "GET /favicon.ico HTTP/1.1" 404 519 "https://antacres.sip.ucm.es/" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"')
    12
    """
    pattern_to_seek = re.compile(r'\[(.+)\]')
    m = pattern_to_seek.search(line)
    return datetime.strptime(m.group(1), '%d/%b/%Y:%H:%M:%S %z').hour


def histbyhour(filename: str) -> dict[int, int]:
    '''
    Computes the histogram of access by hour

     Examples
    ---------
    >>> histbyhour('access.log')
    {2: 2,
     5: 4,
     7: 2,
     10: 2,
     11: 3,
     12: 2,
     15: 2,
     17: 3,
     18: 2,
     20: 3,
     21: 16,
     22: 3,
     23: 4}
    '''
    hours_recorded = dict()
    with open(filename) as file:
          for line in file:
            accessed_hour = get_hour(line)
            if accessed_hour in hours_recorded.keys():
                hours_recorded[accessed_hour] += 1
            else:
                hours_recorded[accessed_hour] = 1
    return hours_recorded


def ipaddreses(filename: str) -> set[str]:
    '''
    Returns the IPs of the accesses that are not bots
    
    Examples
    ---------
    >>> ipaddreses('access.log')
    {'119.120.163.213',
     '147.96.60.31',
     '185.105.102.189',
     '188.76.13.241',
     '189.217.221.3',
     '20.120.74.197',
     '203.2.64.59',
     '23.229.104.2',
     '34.105.93.183',
     '34.132.45.188',
     '34.79.162.186',
     '39.103.168.88',
     '65.154.226.171',
     '94.23.8.213'}
    '''
    ip_numbers = set()
    with open(filename) as file:
        for line in file:
            if not is_bot(get_user_agent(line)): ip_numbers.add(get_ipaddr(line))
    return ip_numbers


def test_doc():
    doctest.run_docstring_examples(get_user_agent, globals(), verbose=True)
    doctest.run_docstring_examples(is_bot, globals(), verbose=True)
    doctest.run_docstring_examples(get_ipaddr, globals(), verbose=True)
    doctest.run_docstring_examples(get_hour, globals(), verbose=True)


def test_ipaddresses():
    assert ipaddreses('access_short.log') == {'34.105.93.183', '39.103.168.88'}


def test_hist():
    hist = histbyhour('access_short.log')
    assert hist == {5: 3, 7: 2, 23: 1}


def main() -> None:
    try:
        #print(ipaddreses('access.log'))
        #print(histbyhour('access.log'))
        test_ipaddresses()
        test_hist()
 
    except FileNotFoundError as e:
        logging.error(f'Error found: {e}')
    
if __name__ == '__main__':
    main()
