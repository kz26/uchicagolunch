from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from site_main.matcher import matcher

class Command(BaseCommand):
    help = "Find matches and notify users via email (run this via cron)"

    def handle(self, *args, **options):
        matches = matcher.run()
        if matches:
            self.stdout.write("Matched:\n")
            for m in matches:
                self.stdout.write("\t%s, %s\n" % (m.request1.name, m.request2.name))


