import tweepy
import json
import time
import socket


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
        # self.get_search()

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

    def get_search(self, max_tweets=1000):
        self.tweets = []
        last_id = -1
        while len(self.tweets) < max_tweets:
            count = max_tweets - len(self.tweets)
            try:
                new_tweets = self.api.search(q=self.q, count=count, max_id=str(last_id - 1))
                if not new_tweets:
                    break
                self.tweets.extend(new_tweets)
                last_id = new_tweets[-1].id
            except tweepy.TweepError:
                time.sleep(10)

        for tw in self.tweets:
            print(tw.text)


class MyStream(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.sock = create_connection()

    def on_data(self, data):
        tweet = json.loads(data)
        #clean tweet text here
        self.sock.send(tweet["text"].encode('utf-8'))
        #print(tweet)
        time.sleep(3)

    """
    def on_status(self, status):
        print(status.text)
    """

    def on_error(self, status_code):
        # returning False in on_error disconnects the stream
        print(status_code)
        return True


def create_connection():
    host = "localhost"
    port = 5555

    sock = socket.socket()

    sock.bind((host, port))

    print("listening on port: {}".format(str(port)))

    sock.listen(5)
    n_sock, address = sock.accept()

    print("address rx: {}".format(str(address)))
    return n_sock


def main():
    foo = TWclient()


if __name__ == "__main__":
    main()
