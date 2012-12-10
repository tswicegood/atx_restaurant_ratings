from django.core.management.base import NoArgsCommand

from ... import models
from ... import scraper


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        restaurant_cache = {}
        city_cache = {}
        counter = 0
        for row in scraper.scrape(generator=True):
            if row['name'] in restaurant_cache:
                restaurant = restaurant_cache[row['name']]
            else:
                restaurant, created = models.Restaurant.objects.get_or_create(
                        name=row['name'])
                restaurant_cache[row['name']] = restaurant

            if row['city'] in city_cache:
                city = city_cache[row['city']]
            else:
                city, created = models.City.objects.get_or_create(
                        name=row['name'])
                city_cache[row['city']] = city

            location, created = models.Location.objects.get_or_create(
                    restaurant=restaurant, city=city, address=row['address'],
                    zipcode=row['zipcode'])

            month, day, year = row['inspection_date'].split('/')
            inspection_date = '%s-%s-%s' % (year, month, day)
            models.Score.objects.create(location=location,
                    inspection_date=inspection_date, score=row['score'])

            counter += 1
            if counter % 250 == 0:
                print "Processed: %d" % counter
