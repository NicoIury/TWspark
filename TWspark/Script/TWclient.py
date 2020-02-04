import tweepy
import json
import time
import socket
import string
import os


class TWclient:
    def __init__(self):
        self.Consumer_API_key = "smkfHwJ7ALgAkrlQIwhjJuOr7"
        self.Consumer_API_secret = "avO6B2ApFHmIPFCgQDMWZLZgYde4cIKF2LKz9P6P64x2jf5Our"
        self.Access_token = "1213382571528089600-BSEAEcCeWi91Ig5CJnPvd7wTaUanyr"
        self.Access_token_secret = "AmcnpoSL5zAA7fcVD6zDUHKDbeZ96stVzC6HgmAmxdnCh"

        self.JSON_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "data.json")

        self.q, mode = self.get_input()

        self.authorize()
        self.get_api()

        if mode == 0:
            self.get_RTstream()
        elif mode == 1:
            self.get_search()  # no param -> 1000 tw

    def authorize(self):
        self.auth = tweepy.OAuthHandler(self.Consumer_API_key, self.Consumer_API_secret)
        self.auth.set_access_token(self.Access_token, self.Access_token_secret)

    def get_api(self):
        self.api = tweepy.API(self.auth)

    def verify_credential(self):
        pass

    def get_input(self):
        while 1:
            try:
                mode = int(input("[.] Execute query on real time tweets (0) or historical tweets (1) ?: "))
                if mode in [0, 1]:
                    break
            except ValueError:
                print("[-] invalid argument")

        Tlist = input("[.] Query term(s): ").split()
        return Tlist, mode

    def get_RTstream(self):
        self.streamListener = MyStream()
        self.myStream = tweepy.Stream(auth=self.api.auth, listener=self.streamListener)

        try:
            print("[*] start streaming...")
            # self.myStream.sample(languages=['en'])
            self.myStream.filter(track=self.q, languages=["en"])

        except (KeyboardInterrupt, Exception) as e:
            print("[!] stopping: " + str(e))

        finally:
            self.myStream.disconnect()
            print("[+] disconnected.")

    def get_search(self, max_tweets=10000):
        self.refresh_json()
        print("[*] starting tweets' search...")
        self.clean_json()

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

        self.build_json()

        print("[+] data saved in: " + self.JSON_FILE)

    def refresh_json(self):
        while 1:
            choice = input("[.] Do u want to clean old data? Y/N")
            if choice == "Y":
                if os.path.exists(self.JSON_FILE):
                    os.remove(self.JSON_FILE)
                    print("[!] Deleted old data")
                break
            if choice == "N":
                break
            else:
                print("[-] invalid input")

    def build_json(self):
        first = 0
        with open(self.JSON_FILE, "a") as f:
            f.write("[")
        for tw in self.tweets:
            hashatag_list = []
            [hashatag_list.append(item["text"]) for item in tw.entities["hashtags"]]
            data = {
                "text": tw.text,
                "hashtag_list": hashatag_list,  # filter out empty list
                "time": tw.created_at  # yyyy-mm-dd hh-mm-ss
            }

            with open(self.JSON_FILE, 'a') as f:
                if first != 0:
                    f.write(",")
                json.dump(data, f, ensure_ascii=False, default=str)  # time not serializable

            first = 1

        with open(self.JSON_FILE, "a") as f:
            f.write("]")

    def clean_json(self):
        if os.path.exists(self.JSON_FILE):
            os.remove(self.JSON_FILE)


class MyStream(tweepy.StreamListener):
    def __init__(self):
        super().__init__()
        self.sock = create_connection()

    def on_data(self, data):
        tweet = json.loads(data)
        # print(tweet["text"])
        tweet["text"] = clean_punct(tweet["text"])
        # print(tweet["text"])
        if tweet["text"].strip():
            self.sock.send(tweet["text"].encode('utf-8'))
        # time.sleep(3)

    """
    def on_status(self, status):
        print(status.text)
    """

    def on_error(self, status_code):
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


def clean_punct(text):
    punctList = string.punctuation.replace("#", "").replace("@", "")
    text = "".join([char for char in text if char not in punctList])
    return text


def run():
    foo = TWclient()


if __name__=="__main__":
    run()
