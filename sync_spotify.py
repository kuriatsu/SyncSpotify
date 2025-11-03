import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pickle
import sys
import subprocess
import os
from pprint import pprint
from mutagen.mp3 import MP3

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                                    client_id=os.environ.get("CLIENT_ID"),
                                    client_secret=os.environ.get("CLIENT_SECRET"),
                                    redirect_uri="http://localhost:8888/callback",
                                    scope="user-library-read",
                                   
                                    )
                    )

def download(url, format):
    # command = ["spotify-ripper", "--flac", "-Q", "320", "-f", "{track_name}.{ext}", "-d", dir, "-l", uri]
    ## when scan and skip
    # command = ["spotdl", "download", url, "--overwrite skip --scan-for-songs"]
    if format == "flac":
        command = ["spotdl", "download", url, "--format flac"]
    else:
        command = ["spotdl", "download", url]

    subprocess.call(command)

def save_song(item, format):
    print("====================")

    ## get file name
    output_mp3_name = f"{item['track']['artists'][0]['name']}"
    if len(item['track']['artists']) == 1:
        output_mp3_name += f" - {item['track']['name']}.{format}" 
    else:
        for artist in item['track']['artists'][1:]:
            output_mp3_name += ", " + artist["name"]
        output_mp3_name += f" - {item['track']['name']}.{format}"


    if not os.path.isfile(output_mp3_name):
        output_mp3_name = f"{item['track']['artists'][0]['name']} - {item['track']['name']}.{format}"

    print(f"{output_mp3_name}")
    is_update = True

    ## judge update or not
    if os.path.isfile(output_mp3_name):
        is_update = False

        expected_duration = item['track']['duration_ms'] * 0.001 
        try:
            actual_duration = MP3(output_mp3_name).info.length
            print(f"current len:{actual_duration}, expected len:{expected_duration}")
            if expected_duration - 5.0 > actual_duration:
                print(f"need to update")
                os.remove(output_mp3_name)
                is_update = True
        except Exception as e:
            print(e)
            print("need to update")
            os.remove(output_mp3_name)
            is_update = True


    if is_update:
        try:
            download(item["track"]["external_urls"]["spotify"], format)
        except Exception as e:
            print(e)

def sync(tracks, format):

    download_list = "" 
    for item in tracks['items']:
        save_song(item, "mp3")

    while tracks['next']:
        tracks = sp.next(tracks)
        for item in tracks['items']:
            save_song(item, format)

def main():

    format = "mp3"
    playlist = "liked" if len(sys.argv) == 1 else sys.argv[1]

    if playlist == "liked":
        tracks = sp.current_user_saved_tracks()
    else:
        tracks = sp.playlist(playlist)["tracks"]

    sync(tracks, format)

if __name__ == "__main__":
    main()
