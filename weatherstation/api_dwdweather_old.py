# coding=utf-8

"""
Parsing dwd webpage for severe weather warnings
"""

import requests
import chardet

from lxml import html

DWD_WEBPAGE_URL = (
    "https://www.dwd.de/DE/wetter/warnungen_aktuell/warnlagebericht/warnlagebericht_node.html"
)
HEADER = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)"
        + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
    )
}


def download_dwd_webpage():
    """
    download raw webpage of dwd and return its content as bytest

    >>> download_dwd_webpage() is not None
    True
    """
    response = requests.get(DWD_WEBPAGE_URL, headers = HEADER)
    return response.content


def scrap_weather_from_html(html_in_bytes):
    """
    parse html and returns an array nodes between the 'wettertext' item

    >>> html_str = '''<div id="wettertext"><h3>foo</h3><h2>bar</h2></div>'''
    >>> scrap_weather_from_html(bytes(html_str, 'utf-8'))
    ['foo', 'bar']
    """
    assert isinstance(html_in_bytes, bytes)

    encoding = chardet.detect(html_in_bytes)['encoding']
    if encoding != 'utf-8':
        html_in_bytes = html_in_bytes.decode(encoding, 'replace').encode('utf-8')

    tree = html.fromstring(html_in_bytes)
    nodes = tree.xpath('//div[@id="wettertext"]/*/text()')

    return nodes


def cleanup_scrapped_weather(weather):
    """
    filter the scrap from scrapped weather information

    possible input: [
        'WARNLAGEBERICHT f�r Deutschland',
        'ausgegeben vom Deutschen Wetterdienst',
        'am Mittwoch, 15.11.2017, 12:50 Uhr',
        'Ruhiges Novemberwetter. In der Nacht zum Donnerstag im S�den leichter Frost.',
        'Entwicklung der WETTER- und WARNLAGE f�r die n�chsten 24 Stunden',
        'bis Donnerstag, 16.11.2017, 11:00 Uhr:',
        'Im S�den gestaltet sich das Wetter unter Hochdruckeinfluss ruhig.
            Im Norden sorgen dagegen schwache Tiefausl�ufer f�r einen leicht unbest�ndigen ...
        ', 'Aktuell sind folgende Warnungen in Kraft:',
        'FROST: In der S�dh�lfte nachts leichter Frost zwischen 0 und -5 Grad. �rtlich darunter.',
        'N�chste Aktualisierung: sp�testens Mittwoch, 15.11.2017, 16:00 Uhr'
    ]
    """
    assert isinstance(weather, list)

    filtered = [x.strip().replace('\n', '').replace('\r', '') for x in weather if len(x) > 0]
    if len(filtered) > 3:
        filtered = [filtered[i] for i in range(2, len(filtered) - 1)]

    return filtered


def get_severe_weather_warning():
    """
    download weather data form dwd and returns information
    """
    dwd_webpage = download_dwd_webpage()

    weather_information = scrap_weather_from_html(dwd_webpage)
    return cleanup_scrapped_weather(weather_information)


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    weather_information = get_severe_weather_warning()
    for i in range(0, len(weather_information)):
        text = bytes(weather_information[i], "utf-8")
        encoding = chardet.detect(text)['encoding']
        if encoding != 'utf-8':
            text = text.decode(encoding, 'replace').encode('utf-8')

        print(text)

    print("ü")
    #print(get_severe_weather_warning())
