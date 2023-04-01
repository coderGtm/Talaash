'''
The purpose of this script is to normalize the Urls model.
Urls model contains icon_link which field which can be made as a seperate model and the id can be reffered to avoid redundancy
'''
from core.models import Urls, Favicons

def normalize():
    #fetching only those records which have icon_link not equal to ""
    for url in Urls.objects.all().exclude(icon_link=""):
        #fetching the record from Favicons model
        icon = Favicons.objects.filter(icon_link=url.icon_link)
        #if record exists in Favicons model
        if icon:
            #update the icon_link field with the id of the record
            url.icon_link = icon[0].id
            url.save()
        #if record does not exist in Favicons model
        else:
            #create a new record in Favicons model
            icon = Favicons(icon_link=url.icon_link)
            icon.save()
            #update the icon_link field with the id of the record
            url.icon_link = icon.id
            url.save()

if __name__ == "django.core.management.commands.shell":
    normalize()
        