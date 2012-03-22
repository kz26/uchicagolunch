from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from site_main.models import Request
from site_main.emails import notify_expired
from datetime import datetime

class Command(BaseCommand):
    help = "Find expired unmatched requests and notify the users via email" 
    
    def handle(self, *args, **options):
        reqs = Request.objects.filter(expires__lt=datetime.now(), active=True, matched=False, expire_notified=False)
        for r in reqs:
            notify_expired(r)

        reqs.update(expire_notified=True)
