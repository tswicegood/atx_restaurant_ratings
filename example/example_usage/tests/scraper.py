import datetime
import random

from django.template.loader import render_to_string
from django.test import TestCase
from mock import patch, MagicMock

from atx_restaurant_ratings import scraper


def random_date():
    now = datetime.date.today()
    r = random.randint(-1000, 1000)
    return (now - datetime.timedelta(days=r)).strftime('%m/%d/%Y')


def generate_random_start_end_doc(start_date=None, end_date=None):
    if start_date is None:
        start_date = random_date()
    if end_date is None:
        end_date = random_date()

    start = MagicMock(text=start_date)
    end = MagicMock(text=end_date)
    find = MagicMock(return_value=[start, end])
    return start_date, end_date, MagicMock(find=find)


class TestOf_get_start_and_end_dates(TestCase):
    def test_first_value_is_the_start_date(self):
        start_date, _, doc = generate_random_start_end_doc()
        with patch.object(scraper, 'pq') as mock:
            mock.return_value = doc
            result = scraper.get_start_and_end_dates()
            self.assertEqual(result[0], start_date)

    def test_second_value_is_the_end_date(self):
        _, end_date, doc = generate_random_start_end_doc()
        with patch.object(scraper, 'pq') as mock:
            mock.return_value = doc
            result = scraper.get_start_and_end_dates()
            self.assertEqual(result[1], end_date)

    def test_strips_any_extranous_whitespace_off_of_values(self):
        a, b, doc = generate_random_start_end_doc(' Alice', 'Bob ')
        with patch.object(scraper, 'pq') as mock:
            mock.return_value = doc
            actual = scraper.get_start_and_end_dates()
            self.assertEqual(['Alice', 'Bob'], actual)


class TestOf_get_all_rows_of_data(TestCase):
    def test_returns_all_matching_rows(self):
        r = random.randint(1, 10)
        content = render_to_string('for_testing/empty_rows.html',
                {'range': range(r)})

        response = MagicMock(content=content)

        with patch.object(scraper, 'requests') as mock:
            mock.post.return_value = response

            rows = scraper.get_all_rows_of_data()
            self.assertEqual(r, len(rows))
