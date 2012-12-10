from pyquery import PyQuery as pq
import requests


BASE_URL = 'http://www.austintexas.gov/health/restaurant/scores.cfm'
FORM_URL = 'http://www.austintexas.gov/health/restaurant/search.cfm'
LABELS = ('name', 'address', 'city', 'zipcode', 'inspection_date', 'score')


def get_start_and_end_dates():
    """Determine the start and end dates available by scraping them"""
    doc = pq(url=FORM_URL)
    return [a.text.strip() for a in doc.find('#col3_content ul li b')]


def get_all_rows_of_data(start, end):
    """
    Fetch all of the rows from the city and return them

    Note that this fetches *all* rows, so you need to filter out any
    that you don't want to deal with.
    """
    request_data = {
        'begdate': start,
        'enddate': end,
        'selpara': 0,
        'estabname': '',
        'estabcity': 'All',
        'estabzip': 'All',
        'Submit': 'Search'
    }
    response = requests.post(BASE_URL, data=request_data)
    doc = pq(response.content)
    return doc.find('#col3_content table tr')


def extract_raw_data(rows):
    """
    Generator that extracts a dictionary from a row

    This cleans up the data for a given row and turns it into a ``dict``
    before yielding each row.  Since this is a generator, you need to
    iterate over the results in order to extract all of the rows.
    """
    for row in rows:
        raw_data = [a.text.strip() if a.text is not None else ''
                for a in row.findall('td')]
        if not raw_data:
            continue
        yield dict(zip(LABELS, raw_data))


def scrape(generator=False):
    """
    Scrapes the entire set of data and returns a list

    This is the main entry point for this module.  It's meant to be
    called, then iterated over to determine what values are provided.
    It does not group data, instead leaving that to the programmer
    consuming this data.

    You can return a raw generator by passing ``generator=True`` when
    calling this function.  That allows you to only iterate over the
    data once and not use any more memory than necessary.
    """
    start, end = get_start_and_end_dates()
    rows = get_all_rows_of_data(start, end)

    result = extract_raw_data(rows)
    return result if generator else [a for a in result]
