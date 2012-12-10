from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=250)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='locations')
    address = models.CharField(max_length=250)
    city = models.ForeignKey(City, related_name='restaurant_locations',
            blank=True, null=True)
    zipcode = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s: %s" % (self.restaurant, self.address)


class Score(models.Model):
    location = models.ForeignKey(Location, related_name='scores')
    inspection_date = models.DateField()
    score = models.PositiveIntegerField()

    def __unicode__(self):
        return "%s: %s (%s)" % (self.location,
                self.inspection_date.strftime('%Y/%m/%d'), self.score)
