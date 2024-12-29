from collections import  defaultdict
from typing import List, Tuple
from datetime import date
from SongEntity import Song
from matplotlib import pyplot as plt
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
class songservice:
    
    def __init__(self, songs: List[Song], spotify_client_id: str, spotify_client_secret: str):
        self.songs = songs

        # Spotify authentication
        client_credentials_manager = SpotifyClientCredentials(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
    def get_songs(self) -> List[Tuple[str, str, date, int, float, str]]:
        """
        Returns a list of tuples containing (name, artist, release_date, popularity, length, mood) for each song.
        """
        return [(song.name, song.artist, song.release_date, song.popularity, song.length, song.mood) for song in self.songs if song.name is not None]

    def recommend_songs(self, mood: str, limit : int = None) -> List[Song]:
        """
        Filters songs based on mood and orders them by popularity.
        The comparison is case-insensitive.

        Returns:
            List[Song]: A list of filtered songs sorted by popularity in descending order.
        """
        mood = mood.lower()  # Convert the input mood to lowercase for case-insensitive comparison
        filtered_songs = [song for song in self.songs if song.mood.lower() == mood]

        if filtered_songs:
            # Sort the filtered songs by popularity (descending order)
            filtered_songs.sort(key=lambda song: song.popularity, reverse=True)

        return filtered_songs[:limit] if limit else filtered_songs


    def duration(self, songs: List[Song]) -> str:
        """
        Calculate the total duration of all songs and return it in a human-readable format.
        - If under 60 minutes, return as minutes.
        - If 60 minutes or more, return as 'hrs min s'.
        """
        # Sum the lengths of all songs
        total_seconds = sum(song.length//1000 for song in songs)
        
        # Convert total seconds to hours, minutes, and seconds
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        # Return duration in a readable format
        if hours > 0:
            return f"{int(hours)} hrs {int(minutes)} min {int(seconds)} s"
        elif minutes > 0:
            return f"{int(minutes)} min {int(seconds)} s"
        else:
            return f"{int(seconds)} s"

        
    def acousticness_vs_energy(self):
        """Plot Acousticness vs Energy as a scatter plot."""
        # Convert the list of Song objects to a pandas DataFrame for easier plotting
        data = {
            'acousticness': [song.acousticness for song in self.songs],
            'energy': [song.energy for song in self.songs]
        }
        df = pd.DataFrame(data)

        df.plot(kind='scatter', x='acousticness', y='energy', s=32, alpha=.8)
        plt.gca().spines[['top', 'right']].set_visible(False)  # Remove top and right spines
        plt.xlabel('Acousticness')
        plt.ylabel('Energy')
        plt.title('Acousticness vs Energy')
        plt.show()
        
    
    def latest_songs(self, limit : int = None) -> List[str]:
        """Return a list of the latest songs, sorted by release date."""
        latest = sorted(self.songs, key=lambda x: x.release_date, reverse=True)
        return latest[:limit]
    
    def aggregated_stats_by_mood(self) -> List[str]:
        """Aggregate and return statistics (average values) for each mood."""
        mood_stats = defaultdict(lambda: {'popularity': 0, 'length': 0, 'count': 0})
        
        for song in self.songs:
            mood_stats[song.mood]['popularity'] += song.popularity
            mood_stats[song.mood]['length'] += song.length
            mood_stats[song.mood]['count'] += 1

        aggregated = []
        for mood, stats in mood_stats.items():
            average_popularity = stats['popularity'] / stats['count']
            average_length = stats['length'] / stats['count']
            aggregated.append(f"Stats for {mood} mood:")
            aggregated.append(f"  Average Popularity: {average_popularity:.2f}")
            aggregated.append(f"  Average Length: {average_length:.2f} minutes")
        return aggregated

    
    def most_popular_song(self) -> str:
        """Return the most popular song."""
        most_popular = max(self.songs, key=lambda x: x.popularity)
        return f"Most popular song: {most_popular.name} by {most_popular.artist} (Popularity: {most_popular.popularity})"

    def longest_song(self) -> str:
        """Return the longest song."""
        longest = max(self.songs, key=lambda x: x.length)
        return f"Longest song: {longest.name} by {longest.artist} (Length: {int(((longest.length // 1000) %3600) //60)} minutes)"

    def shortest_song(self) -> str:
        """Return the shortest song."""
        shortest = min(self.songs, key=lambda x: x.length)
        return f"Shortest song: {shortest.name} by {shortest.artist} (Length: {int(((shortest.length // 1000) %3600) //60)} minutes)"
    
    
  
"""  def spotify_recommendations() -> List[Song]: 
        CLIENT_ID = "12a66723895446c6b727124314fc5d1d"
        CLIENT_SECRET = "842de7c9f2134b50a23efc1b7336e29d"

            # Fetch songs
        updater = SongAPIUpdater(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

        try:
            fetched_songs = updater.fetch_songs(query="Happy", limit=20)
            for song in fetched_songs:
                print(f"{song.name} by {song.artist} (Released: {song.release_date})")
        except Exception as e:
            print(f"An error occurred: {e}") """
