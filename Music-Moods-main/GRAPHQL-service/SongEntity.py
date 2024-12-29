class Song:
    def __init__(self, name, artist, release_date, popularity, length, 
                 album, song_id, danceability, 
                 acousticness, energy, instrumentalness, 
                 liveness, valence, loudness, speechiness, 
                 tempo, key, time_signature, mood):
        self.name = name
        self.artist = artist
        self.release_date = release_date
        self.popularity = popularity
        self.length = length
        self.album = album
        self.song_id = song_id
        self.danceability = danceability
        self.acousticness = acousticness
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.liveness = liveness
        self.valence = valence
        self.loudness = loudness
        self.speechiness = speechiness
        self.tempo = tempo
        self.key = key
        self.time_signature = time_signature
        self.mood = mood
        
    def __repr__(self):
        return f"Song(name='{self.name}', artist='{self.artist}', album='{self.album}', release_date='{self.release_date}',popularity='{self.popularity}' , mood='{self.mood}')\n"