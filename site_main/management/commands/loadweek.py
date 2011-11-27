from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from site_main.models import *
from datetime import timedelta, date

class Command(BaseCommand):
    help = "Inserts dates into the date table (run this at the beginning of each week with cron)"

    def handle(self, *args, **options):
        today = date.today()
        for i in range(settings.DAYS_IN_FUTURE + 7):
            d = today + timedelta(days=i) 
            dobj = Day.objects.get_or_create(date=d)
            if dobj[1]:
                self.stdout.write("Added %s\n" % (d.strftime("%A, %B %d, %Y")))
        
