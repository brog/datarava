"""
The MIT License

Copyright (c) 2007 Leah Culver

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Example consumer. This is not recommended for production.
Instead, you'll want to create your own subclass of OAuthClient
or find one that works with your web framework.
"""

import httplib
import time
import oauth2 as oauth

# settings for the local test consumer
SERVER = 'localhost'
PORT = 8000

# fake urls for the test server (matches ones in server.py)
REQUEST_TOKEN_URL = 'https://oauth.withings.com/account/request_token'
ACCESS_TOKEN_URL = 'https://oauth.withings.com/account/access_token'
AUTHORIZATION_URL = 'https://oauth.withings.com/account/authorize'
CALLBACK_URL = 'http://192.168.2.7:8000/request_token_ready'
RESOURCE_URL = 'http://photos.example.net/photos'

# key and secret granted by the service provider for this consumer application - same as the MockOAuthDataStore
CONSUMER_KEY = '1e010b6eb501002ededd305c020f776dc0d74d2947ebb1ee37321589bc5785'
CONSUMER_SECRET = '9c63ee28b58bccf497c019e1b9e83d73e2c263f6ed7ffb9d82f966597eb36'

# Set the API endpoint 
url = "http://example.com/photos"

# Set the base oauth_* parameters along with any other parameters required
# for the API call.

#https://oauth.withings.com/account/request_token?
#oauth_callback=http%3A%2F%2F192.168.2.7:8000%2Frequest_token_ready
#&oauth_consumer_key=consumer_key
#&oauth_nonce=oauth.generate_nonce()
#&oauth_signature=J8xzgFtHTsSRw8Ejc8UDV2jls34%3D
#&oauth_signature_method=HMAC-SHA1
#&oauth_timestamp=int(time.time())
#&oauth_version=1.0



params = {
    'oauth_version': "1.0",
    'oauth_nonce': oauth.generate_nonce(),
    'oauth_timestamp': int(time.time()),
    'oauth_consumer_key' : CONSUMER_KEY,
    'oauth_callback' : CALLBACK_URL,   
}


# Set up instances of our Token and Consumer. The Consumer.key and 
# Consumer.secret are given to you by the API provider. The Token.key and
# Token.secret is given to you after a three-legged authentication.

token = oauth.Token(key="tok-test-key", secret="tok-test-secret")
consumer = oauth.Consumer(key="con-test-key", secret="con-test-secret")

# Set our token/key parameters

#params['oauth_token'] = token.key
#params['oauth_consumer_key'] = consumer.key

# Create our request. Change method, etc. accordingly.

#req = oauth.Request(method="GET", url=REQUEST_TOKEN_URL, parameters=params)

# Sign the request.
#signature_method = oauth.SignatureMethod_HMAC_SHA1()
#req.sign_request(signature_method, consumer, token)

# Create your consumer with the proper key/secret.
consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)

# Request token URL for Twitter.
request_token_url = REQUEST_TOKEN_URL

# Create our client.
client = oauth.Client(consumer)

# The OAuth Client request works just like httplib2 for the most part.
resp, content = client.request(request_token_url, "GET")
print resp
print "\n\n"
print content



