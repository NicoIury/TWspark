import tweepy


class TWclient:
    def __init__(self):
        self.Consumer_API_key = "smkfHwJ7ALgAkrlQIwhjJuOr7"
        self.Consumer_API_secret = "avO6B2ApFHmIPFCgQDMWZLZgYde4cIKF2LKz9P6P64x2jf5Our"
        self.Access_token = "1213382571528089600-BSEAEcCeWi91Ig5CJnPvd7wTaUanyr"
        self.Access_token_secret = "AmcnpoSL5zAA7fcVD6zDUHKDbeZ96stVzC6HgmAmxdnCh"

        self.q = self.get_search_terms()

    def authorize(self):
        self.auth = tweepy.OAuthHandler(self.Consumer_API_key, self.Consumer_API_secret)
        self.auth.set_access_token(self.Access_token, self.Access_token_secret)

    def get_api(self):
        self.api = tweepy.API(self.auth)

    def verify_credential(self):
        pass

    def get_search_terms(self):
        Tlist = input("Query term(s): ")
        return Tlist

    def get_sream(self):
        self.myStream = tweepy.Stream(auth=self.auth, listener=MyStream())
        self.myStream.filter(track=[self.q])

    def send_to_spark(self):
        pass

class MyStream(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.counter = 0
        self.limit = 10

    def on_status(self, status):
        print(status.text)

        self.counter += 1
        if self.counter < self.limit:
            return True
        else:
            return False

    def on_error(self, status_code):
            if status_code == 420:
                # returning False in on_error disconnects the stream
                print(status_code)
                return True


def main():
    foo = TWclient()
    foo.authorize()
    foo.get_sream()


if __name__ == "__main__":
    main()