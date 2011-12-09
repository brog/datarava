from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.template import Context, loader
from django.conf import settings
import httplib
import time
import oauth2 as oauth
import urlparse
import urllib
import json
from django.contrib.auth.decorators import login_required


import logging
logger = logging.getLogger('datarava')

@login_required
def request_token_ready(request):
   
#STEP 3 - Take the info specific to the user and #todo store it.

    if request.method == 'GET':
       # q = json.loads(request)
        user = request.user

        oauth_token = request.GET.get('oauth_token', '')
        withings_userid = request.GET.get('userid', '')
        oauth_verifier = request.GET.get('oauth_verifier', '')

        #let's try to save this data to the user's profile
        user_profile = user.get_profile()
        user_profile.withings_oauth_token = oauth_token
        user_profile.withings_user_id = int(withings_userid)
        user_profile.withings_oauth_verifier = oauth_verifier
        user_profile.save()


        t = loader.get_template('withings/request_token_ready.html')
        c = Context({
            'oauth_token' : oauth_token,
            'oauth_verifier' : oauth_verifier,
            'withings_userid' : withings_userid
        })

    return HttpResponse(t.render(c))

@login_required
def request_token(request):

#STEP 1 - request oauth tokens
    nonce = oauth.generate_nonce()
    timestamp = int(time.time())

    params = {
        'oauth_version': "1.0",
        'oauth_nonce': nonce,
        'oauth_timestamp': timestamp,
        'oauth_consumer_key' : settings.OAUTH_WITHINGS_CONSUMER_KEY,
        'oauth_callback' : settings.OAUTH_WITHINGS_CALLBACK_URL,   
    }
    consumer = oauth.Consumer(key=settings.OAUTH_WITHINGS_CONSUMER_KEY, secret=settings.OAUTH_WITHINGS_CONSUMER_SECRET)

    # Request token URL for withings.
    request_token_url = "%s?oauth_callback=%s" % (settings.OAUTH_WITHINGS_REQUEST_TOKEN_URL, settings.OAUTH_WITHINGS_CALLBACK_URL)

	# Create our client.
    client = oauth.Client(consumer)

	# The OAuth Client request works just like httplib2 for the most part.
    resp, content = client.request(request_token_url, "GET")
 
#STEP 2 - taking the info passed back from the oauth request tokens, build a url to redirect the user to.  The user will return to the /request_token_ready view (as per the callback)
    
    request_token = dict(urlparse.parse_qsl(content))
    oauth_token = request_token['oauth_token']
    oauth_token_secret = request_token['oauth_token_secret']

    authorization_url = settings.OAUTH_WITHINGS_AUTHORIZATION_URL

    token = oauth.Token(key=oauth_token, secret=oauth_token_secret)

    
    params2 = {
        'oauth_callback' : 'http://www.google.com',
        #'oauth_callback' : settings.OAUTH_WITHINGS_CALLBACK_URL, 
        'oauth_version': "1.0",
        'oauth_nonce': nonce,
        'oauth_timestamp': timestamp,
        'oauth_consumer_key' : settings.OAUTH_WITHINGS_CONSUMER_KEY,
        'oauth_token' : oauth_token 
    }

    req = oauth.Request(method="GET", url=authorization_url, parameters=params2)

    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, token)
    req_string = req.to_postdata()

    redirect_url = "%s?oauth_callback=%s&oauth_token=%s" % (authorization_url,'http%3A%2F%2Fwww.themattnicole.com',oauth_token)

    return HttpResponseRedirect("%s?%s" % ( authorization_url,req_string))
