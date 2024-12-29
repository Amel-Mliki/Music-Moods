import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from LoadData import Loaddata
from SongService import songservice
from api_spotify import SongAPIUpdater

from typing import List


app = FastAPI()

# Load songs and initialize the service
csv_file_path = "cleaned_data_moods.csv"
loader = Loaddata(csv_file_path)
loader.load_songs_from_csv()

# Get Spotify credentials from environment variables or config file
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID', '12a66723895446c6b727124314fc5d1d')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', '842de7c9f2134b50a23efc1b7336e29d')

# Initialize songservice with both CSV and Spotify functionality
song_service = songservice(loader.songs, spotify_client_id, spotify_client_secret)


CLIENT_ID = "12a66723895446c6b727124314fc5d1d"
CLIENT_SECRET = "842de7c9f2134b50a23efc1b7336e29d"


@app.get("/spotify/songs")
def get_songs_spotify(query: str = "happy", limit: int = 20):
    """
    REST API endpoint to fetch songs from Spotify.
    """
    try:
        updater = SongAPIUpdater(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        songs = updater.fetch_songs(query=query, limit=limit)
        # Convert Song objects to dictionaries
        return [
            {
                "name": song.name,
                "artist": song.artist,
                "release_date": song.release_date,
                "song_id": song.song_id,
                "album": song.album,
                "mood": song.mood,
                "popularity": song.popularity,
            }
            for song in songs
        ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
 

@app.get("/songs")
def get_songs():
    """Return all songs."""
    return song_service.get_songs()


@app.get("/recommendations")
def get_recommendations(mood: str, limit: int = Query(None, description="Number of recommendations to return")):
    """Return recommended songs based on mood."""
    recommendations = song_service.recommend_songs(mood, limit)
    if recommendations:
        return recommendations
    return JSONResponse(status_code=404, content={"message": "No recommendations found for the given mood."})


@app.get("/duration")
def get_duration():
    """Return the total duration of all songs."""
    total_duration = song_service.duration(song_service.songs)
    return {"total_duration": total_duration}


@app.get("/acousticness-energy")
def acousticness_vs_energy():
    """Generate and show Acousticness vs Energy scatter plot."""
    song_service.acousticness_vs_energy()
    return {"message": "Acousticness vs Energy plot displayed."}


@app.get("/latest-songs")
def get_latest_songs(limit: int = Query(None, description="Number of latest songs to return")):
    """Return the latest songs by release date."""
    latest = song_service.latest_songs(limit)
    return latest


@app.get("/aggregated-stats")
def get_aggregated_stats():
    """Return aggregated statistics by mood."""
    stats = song_service.aggregated_stats_by_mood()
    return stats


@app.get("/most-popular-song")
def most_popular_song():
    """Return the most popular song."""
    songs = {"Response" : song_service.most_popular_song()}
    return JSONResponse(content=songs,status_code=200)


@app.get("/longest-song")
def longest_song():
    """Return the longest song."""
    long = {"Response" : song_service.longest_song()}
    return JSONResponse(content=long,status_code=200)


@app.get("/shortest-song")
def shortest_song():
    """Return the shortest song."""
    short = {"Response":song_service.shortest_song()}
    return JSONResponse(content=short,status_code=200)


@app.get("/recommendations-duration")
def recommendations_duration(mood: str, limit: int = Query(None, description="Number of recommendations to consider")):
    """Return the total duration and list of recommended songs."""
    filtered_list = song_service.recommend_songs(mood, limit)
    duration = song_service.duration(filtered_list)
    return {
        "total_songs": len(filtered_list),
        "total_duration": duration,
        "songs": filtered_list,
    }
    
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)