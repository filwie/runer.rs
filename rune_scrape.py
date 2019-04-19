#!/usr/bin/env python3

import json
import re
from pathlib import Path
import urllib.request
import logging

import bs4

character_map = {}
output_file = Path(__file__).parent / 'data' / 'character_map.json'

rune_chart_url = 'https://en.wikipedia.org/wiki/Runic_(Unicode_block)'

log = logging.getLogger(__file__)


def get_soup(url) -> bs4.BeautifulSoup:
    with urllib.request.urlopen(rune_chart_url) as res:
        log.info('GET: %s RESPONSE: %s', rune_chart_url, res.status)
        raw = res.read()
    return bs4.BeautifulSoup(raw, 'html.parser')


def parse_character_table(soup) -> dict:
    character_map = {}
    symbol_table = soup.find('table', attrs={'class': 'wikitable'})
    rows = symbol_table.find_all('tr')[1:]
    for row in rows:
        code_point = row.find_all('td')[0].get_text().lower()
        name = row.find_all('td')[2].get_text()
        letter = re.match(r'^(?:.*\s)?([A-Z])$', name)
        if letter:
            letter = letter.group(1)
            code_point = f'\\u{code_point}'
            log.info('Parsed rune for letter %s: %s', letter, code_point)
            character_map.update({letter: code_point})
    return character_map


def write_results_to_file(results: dict, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    log.info("Wrote results to file: %s", output_file.resolve())
    output_file.write_text(json.dumps(results, indent=2, sort_keys=True))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    soup = get_soup(rune_chart_url)
    character_map = parse_character_table(soup)
    write_results_to_file(character_map, output_file)
