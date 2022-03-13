import tweepy
import json
import time
import socket
import string
import os
import sys
import threading


class TWclient:
    def __init__(self, query, mode):
        self.Consumer_API_key = ""
        self.Consumer_API_secret = ""
        self.Access_token = ""
        self.Access_token_secret = ""

        self.JSON_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "data.json")
        self.old_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "projData", "old")
        self.dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard.py")

        self.q = query.split(",")
        mode = int(mode)

        self.authorize()
        self.get_api()

        if mode == 2:
            threading.Thread(target=self.call_dashboard).start()
            self.get_RTstream()
        elif mode == 1:
            self.get_search()  # no param -> 1000 tw

    def authorize(self):
        self.auth = tweepy.OAuthHandler(self.Consumer_API_key, self.Consumer_API_secret)
        self.auth.set_access_token(self.Access_token, self.Access_token_secret)

    def get_api(self):
        self.api = tweepy.API(self.auth)

    """
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
    """

    def get_RTstream(self):
        self.streamListener = MyStream()
        self.myStream = tweepy.Stream(auth=self.api.auth, listener=self.streamListener, tweet_mode="extended")

        try:
            print("[*] start streaming...")
            # self.myStream.sample(languages=['en'])
            self.myStream.filter(track=self.q, languages=["en"])

        except (KeyboardInterrupt, Exception) as e:
            print("[!] stopping: " + str(e))

        finally:
            self.myStream.disconnect()
            print("[+] disconnected.")

    def call_dashboard(self):
        self.get_platform()

    def get_platform(self):
        plat = sys.platform
        try:
            if plat.startswith("linux"):
                os.system("xterm -hold -e python3  {}".format(self.dashboard_path))
            elif plat.startswith("win"):
                os.system("START cmd /k py -3  {}".format(self.dashboard_path))  # WINDOWS

            elif plat.startswith('darwin'):
                os.system("osascript -e 'tell app \"terminale\" "
                          "to do script \"python3 {}\"'".format(self.dashboard_path))  # MAC OS

            else:
                print("[!] Not a valid system")

        except Exception as e:
            print(e)

    def get_search(self, max_tweets=1000):
        self.refresh_json()
        print("[*] starting tweets' search...")

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
        if not os.path.exists(self.old_data_path):
            os.mkdir(self.old_data_path)

        if os.path.exists(self.JSON_FILE):
            os.rename(self.JSON_FILE, os.path.join(self.old_data_path,
                                                   "oldData" + time.strftime("%Y%m%d-%H%M%S")))
            print("[!] Cleaned old data")

    def build_json(self):
        first = 0
        with open(self.JSON_FILE, "a") as f:
            f.write("[")
        for tw in self.tweets:
            hashatag_list = []
            [hashatag_list.append(item["text"]) for item in tw.entities["hashtags"]]
            # print(tw.coordinates)
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
        if "text" in data:
            tweet = json.loads(data)
            tweet["text"] = clean_punct(tweet["text"])
            if tweet["text"].strip():
                self.sock.send(tweet["text"].encode('utf-8'))

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


def run(argv):
    foo = TWclient(argv[1], argv[2])


run(sys.argv)
