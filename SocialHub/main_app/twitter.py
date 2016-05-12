import requests
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import json



client_key = '1VjKOBZr4k8cRycT05PNyXj2i'
client_secret = 'QIIfKQjaGYdBZB1jL1lzGRgNFXCfk87AyyLr8uliHuPLFsYKSo'


request_token_url = 'https://api.twitter.com/oauth/request_token'
oauth = OAuth1(client_key, client_secret=client_secret)
r = requests.post(url=request_token_url, auth=oauth, data={'oauth_callback': 'http://13.92.250.143:5000/try'})
print r.content
# oauth_token=_4_43gAAAAAAujwTAAABVIx5rOM
# oauth_token_secret=5mnCbUmdKcb93E6h4c4TBcg40xmSTlDG

# go to the url https://api.twitter.com/oauth/authenticate?oauth_token=G-2QegAAAAAAujwTAAABVKGzMY0
# oauth_token=4LzORwAAAAAAujwTAAABVIv1Txs
# oauth_verifier=LFMgLueR1Co0dZ44Igh8z7ACSDlilPW1



# access_token_url = 'https://api.twitter.com/oauth/access_token'
# oauth_token = '_4_43gAAAAAAujwTAAABVIx5rOM'
# oauth_token_secret = '5mnCbUmdKcb93E6h4c4TBcg40xmSTlDG'
# oauth_verifier = 'LFMgLueR1Co0dZ44Igh8z7ACSDlilPW1'
# oauth = OAuth1(client_key=client_key,
#                    client_secret=client_secret,
#                    resource_owner_key=oauth_token,
#                    resource_owner_secret=oauth_token_secret,
#                    verifier=oauth_verifier)
# r = requests.post(url=access_token_url, auth=oauth)
# print r.content
# # oauth_token=718865201123168256-obsAg2PAjpTvaSr70B4UWVybBSAfs5S
# # oauth_token_secret=Wssq0oEU6eNp9whollPlAtiDJZn9nVhz7Keag5tplu3y7
# # user_id=718865201123168256
# # screen_name=keyu_lai
# # x_auth_expires=0




