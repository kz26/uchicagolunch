from django.contrib.sites.models import Site

def current_site_domain(request):
    return {'site_domain': Site.objects.get_current().domain}
