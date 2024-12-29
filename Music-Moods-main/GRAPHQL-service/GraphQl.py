from fastapi import FastAPI
from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from LoadData import Loaddata
from SongService import songservice
from api_spotify import SongAPIUpdater


type_defs = """
type Song {
    name: String!
    artist: String!
    release_date: String!
    popularity: Int!
    length: Int!
    mood: String!
    acousticness: Float
    energy: Float
}

type Query {
    allSongs: [Song!]
    recommendSongs(mood: String!, limit: Int): [Song!]
    aggregatedStats: [String!]
    mostPopularSong: String!
    longestSong: String!
    shortestSong: String!
    spotifySongs(query: String!, limit: Int!): [Song!]
}
"""

query = QueryType()

# Spotify credentials
CLIENT_ID = "12a66723895446c6b727124314fc5d1d"
CLIENT_SECRET = "842de7c9f2134b50a23efc1b7336e29d"
spotify_updater = SongAPIUpdater(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

csv_file_path = "GRAPHQL-service/cleaned_data_moods.csv"
loader = Loaddata(csv_file_path)
loader.load_songs_from_csv()
# Pass the spotify credentials while initializing songservice
song_service = songservice(loader.songs, CLIENT_ID, CLIENT_SECRET)




@query.field("allSongs")
def resolve_all_songs(_, info):
    return song_service.get_songs()

@query.field("recommendSongs")
def resolve_recommend_songs(_, info, mood, limit=None):
    return song_service.recommend_songs(mood, limit)

@query.field("aggregatedStats")
def resolve_aggregated_stats(_, info):
    return song_service.aggregated_stats_by_mood()

@query.field("mostPopularSong")
def resolve_most_popular_song(_, info):
    return song_service.most_popular_song()

@query.field("longestSong")
def resolve_longest_song(_, info):
    return song_service.longest_song()

@query.field("shortestSong")
def resolve_shortest_song(_, info):
    return song_service.shortest_song()

@query.field("spotifySongs")
def resolve_spotify_songs(_, info, query, limit):
    try:
        songs = spotify_updater.fetch_songs(query=query, limit=limit)
        return [
            {
                "name": song.name,
                "artist": song.artist,
                "release_date": song.release_date,
                "popularity": song.popularity,
                "length": song.length,
                "mood": song.mood,
                "acousticness": song.acousticness,
                "energy": song.energy,
            }
            for song in songs
        ]
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)



schema = make_executable_schema(type_defs, query)

app = FastAPI()
app.add_route("/graphql", GraphQL(schema, debug=True))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8082)
