import urllib
from django.conf import settings
from django.core import urlresolvers
from django.views import generic as generic_views

GOOGLE_SCOPE = 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'

class GoogleLoginView(generic_views.RedirectView):
    """
    This view authenticates the user via Google.
    """

    permanent = False

    def get_redirect_url(self, **kwargs):
        args = {
            'hd': settings.GOOGLE_APPS_DOMAIN,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'scope': GOOGLE_SCOPE,
            'redirect_uri': self.request.build_absolute_uri(urlresolvers.reverse('google_callback')),
            'response_type': 'code',
            'access_type': 'online',
            'approval_prompt': 'auto',
        }
        return 'https://accounts.google.com/o/oauth2/auth?%s' % urllib.urlencode(args)