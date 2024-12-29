import streamlit as st
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Define API URLs
REST_API_URL = "http://127.0.0.1:8000"
GRAPHQL_API_URL = "http://127.0.0.1:8082/graphql"

# Function to call REST API
def fetch_songs_rest(endpoint: str, params: dict):
    try:
        response = requests.get(f"{REST_API_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# Function to call GraphQL API
def fetch_songs_graphql(query_str: str):
    try:
        transport = RequestsHTTPTransport(url=GRAPHQL_API_URL)
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql(query_str)
        return client.execute(query)
    except Exception as e:
        return {"error": str(e)}

# Streamlit UI
st.title("🎵 Song Recommendation App")
st.sidebar.title("🎶 Choose API")

# Choose between REST or GraphQL
api_choice = st.sidebar.selectbox("Choose API", ["REST", "GraphQL"])

# Select function to call (dropdown)
function_choice = st.selectbox(
    "Choose a function",
    [
        "allSongs",
        "recommendSongs",
        "aggregatedStats",
        "mostPopularSong",
        "longestSong",
        "shortestSong",
        "spotifySongs",
    ],
)

# Get user input for query and limit
if function_choice in ["recommendSongs", "spotifySongs"]:
    query = st.text_input("Enter mood or query", value="happy")
else:
    query = None

limit = st.slider("Limit number of results", 1, 50, 10) if function_choice in ["recommendSongs", "spotifySongs"] else None

# Display button to fetch data
if api_choice == "REST":
    if st.button("🎤 Fetch Data from REST API"):
        with st.spinner("Fetching data..."):
            try:
                # Map user-selected function to backend REST endpoint
                endpoint_mapping = {
                    "allSongs": "songs",
                    "recommendSongs": "recommendations",
                    "aggregatedStats": "aggregated-stats",
                    "mostPopularSong": "most-popular-song",
                    "longestSong": "longest-song",
                    "shortestSong": "shortest-song",
                    "spotifySongs": "spotify/songs",
                }
                
                # Prepare request parameters
                params = {"mood": query, "limit": limit} if query else {"limit": limit}
                
                # Fetch data from the REST API
                data = fetch_songs_rest(endpoint_mapping[function_choice], params)                
                # Handle the response
                if "error" in data:
                    st.error(f"Error: {data['error']}")
                else:
                    st.json(data)  # Display the data in JSON format
                
            except ValueError:
                st.error("Received an invalid response format. Please check the backend implementation.")
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
            
            

elif api_choice == "GraphQL":
    if st.button("🎻 Fetch Data from GraphQL API"):
        with st.spinner("Fetching data..."):
            graphql_queries = {
                "allSongs": """
                query {
                    allSongs {
                        name
                        artist
                        release_date
                        popularity
                        length
                        mood
                    }
                }
                """,
                "recommendSongs": f"""
                query {{
                    recommendSongs(mood: \"{query}\", limit: {limit}) {{
                        name
                        artist
                        release_date
                        popularity
                        length
                        mood
                    }}
                }}
                """,
                "aggregatedStats": """
                query {
                    aggregatedStats 
                }
                """,
                "mostPopularSong": """
                query {
                    mostPopularSong
                }
                """,
                "longestSong": """
                query {
                    longestSong
                }
                """,
                "shortestSong": """
                query {
                    shortestSong
                }
                """,
                "spotifySongs": f"""
                query {{
                    spotifySongs(query: \"{query}\", limit: {limit}) {{
                        name
                        artist
                        release_date
                        popularity
                        length
                        mood
                        acousticness
                        energy
                    }}
                }}
                """,
            }
            query_str = graphql_queries.get(function_choice, "")
            data = fetch_songs_graphql(query_str)
            if "error" in data:
                st.error(f"Error: {data['error']}")
            else:
                st.json(data)
