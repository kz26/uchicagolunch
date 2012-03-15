from site_main.models import *
from site_main.emails import *
from datetime import datetime, timedelta, date, time
import edmonds
from random import choice

# find and process matches
# returns a list of newly created Match objects
def run():
    # retrieve a list of unfilled requests
    def getRequests():
        reqs = Request.objects.filter(expires__gt=datetime.now(), matched=False, active=True)
        rl = {}
        for r in reqs:
            r_id = r.pk
            r_dates = set(r.day_set.all().values_list('date', flat=True))
            r_prefs = set(r.restaurant_prefs.all().values_list('pk', flat=True))
            rl[r_id] = (r_dates, r_prefs)
        return rl

    # create a graph from the above
    # dictionary key: request ID
    # dictionary value: compatible request IDs
    def createGraph(rl):
        g = {}
        for k1, v1 in rl.iteritems():
            if k1 not in g:
                g[k1] = []
            for k2, v2 in rl.iteritems():
                if k2 == k1: continue
                if not v2[0].isdisjoint(v1[0]) and not v2[1].isdisjoint(v1[1]):
                    g[k1].append(k2)
        return g

    # runs Edmond's matching algorithm on the input graph
    def findMatches(g):
        return edmonds.matching(g)

    reqs = getRequests()
    g = createGraph(reqs)
    matches = findMatches(g)
    matched = []
    results = []

    for k, v in matches.iteritems():
        if k in matched or v in matched: continue
        req1 = reqs[k]
        req2 = reqs[v]
        suggested_day = choice(tuple(req1[0].intersection(req2[0])))
        suggested_date = datetime.combine(suggested_day, time(12)) + timedelta(minutes=choice(range(0, 135, 15)))
        suggested_rc = choice(tuple(req1[1].intersection(req2[1])))
        suggested_rest = choice(list(Restaurant.objects.filter(category__pk=suggested_rc)))

        reqo1 = Request.objects.get(pk=k)
        reqo2 = Request.objects.get(pk=v)

        mo = Match.objects.create(request1=reqo1, request2=reqo2, location=suggested_rest, date=suggested_date)
        notify_match(mo)
        for r in (reqo1, reqo2):
            r.matched = True
            r.save()
        
        matched.extend((k, v)) 
        results.append(mo)

    return results
