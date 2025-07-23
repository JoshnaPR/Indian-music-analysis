import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import config

print("Testing Spotify API connection...")

# Set up Spotify client
client_credentials_manager = SpotifyClientCredentials(
    client_id=config.SPOTIFY_CLIENT_ID,
    client_secret=config.SPOTIFY_CLIENT_SECRET
)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Test search for Indian music
try:
    results = sp.search(q='Bollywood', type='playlist', limit=5)
    print("Connection successful!")
    print(f"Found {len(results['playlists']['items'])} Bollywood playlists")
    
    # Print first playlist as example
    if results['playlists']['items']:
        first_playlist = results['playlists']['items'][0]
        print(f"Example playlist: {first_playlist['name']}")
        print(f"Followers: {first_playlist['followers']['total']}")
    
    print("\nSpotify API is working perfectly!")
    
except Exception as e:
    print(f"Error: {e}")
    print("Check your credentials in config.py")