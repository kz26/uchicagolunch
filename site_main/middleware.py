from models import IPBan
from django.http import HttpResponseForbidden

class IPBanMiddleware:
    def process_request(self, request):
        if IPBan.objects.filter(ip=request.META['REMOTE_ADDR']).exists():
            return HttpResponseForbidden("<h1>Forbidden</h1>") 
        return None
