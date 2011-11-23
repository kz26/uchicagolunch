from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from site_main.models import *

class Command(BaseCommand):
    help = "Delete expired entries in the queue"

    def handle(self, *args, **options):
        Client.objects.filter(expires__lte=datetime.now()).delete()
