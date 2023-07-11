# SyncSpotfy

## Install
```bash
apt install ffmpeg
pip install spotipy spotdl --upgrade
```

## Setup
1. Be Spotify premium user
2. Go to https://developer.spotify.com/dashboard
3. Create app to get Client ID, Client secret, and set Redirect URIs
4. Set http://localhost:8888/callback as Redirect URIs


## Run
```bash
export CLIENT_ID=<Client ID>
export CLIENT_SECRET=<Client secret>
cd /dir/where/you/want/to/download/playlists
// Download liked songs
python3 sync_spotify.py
// or a specific playlist or album
python3 sync_spotify.py <playlist/album id>
```
