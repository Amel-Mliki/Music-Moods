import csv
from typing import List

from SongEntity import Song

class Loaddata:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.songs: List[Song] = []  # Initialize an empty list for songs

    def load_songs_from_csv(self):
        with open(self.csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Converting necessary columns to appropriate data types
                self.songs.append(Song(
                    name=row['name'],
                    album=row['album'],
                    artist=row['artist'],
                    song_id=row['id'],
                    release_date=row['release_date'],  # You may want to convert this to a datetime object
                    popularity=int(row['popularity']),
                    length=float(row['length']),
                    danceability=float(row['danceability']),
                    acousticness=float(row['acousticness']),
                    energy=float(row['energy']),
                    instrumentalness=float(row['instrumentalness']),
                    liveness=float(row['liveness']),
                    valence=float(row['valence']),
                    loudness=float(row['loudness']),
                    speechiness=float(row['speechiness']),
                    tempo=float(row['tempo']),
                    key=row['key'],  # Convert this to an integer or float if necessary
                    time_signature=row['time_signature'],  # Convert to float if necessary
                    mood=row['mood']
                ))
