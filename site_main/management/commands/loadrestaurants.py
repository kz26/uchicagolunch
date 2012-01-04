from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from site_main.models import *
from django.utils.encoding import smart_unicode

class Command(BaseCommand):
    help = "Loads restaurants and categories from a file"

    def handle(self, *args, **options):
        if len(args) > 0:
            f = open(args[0], 'r')
            for line in f:
                l = line.rstrip().split('\t')
                if len(l) >= 3:
                    cat = RestaurantCategory.objects.get_or_create(name=l[2])[0]
                    rest = Restaurant.objects.get_or_create(name=l[0], address=l[1], category=cat)
                    if rest[1]:
                        self.stdout.write("Added %s to category %s\n" % (l[0], l[2]))
