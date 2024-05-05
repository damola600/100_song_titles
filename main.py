import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


SPOTIFY_CLIENT_ID = "d449cdc5c95a4ff581df82b343c23990"
SPOTIFY_CLIENT_SECRET = "d912442ae3284631855dbbede15f9f99"
URL = "https://www.billboard.com/charts/hot-100"
REDIRECT_URI = "http://example.com"
SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/users/31r4evqfnx6oaxufvxwc2z33q3uu"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]
response = requests.get(f"{URL}/{date}")

billboard_webpage = response.text

song_uri = []
soup = BeautifulSoup(billboard_webpage, "html.parser")
titles = [title.getText().strip() for title in soup.select("li ul li h3")]
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope="playlist-modify-private"))
user_id =sp.current_user()["id"]
print(user_id)
for song in titles:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. SKipped.")

playlist_name = f"{date} Billboard 100"
playlist = sp.user_playlist_create(user=user_id, name=playlist_name, public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uri)