import requests
import os
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

AUTH_URL = "https://accounts.spotify.com/api/token"


def get_access_token(client_id, client_secret):

    auth_response = requests.post(
        AUTH_URL,
        {
            "grant_type": "client_credentials",
            "client_id": os.getenv(client_id),
            "client_secret": os.getenv(client_secret),
        },
    )

    auth_response_data = auth_response.json()

    access_token = auth_response_data["access_token"]

    try:

        return access_token
    except KeyError:
        print("Couldn't generate access_token!")


def artist_info(token, artist_id):

    BASE_URL = f"https://api.spotify.com/v1/artists/{artist_id}"

    headers = {"Authorization": "Bearer {token}".format(token=token)}

    r = requests.get(BASE_URL, headers=headers)
    d = r.json()

    artist_name = d["name"]

    try:
        return artist_name
    except KeyError:
        print("Couldn't fetch data!")


def get_top_tracks(token, artist_id):

    BASE_URL = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=ES"

    headers = {"Authorization": "Bearer {token}".format(token=token)}

    r = requests.get(BASE_URL, headers=headers)
    d = r.json()

    tracktitle = []
    trackpic = []
    songpreview = []

    if "error" in d:
        return KeyError

    for track in d["tracks"]:

        tracktitle.append(track["name"])
        trackpic.append(track["album"]["images"][1]["url"])
        songpreview.append(track["preview_url"])

    return (tracktitle, trackpic, songpreview)


def search_id(token, artist_name):

    search_input = artist_name.replace(" ", "%20")

    BASE_URL = f"https://api.spotify.com/v1/search?q={search_input}&type=artist&market=US&limit=1"

    headers = {"Authorization": "Bearer {token}".format(token=token)}

    r = requests.get(BASE_URL, headers=headers)
    d = r.json()

    if "error" in d:
        return KeyError

    artist_id = d["artists"]["items"][0]["id"]

    try:
        return artist_id
    except KeyError:
        return "Couldn't fetch data!"
