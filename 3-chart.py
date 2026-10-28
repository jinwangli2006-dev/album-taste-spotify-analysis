import re
import pandas as pd
import matplotlib.pyplot as plt

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
cand = df[df["album_key"].isin(set(seed["album_key"]))]
mask = [any((ak, ar) in pairs for ar in al) for ak, al in zip(cand["album_key"], cand["artist_list"])]
mine = cand[mask]

# Chart 1: mean audio features, your albums vs all tracks
cols = ["energy", "acousticness", "valence", "danceability", "speechiness"]
out = pd.DataFrame({"Your albums": mine[cols].mean(), "All tracks": df[cols].mean()})
out.plot(kind="bar", figsize=(8, 5), color=["#1db954", "#999999"])
plt.title("Audio profile: my reviewed albums vs. all Spotify tracks")
plt.ylabel("Mean value (0-1)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart_features.png", dpi=150)
plt.close()

# Chart 2: energy distribution
plt.figure(figsize=(8, 5))
plt.hist(df["energy"], bins=30, density=True, alpha=0.5, label="All tracks", color="#999999")
plt.hist(mine["energy"], bins=30, density=True, alpha=0.6, label="Your albums", color="#1db954")
plt.title("Energy distribution")
plt.xlabel("Energy")
plt.legend()
plt.tight_layout()
plt.savefig("chart_energy.png", dpi=150)
print("Saved chart_features.png and chart_energy.png")
