

from pathlib import Path
from html.parser import HTMLParser
import json
import unittest
import urllib.error
from unittest.mock import patch
from http.client import IncompleteRead
import check_animal_populations as populations
from animals.photograph_information import PHOTOS

ROOT = Path(__file__).resolve().parent
# Source examples keep parser tests independent of live websites.
STATEMENTS = {
    'tiger': 'numbers are now on the rise at 5,711 in 2025',
    'amur-leopard': 'increased to around 130 adults',
    'asian-elephant': 'fewer than 52,000 Asian elephants left in the wild',
    'black-rhino': 'black rhinos increased from 6,195 in 2022 to 6,788 at the end of 2024',
    'mountain-gorilla': 'overall total of mountain gorillas is now 1,063',
    'sumatran-orangutan': 'Orangutan Sumatera (Pongo abelii) diperkirakan mencapai 11.694 individu',
    'hawksbill-turtle': 'Population estimate is between 20,000 and 23,000 nesting females',
    'blue-whale': 'Population 10,000–25,000',
    'vaquita': 'confirming sightings of between 7 and 10 vaquitas',
    'kakapo': 'There are 325 kākāpō alive today'
}


# Read only the JSON consumed by website-actions.js.
class PageData(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_data = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script' and dict(attrs).get('id') == 'atlas-data':
            self.in_data = True

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_data = False

    def handle_data(self, text):
        if self.in_data:
            self.parts.append(text)


# Cover parsing, editorial review, and cached network failures.
class SourceTests(unittest.TestCase):
    def setUp(self):
        populations._CACHE.clear()

    def test_all_population_parsers(self):
        for animal in populations.SPECIES:
            with self.subTest(species=animal['slug']):
                value, _ = populations.parse_population(animal, '<p>' + STATEMENTS[animal['slug']] + '</p>')
                self.assertEqual(value, animal['population'])

    def test_updated_tiger_year(self):
        result = populations.parse_population(populations.BY_SLUG['tiger'], 'numbers are now on the rise at 6,100 in 2026')
        self.assertEqual(result, ('6,100', '2026 estimate'))

    def test_fixed_report_change(self):
        with self.assertRaises(ValueError):
            populations.parse_population(populations.BY_SLUG['blue-whale'], 'Population 11,000–26,000')

    def test_hidden_source_text(self):
        with self.assertRaises(ValueError):
            populations.parse_population(populations.BY_SLUG['kakapo'], '<script>There are 999 kākāpō alive today</script>')

    def test_unavailable_source(self):
        with patch('check_animal_populations.urllib.request.urlopen', side_effect=urllib.error.URLError('offline')):
            result = populations.check_source('kakapo')
        self.assertEqual(result['population'], '325')
        self.assertEqual(result['verification'], 'unavailable')
        self.assertIsNone(result['checked_at'])

    def test_failure_cache(self):
        with patch('check_animal_populations.urllib.request.urlopen', side_effect=urllib.error.URLError('offline')) as request:
            populations.check_source('kakapo')
            result = populations.check_source('kakapo', force=True)
        self.assertEqual(request.call_count, 1)
        self.assertTrue(result['cached'])

    def test_incomplete_response(self):
        with patch('check_animal_populations.urllib.request.urlopen', side_effect=IncompleteRead(b'partial')):
            result = populations.check_source('kakapo')
        self.assertEqual(result['verification'], 'unavailable')


# Check the actual page data, photograph records, and map destinations.
class ProjectTests(unittest.TestCase):
    def test_page_data(self):
        pages = list((ROOT / 'website-layout').glob('*.html')) + list((ROOT / 'animals').glob('*.html'))
        self.assertEqual(len(pages), 13)
        for page in pages:
            parser = PageData()
            parser.feed(page.read_text(encoding='utf-8'))
            data = json.loads(''.join(parser.parts))
            self.assertEqual(len(data['animals']), 10)

    def test_animal_photographs(self):
        for animal in populations.SPECIES:
            photos = [photo for photo in PHOTOS if photo['slug'] == animal['slug']]
            self.assertEqual(len(photos), 3)
            for photo in photos:
                self.assertTrue((ROOT / photo['src'].lstrip('/')).is_file())
                self.assertTrue(photo['credit'])
                self.assertTrue(photo['source'].startswith('https://'))

    def test_map_destinations(self):
        world_map = (ROOT / 'maps/world-map.svg').read_text(encoding='utf-8')
        for animal in populations.SPECIES:
            filename = animal['slug'] + '-page.html'
            self.assertTrue((ROOT / 'animals' / filename).is_file())
            self.assertIn('href="/animals/' + filename + '"', world_map)


if __name__ == '__main__':
    unittest.main()
