from django.db import models

# Create your models here.

class Keywords(models.Model):
    keyword = models.CharField(max_length=100)
    def __str__(self):
        return self.keyword

class Links(models.Model):
    link_url = models.CharField(max_length=100)
    link_ref_num = models.IntegerField()
    link_keywords = models.ManyToManyField(Keywords)
    def __str__(self):
        return self.link