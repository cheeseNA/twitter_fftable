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
    
    cursor = -1
    ids = []
    while True:
        param = {
            "count" : 5000,
            "cursor" : cursor,
            "stringify_ids" : True,
            "screen_name" : user_name
            }
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
    print("finish fetching ids")

    with open(user_name + "_" + target + ".csv", "w", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["id", "screen_name", "protected", "friends_count",
                         "followers_count", "name", "lang", "following"])
        cursor = -1
        for i in range(int((len(ids)+99) / 100)):
            param = {
                "user_id" : ",".join(ids[i*100:i*100 + 100]),
                "tweet_mode" : False
                }
            if i == int((len(ids)+99) / 100) - 1:
                param["user_id"] = ",".join(ids[i*100:])
            res = twitter.post("https://api.twitter.com/1.1/users/lookup.json",
                               params=param)
            if res.status_code != 200:
                print("request error:" + str(res.status_code))
                break
            else:
                data = json.loads(res.text)
                for user in data:
                    # a "following" attribute is deprecated
                    writer.writerow([user["id"], user["screen_name"],
                                     user["protected"], user["friends_count"],
                                     user["followers_count"], user["name"],
                                     user["lang"], user["following"]
                                     ])
            print(str(i+1) + "/" + str(int((len(ids)+99) / 100)) + " completed")
    print("finish fetching user data")