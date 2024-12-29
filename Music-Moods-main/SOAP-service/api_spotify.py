import requests
from typing import List
from SongEntity import Song

class SongAPIUpdater:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def get_access_token(self):
        """
        Fetch an access token from Spotify API using client_id and client_secret.
        """
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            print("Access token fetched successfully")
        else:
            raise Exception(f"Error fetching token: {response.json()}")

    def fetch_songs(self, query="happy", limit=20) -> List[Song]:
    
        #Fetch songs matching a query, removing duplicates and 'Happy' prefix.
        
        if not self.token:
            self.get_access_token()

        # Search tracks
        search_url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"q": query, "type": "track", "limit": min(limit, 50)}

        response = requests.get(search_url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Error in Spotify API request: {response.json()}")

        tracks = response.json()["tracks"]["items"]

        # Use a dictionary to avoid duplicates (keyed by song name + artist)
        unique_songs = {}
        for track in tracks:
            song_id = track["id"]
            song_name = track["name"]
            artist_name = track["artists"][0]["name"]
            
            # Remove 'Happy' prefix if it exists
            if song_name.lower().startswith("happy "):
                song_name = song_name[6:]  # Remove the first 6 characters ('Happy ')

            # Create a unique key based on song name and artist to avoid duplicates
            key = f"{song_name} - {artist_name}"

            if key not in unique_songs:  # Only add if the song is not already in the dictionary
                unique_songs[key] = Song(
                    name=song_name,
                    artist=artist_name,
                    release_date=track["album"]["release_date"],
                    popularity=track["popularity"],
                    length=track["duration_ms"] // 1000,
                    mood="Unknown",  # Placeholder for mood
                    album=track["album"]["name"],  # Placeholder for album name
                    song_id=song_id,  # Use Spotify track ID
                    danceability=None,  # Placeholder for danceability
                    acousticness=None,  # Placeholder for acousticness
                    energy=None,  # Placeholder for energy
                    instrumentalness=None,  # Placeholder for instrumentalness
                    liveness=None,  # Placeholder for liveness
                    valence=None,  # Placeholder for valence
                    loudness=None,  # Placeholder for loudness
                    speechiness=None,  # Placeholder for speechiness
                    tempo=None,  # Placeholder for tempo
                    key=None,  # Placeholder for key
                    time_signature=None  # Placeholder for time signature
                )

        # Return the list of unique songs
        return list(unique_songs.values())
    

 
"""

if __name__ == "__main__":
    # Replace with your Spotify Client ID and Secret
    CLIENT_ID = "12a66723895446c6b727124314fc5d1d"
    CLIENT_SECRET = "842de7c9f2134b50a23efc1b7336e29d"

    # Fetch songs
    updater = SongAPIUpdater(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

try:
    fetched_songs = updater.fetch_songs(query="Happy", limit=20)
    for song in fetched_songs:
        print(f"{song.name} by {song.artist} (Released: {song.release_date})")
except Exception as e:
    print(f"An error occurred: {e}")
"""