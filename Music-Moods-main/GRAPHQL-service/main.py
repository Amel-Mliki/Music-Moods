from SongService import songservice
from LoadData import Loaddata
import csv
class Main:
    def __init__(self, csv_path: str, spotify_client_id: str, spotify_client_secret: str):
        # Initialize the loader and load songs from the CSV
        self.loader = Loaddata(csv_path)
        self.loader.load_songs_from_csv()  # Ensure this method loads data into self.loader.songs

        # Pass the loaded songs and Spotify credentials to the songservice constructor
        self.song_service = songservice(self.loader.songs, spotify_client_id, spotify_client_secret)

    def run(self):
        # Step 1: Check if songs are loaded
        """if not self.loader.songs:
            print("No songs found. Exiting program.")
            return

        # Step 2: Display all songs
        print("\nAvailable Songs:")
        songs_list = self.song_service.get_songs()"""
        

        # Step 3: Calculate total duration of all songs
        #total_duration = self.song_service.duration()
        #print(f"\nTotal Duration of All Songs: {total_duration}")
        self.song_service.acousticness_vs_energy()
        print(self.song_service.most_popular_song())
        print(self.song_service.latest_songs(10))
        print(self.song_service.aggregated_stats_by_mood())
        print(self.song_service.longest_song())
        print(self.song_service.shortest_song())
        filtered_list = self.song_service.recommend_songs("Sad",10)
        duration = self.song_service.duration(filtered_list)
        print("Total songs :",len(filtered_list))
        print("Total duration of songs :", duration)
        print("Songs for you", filtered_list)
        
        
       
        
        
        
        
if __name__ == "__main__":
    CLIENT_ID = "12a66723895446c6b727124314fc5d1d"
    CLIENT_SECRET = "842de7c9f2134b50a23efc1b7336e29d"
    # Path to the CSV file
    csv_file_path = "GRAPHQL-service/cleaned_data_moods.csv"
    main_app = Main(csv_file_path,CLIENT_ID,CLIENT_SECRET)
    main_app.run()
