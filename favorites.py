import tweepy
from requests import get

def download(url, file_name = None):
    if not file_name:
        file_name = url.split('/')[-1]

    with open(f"./Download/{file_name}", "wb") as file:
        response = get(url)
        file.write(response.content)

api_key = ""
api_secret = ""
access_token = ""
access_secret = ""
target_user_id = ""

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
api = tweepy.API(auth)
favorites = api.get_favorites(user_id = target_user_id, count = 200)
for tweet in favorites:
    print(f"{tweet.id} ", end='')
    if hasattr(tweet, 'extended_entities'):
        print("Downloading...", end='')
        try:
            for entity in tweet.extended_entities['media']:
                download(f"{entity['media_url_https']}")
                print(' Done!')
            api.destroy_favorite(tweet.id)
        except:
            print(' Something wrong with download!')
    else:
        print("This tweet doesn't have media...")
        api.destroy_favorite(tweet.id)