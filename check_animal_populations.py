"""Population checks: read published estimates from linked source pages.

The species rules control accepted figures. Failed checks return saved estimates.
Run python check_animal_populations.py --species kakapo --refresh for one source.
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from http.client import HTTPException
import copy
import json
import re
import threading
import time
import urllib.error
import urllib.request

from animals.animal_information import ANIMALS as SPECIES
BY_SLUG = {animal['slug']: animal for animal in SPECIES}  # A lookup table: BY_SLUG['tiger'] gives the tiger's full saved record.
# Reuse successful checks for six hours; retry failures after one minute.
CACHE_TTL = 6 * 60 * 60  # 6 hours in seconds; TTL means how long a cached success can be reused.
FAILURE_TTL = 60  # Keep a failed check for 60 seconds before trying again.
MIN_REFRESH_SECONDS = 60  # Even a manual refresh must wait this long after a completed check.
_CACHE = {}  # Temporary memory: each slug stores a check time and its result; restarting clears it.
_LOCK = threading.Lock()  # Only one thread at a time can read or write the protected cache section.


# Collect page text while skipping scripts, styles, and noscript blocks.
class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []  # Collect the pieces of text found between HTML tags.
        self.skip = 0  # Count skipped blocks; a value above zero means ignore their text.

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style', 'noscript'):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = max(0, self.skip - 1)  # Close one skipped block, but never let the counter become negative.

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def plain_text(html):
    parser = TextOnly()
    parser.feed(html)  # Pass the downloaded HTML through the parser's tag and text handlers.
    return re.sub(r'\s+', ' ', unescape(' '.join(parser.parts))).strip()  # Join the text and turn repeated spaces, tabs, or newlines into one space.


# Build the fallback from the saved species record.
def base_record(animal):
    fields = ('slug', 'name', 'population', 'unit', 'estimate_date',
              'source_name', 'source_url', 'reviewed_on')
    result = {key: animal[key] for key in fields}
    result.update(checked_at=None, verification='saved', cached=False)  # No source has been checked yet, so this is only the saved estimate.
    return result


# Remove grouping marks, including dots used by the Indonesian source.
def extract_number(value):
    return int(re.sub(r'[^0-9]', '', value))  # Keep digits only: '5,711' becomes 5711 and '11.694' becomes 11694.


# Match the species rule and reject figures outside its review bounds.
def parse_population(animal, html):
    text = plain_text(html)
    match = re.search(animal['pattern'], text, re.I)  # Look for this animal's expected sentence; re.I ignores letter case.
    if not match:
        raise ValueError('The expected population statement was absent. The source parser needs review.')
    groups = match.groups()  # These are the pieces captured by parentheses in the search pattern.
    values = [extract_number(groups[0])]
    if animal['format'] == 'range':
        values.append(extract_number(groups[1]))  # Ranges need a second value, e.g. 7 and 10 for 7-10.
    if any(value < animal['minimum'] or value > animal['maximum'] for value in values):
        raise ValueError('The extracted figure is outside the review bounds.')
    if len(values) == 2 and values[0] > values[1]:  # Reject a range whose lower number is greater than its upper number.
        raise ValueError('The population range is reversed.')

    population = f'{values[0]:,}'  # Put the thousands separators back for display: 5711 becomes '5,711'.
    if animal['format'] == 'range':
        population += f'–{values[1]:,}'
    elif animal['format'] == 'less':
        population = '<' + population
    elif animal['format'] == 'approx':
        population = '≈' + population

    # Changed fixed reports need an editor to review the date and counting method.
    if population != animal['population'] and animal['slug'] not in ('tiger', 'kakapo'):
        raise ValueError('The changed figure requires a review of its date and population measure.')
    estimate_date = animal['estimate_date']
    if animal['slug'] == 'tiger':
        year = int(groups[1])  # For tigers, the second captured piece is the estimate year.
        if year < 2020 or year > datetime.now(timezone.utc).year:
            raise ValueError('The tiger estimate year is outside the accepted range.')
        estimate_date = f'{year} estimate'
    if animal['slug'] == 'kakapo' and population != animal['population']:
        estimate_date = 'Current recovery-page figure · count date not stated'
    return population, estimate_date


def check_source(slug, force=False):
    animal = BY_SLUG[slug]
    now = time.monotonic()  # A clock for elapsed time; changing the computer's date does not affect it.
    # Protect the shared cache used by concurrent browser requests.
    with _LOCK:
        prior = _CACHE.get(slug)
        if prior:
            age = now - prior[0]  # How many seconds have passed since this cached check finished.
            ttl = CACHE_TTL if prior[1]['verification'] == 'verified' else FAILURE_TTL
            # Refresh requests still respect the minimum interval.
            if age < MIN_REFRESH_SECONDS or (not force and age < ttl):
                result = copy.deepcopy(prior[1])  # Return a separate copy so callers cannot change the cached dictionary.
                result['cached'] = True
                return result

    result = base_record(animal)
    try:
        request = urllib.request.Request(animal['source_url'], headers={
            'User-Agent': 'Mozilla/5.0', 'Accept': 'text/html'
        })
        with urllib.request.urlopen(request, timeout=14) as response:  # Open the source with a 14-second socket timeout, not a total download deadline.
            # Read one extra byte to detect documents above the size limit.
            raw = response.read(2_000_001)
            if len(raw) > 2_000_000:
                raise ValueError('The source exceeds the document size limit.')
            encoding = response.headers.get_content_charset() or 'utf-8'  # Use the page's declared encoding, or assume UTF-8 if none was supplied.
            html = raw.decode(encoding, errors='replace')  # Turn bytes into text; replace unreadable characters instead of stopping.
        result['population'], result['estimate_date'] = parse_population(animal, html)
        result['verification'] = 'verified'
        result['checked_at'] = datetime.now(timezone.utc).isoformat()  # Record when the source was checked, not when the animals were counted.
        result['message'] = 'The expected statement was found on the linked page. The check time records source access.'
    except ValueError as error:  # The page was read, but its figure or format needs an editor's review.
        result['verification'] = 'review_required'
        result['message'] = str(error)
    except (OSError, urllib.error.URLError, HTTPException, LookupError):  # Network, response, or decoding problems leave the saved figure available.
        result['verification'] = 'unavailable'
        result['message'] = 'The source could not be read. The saved estimate remains available.'
    with _LOCK:
        _CACHE[slug] = (time.monotonic(), copy.deepcopy(result))  # Save the completed check and a separate copy of its result for later requests.
    return result


# Check requested sources in parallel, then return one API response.
def get_populations(slug=None, force=False):
    if slug and slug not in BY_SLUG:
        raise KeyError(slug)
    slugs = [slug] if slug else list(BY_SLUG)  # One slug checks one animal; no slug checks every animal in the lookup table.
    with ThreadPoolExecutor(max_workers=10) as pool:  # Run up to 10 source checks at once instead of waiting for each in turn.
        records = list(pool.map(lambda item: check_source(item, force), slugs))  # Call check_source for each slug and collect results in the same order.
    return {
        'records': records,
        'cache_seconds': CACHE_TTL,
        'method': 'Published population estimates with source-page checks.'
    }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Check linked population sources.')
    parser.add_argument('--species', choices=list(BY_SLUG))
    parser.add_argument('--refresh', action='store_true')
    args = parser.parse_args()
    print(json.dumps(get_populations(args.species, args.refresh), ensure_ascii=False, indent=2))
