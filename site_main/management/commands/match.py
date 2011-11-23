from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from site_main.matcher import *

class Command(BaseCommand):
    help = "Find matches and notify users via email"

    def handle(self, *args, **options):
        clients = Client.objects.filter(matched=False).order_by('?')
        for c in clients:
            if not c.matched:
                m = Matcher(c)
                if m:
                    mo = m.get_match()


