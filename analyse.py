import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":
    filename = input("input file name>>>")
    df = pd.read_csv(filename, header=0, encoding="utf-8")
    for lang in df.lang.unique():
        plt.scatter(df.loc[df.lang==lang, "followers_count"],
            df.loc[df.lang==lang, "friends_count"], label=lang)
    plt.legend()
    plt.grid(True)
    # plt.xlim([-10, 100])
    # plt.ylim([-10, 400])
    plt.xlabel("followers_count")
    plt.ylabel("friends_count")
    plt.show()
    '''num = len(unique_lang)
    cdict = {unique_lang[i]: i for i in range(num)}
    df["cmap"] = cdict[df["lang"]]

    df.plot(kind="scatter", x="followers_count", y="friends_count", alpha=0.5,
            figsize=(9, 6), grid=True, c=df["cmap"], cmap="winter")'''