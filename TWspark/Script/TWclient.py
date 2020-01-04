import tweepy
import json

class TWclient:
    def __init__(self):
        self.Consumer_API_key = "smkfHwJ7ALgAkrlQIwhjJuOr7"
        self.Consumer_API_secret = "avO6B2ApFHmIPFCgQDMWZLZgYde4cIKF2LKz9P6P64x2jf5Our"
        self.Access_token = "1213382571528089600-BSEAEcCeWi91Ig5CJnPvd7wTaUanyr"
        self.Access_token_secret = "AmcnpoSL5zAA7fcVD6zDUHKDbeZ96stVzC6HgmAmxdnCh"

        self.q = self.get_search_terms()
        self.authorize()

        self.get_api()
        self.get_RTstream()

    def authorize(self):
        self.auth = tweepy.OAuthHandler(self.Consumer_API_key, self.Consumer_API_secret)
        self.auth.set_access_token(self.Access_token, self.Access_token_secret)

    def get_api(self):
        self.api = tweepy.API(self.auth)

    def verify_credential(self):
        pass

    def get_search_terms(self):
        Tlist = input("Query term(s): ").split()
        return Tlist

    def get_RTstream(self):
        self.streamListener = MyStream()
        self.myStream = tweepy.Stream(auth=self.api.auth, listener=self.streamListener)

        try:
            print("start streaming")
            #self.myStream.sample(languages=['en'])
            self.myStream.filter(track=self.q, languages=["en"])

        except KeyboardInterrupt:
            print("stopping")

        finally:
            self.myStream.disconnect()
            print("disconnected")

    def send_to_spark(self):
        pass

class MyStream(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
    """
    def on_data(self, data):
        tweet = json.loads(data)
        print(tweet)
    """
    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        # returning False in on_error disconnects the stream
        print(status_code)
        return True


def main():
    foo = TWclient()


if __name__ == "__main__":
    main()