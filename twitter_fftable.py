import json
import csv
from time import sleep
import requests
import pandas as pd
from requests_oauthlib import OAuth1Session
import setting


if __name__ == "__main__":
    twitter = OAuth1Session(
        setting.API_KEY, setting.API_SECRET,
        setting.ACCESS_TOKEN, setting.ACCESS_TOKEN_SECRET)
    user_name = input("input user name>>>").rstrip()
    target = input("followers or friends ?>>>").rstrip()
    attributions = [
        "id_str", "name", "screen_name",
        "followers_count", "friends_count",
        "listed_count", "favourites_count",
        "statuses_count", "created_at", "lang", "protected", 
        "default_profile", "default_profile_image",
        "following", "description"
        ]

    cursor = -1
    ids = []
    print("fetching ids...")
    while True:
        param = {
            "count" : 5000,
            "cursor" : cursor,
            "stringify_ids" : True,
            "screen_name" : user_name
            }
        # 15 requests per 15 minutes
        res = twitter.get("https://api.twitter.com/1.1/" + target + "/ids.json",
                          params=param)
        if res.status_code != 200:
            print("request error:" + str(res.status_code))
            break
        else:
            data = json.loads(res.text)
            ids.extend(data["ids"])
            cursor = data["next_cursor"]
        if cursor == 0:
            break
    print("finished!")

    print("fetching user data...")
    with open(user_name + "_" + target + ".csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow([x for x in attributions])
        cursor = -1
        n = int((len(ids)+99) / 100)
        for i in range(n):
            param = {
                "user_id" : ",".join(ids[i*100:i*100 + 100]),
                "tweet_mode" : False
                }
            if i == n - 1:
                param["user_id"] = ",".join(ids[i*100:])
            # 900 requests per 15 minutes (user auth)
            res = twitter.post("https://api.twitter.com/1.1/users/lookup.json",
                               params=param)
            if res.status_code != 200:
                print("request error:" + str(res.status_code))
                break
            else:
                data = json.loads(res.text)
                for user in data:
                    writer.writerow([user[x] for x in attributions])
            print("\r[{0}] {1}/{2}".format("#"*(i+1) + '-'*(n-i-1), i+1, n), end="")
    print("\nfinished!")
