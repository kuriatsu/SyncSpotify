import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pickle
import sys
import subprocess
import os

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="",
                                               client_secret="",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-library-read"))
user = ""
base_dir = ""

def save_song(url):
    # command = ["spotify-ripper", "--flac", "-Q", "320", "-f", "{track_name}.{ext}", "-d", dir, "-l", uri]
    command = ["spotdl", "download", url, "--overwrite skip --scan-for-songs"]
    subprocess.call(command)


def sync(tracks):

    download_list = "" 
    for item in tracks['items']:
        try:
            save_song(item["track"]["external_urls"]["spotify"])
        except Exception as e:
            print(e)

    while tracks['next']:
        tracks = sp.next(tracks)
        for item in tracks['items']:
            try:
                save_song(item["track"]["external_urls"]["spotify"])
            except Exception as e:
                print(e)

def main():

    playlist = "liked" if len(sys.argv) == 1 else sys.argv[1]

    if playlist == "liked":
        tracks = sp.current_user_saved_tracks()
    else:
        tracks = sp.playlist(playlist)["tracks"]

    sync(tracks)

if __name__ == "__main__":
    main()
