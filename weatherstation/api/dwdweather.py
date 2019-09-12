"""html scrapper for dwd weather to retrieve the severe weather warnings"""

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

def download_webpage():
    """Returns coroutine to download the content dwd webpage in bytes"""
    response = requests.get(DWD_WEBPAGE_URL, headers=HEADER)
    return response.content


def scrap_weather_nodes_from_html(html_bytes):
    """Returns [string] of all nodes in the 'wettertext' div of the given html"""
    assert isinstance(html_bytes, bytes)

    encoding = chardet.detect(html_bytes)['encoding']
    if encoding != 'utf-8':
        html_bytes = html_bytes.decode(encoding, 'replace').encode('utf-8')

    tree = html.fromstring(html_bytes)
    return tree.xpath('//div[@id="wettertext"]/*/text()')


def cleanup_scrapped_weather_data(nodes):
    """
    returns [string] by removing all unrelevant nodes (ie. empty nodes) from the given import

    possible input: [
        'WARNLAGEBERICHT für Deutschland',
        'ausgegeben vom Deutschen Wetterdienst',
        'am Mittwoch, 15.11.2017, 12:50 Uhr',
        'Ruhiges Novemberwetter. In der Nacht zum Donnerstag im Süden leichter Frost.',
        'Entwicklung der WETTER- und WARNLAGE für die nächsten 24 Stunden',
        'bis Donnerstag, 16.11.2017, 11:00 Uhr:',
        'Im Süden gestaltet sich das Wetter unter Hochdruckeinfluss ruhig.
            Im Norden sorgen dagegen schwache Tiefausläufer für einen leicht unbeständigen ...
        ', 'Aktuell sind folgende Warnungen in Kraft:',
        'FROST: In der Südhälfte nachts leichter Frost zwischen 0 und -5 Grad. Örtlich darunter.',
        'Nächste Aktualisierung: spätestens Mittwoch, 15.11.2017, 16:00 Uhr'
    ]
    """
    filtered = [
        x.strip().replace('\n', '').replace('\r', '') # replace linebreaks inside text
        for x in nodes
    ]
    filtered = [
        x
        for x in filtered
        if len(x) > 0 # filter empty nodes
    ]
    if len(filtered) <= 3: # if less than 3 entries, most likely no information was given
        return filtered

    return [filtered[i] for i in range(3, len(filtered) - 1)] # remove dwd header


def download_dwd_weather_data():
    """
    returns coroutine for [string] containing weather information of dwd (german weather)
    """
    raw_html = download_webpage()
    raw_weather_information = scrap_weather_nodes_from_html(raw_html)
    result = cleanup_scrapped_weather_data(raw_weather_information)
    return result

download_dwd_weather_data()
