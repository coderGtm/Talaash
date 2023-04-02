from django.db import models
import datetime

# Create your models here.

class Keywords(models.Model):
    keyword_string = models.CharField(max_length=100)

class Favicons(models.Model):
    icon_link = models.CharField(max_length=100)

class Urls(models.Model):
    address = models.CharField(unique=True ,max_length=100)
    page_title = models.CharField(max_length=60, default="")
    page_description = models.CharField(max_length=140, default="")
    icon_link = models.CharField(max_length=100, default="")
    num_of_refs = models.IntegerField(default=1)
    keywords_in_it = models.ManyToManyField(Keywords)
    last_scrapped = models.DateTimeField(default=datetime.datetime.min)