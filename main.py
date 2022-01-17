from bs4 import BeautifulSoup
from config import *
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify Authentication
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=spotify_scope,
        redirect_uri=spotify_redirect_uri,
        client_id=spotify_client_id,
        client_secret=spotify_client_secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

# Scraping Billboard 100
date = input(
    "Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{date}"

response = requests.get(URL)
page_html = response.text
soup = BeautifulSoup(page_html, "lxml")

musics_no_formatted = [item.getText() for item in soup.select(
    selector="li .o-chart-results-list__item h3")]
musics = [i.strip() for i in musics_no_formatted]
print(f"Musics: {musics}")


#---Getting musics URI --------------#
list_uri = []

for music in musics:
    result = sp.search(q=f"{music}", type="track", limit=1)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        list_uri.append(uri)
    except IndexError:
        info = f"{music} does not exist in Spotify. Skipped."

print(f"\nList_URI: {list_uri}")
# print(len(list_uri))


#---- Creating the playlist --------------#
sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100")

playlist_id = sp.user_playlists(user=user_id)["items"][0]["id"]
playlist_url = sp.user_playlist(user=user_id, playlist_id=playlist_id)[
    "external_urls"]

#--------- Adding musics to your playlist -------------#
for uri in list_uri:
    print(f"\nAdding {musics[list_uri.index(uri)]} to your playlist")
    sp.user_playlist_add_tracks(
        user=user_id, playlist_id=playlist_id, tracks=[uri])

print("\nReady!!")
print(f"\nThe link for your playlist is {playlist_url}")
