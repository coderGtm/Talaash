from django.db import models
import datetime

# Create your models here.

class Keywords(models.Model):
    keyword_string = models.CharField(max_length=100)


class Urls(models.Model):
    address = models.CharField(unique=True ,max_length=100)
    num_of_refs = models.IntegerField(default=1)
    keywords_in_it = models.ManyToManyField(Keywords)
    last_scrapped = models.DateTimeField(default=datetime.datetime.min)
