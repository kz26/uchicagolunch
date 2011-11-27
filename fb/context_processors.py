from django.conf import settings

def facebook(request):
    return {'fb_app_id': settings.FB_APP_ID}
