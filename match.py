import re
import pandas as pd

def norm(s):
    s = str(s).lower()
    s = re.sub(r"[\(\[].*?[\)\]]", " ", s)
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(s.split())

df = pd.read_csv("dataset.csv").drop_duplicates("track_id")
seed = pd.read_csv("album_reviews_seed.csv", encoding="utf-8-sig")

df["album_key"] = df["album_name"].map(norm)
seed["album_key"] = seed["album"].map(norm)
seed["artist_key"] = seed["artist"].map(norm)

df["artist_list"] = df["artists"].fillna("").map(lambda a: {norm(x) for x in a.split(";")})

pairs = set(zip(seed["album_key"], seed["artist_key"]))
albums = set(seed["album_key"])
cand = df[df["album_key"].isin(albums)]
mask = [any((ak, ar) in pairs for ar in al) for ak, al in zip(cand["album_key"], cand["artist_list"])]
matched = cand[mask]

found = {(ak, ar) for ak, al in zip(matched["album_key"], matched["artist_list"]) for ar in al} & pairs
print("Albums in your list:", len(pairs))
print("Albums matched:", len(found), "| tracks matched:", len(matched))
print("Not matched:", sorted(seed[[(a, r) not in found for a, r in zip(seed["album_key"], seed["artist_key"])]]["album"]))

cols = ["energy", "acousticness", "valence", "danceability", "speechiness", "tempo"]
out = pd.DataFrame({"your_albums": matched[cols].mean(), "all_dataset": df[cols].mean()})
print(out.round(3))
