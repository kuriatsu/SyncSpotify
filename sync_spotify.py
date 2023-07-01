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


def sync(tracks, playlist_name):

    download_list = "" 
    for item in tracks['items']:
        try:
            print("save: " + str(item["track"]["name"].encode("ascii")))
            # download_list += str(item["track"]["external_urls"]["spotify"]) + " "
            save_song(item["track"]["external_urls"]["spotify"])
        except Exception as e:
            print(e)

    while tracks['next']:
        tracks = sp.next(tracks)
        for item in tracks['items']:
            try:
                print("save: " + str(item["track"]["name"].encode("ascii")))
                # download_list += str(item["track"]["external_urls"]["spotify"]) + " "
                save_song(item["track"]["external_urls"]["spotify"])
            except Exception as e:
                print(e)



def sync_playlist(tracks, playlist_name, max=-1):
    music_dir = base_dir + playlist_name + "/"
    db_name = base_dir + playlist_name + ".pickle"
    print("dir: " + music_dir)

    if os.path.exists(db_name):
        with open(db_name, "rb") as f:
            db = pickle.load(f)
    else:
        db = []

    if len(db) == 0:
        current_uris = []
    else:
        print(len(db))
        current_uris = [item['track']['uri'] for item in db]

    download_list = []
    exception_list = []
    count = len(tracks)

    for item in tracks['items']:
        if item['track']['uri'] not in current_uris:
            try:
                print("save: " + item["track"]["name"].encode("ascii"))
                download_list.append(item['track']['uri']+"\n")
            except Exception as e:
                exception_list.append(item['track']['uri']+"\n")
                print(e)

            db.append(item)

    while tracks['next']:
        tracks = sp.next(tracks)
        count += len(tracks["items"])
        for item in tracks['items']:
            if item['track']['uri'] not in current_uris:
                try:
                    print("save: " + item["track"]["name"].encode("ascii"))
                    download_list.append(item['track']['uri']+"\n")
                except Exception as e:
                    print(e)
                    exception_list.append(item['track']['uri']+"\n")

                db.append(item)

        if max != -1 and count > max:
            break

    # with open("download_list.txt", "w") as f:
    #     f.writelines(download_list)

    # save_songs("download_list.txt", music_dir)

    # with open("exception_list.txt", "w") as f:
    #     f.writelines(exception_list)

    # save_exception_songs("exception_list.txt", music_dir)

    # with open(db_name, "wb") as f:
    #     pickle.dump(db, f)


def main():

    playlist = "liked" if len(sys.argv) == 1 else sys.argv[1]
    if playlist == "liked":
        tracks = sp.current_user_saved_tracks()
        sync(tracks, "liked")
    else:
        tracks = sp.playlist(playlist)
        print(tracks["tracks"].keys())
        sync_playlist(tracks["tracks"], tracks["name"], 100)


if __name__ == "__main__":
    main()
