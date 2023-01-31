from django.db import models

# Create your models here.

class Keywords(models.Model):
    keyword = models.CharField(max_length=100)
    def __str__(self):
        return self.keyword


class Urls(models.Model):
    address = models.CharField(unique=True ,max_length=100)
    num_of_refs = models.IntegerField(default=0)
    keywords_in_it = models.ManyToManyField(Keywords)
    def __str__(self):
        return self.link