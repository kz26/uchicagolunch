from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from site_main.matcher import *
from random import shuffle

class Command(BaseCommand):
    help = "Find matches and notify users via email"

    def handle(self, *args, **options):
        clients = Client.objects.filter(matched=False).values_list('id', flat=True)
        shuffle(list(clients))
        for clid in clients:
            c = Client.objects.get(pk=clid) # force a refresh of the client object, otherwise caching does funny things
            if not c.matched:
                #self.stdout.write("%s is not matched\n" % (c.person.name))
                m = Matcher(c)
                if m:
                    mo = m.get_match()
                    #self.stdout.write("Got match object with %s and %s\n" % (mo.person1.name, mo.person2.name))
            else:
                #self.stdout.write("%s is already matched, skipping\n" % (c.person.name))


