from http.server import BaseHTTPRequestHandler, HTTPServer
import xml.etree.ElementTree as ET
from LoadData import Loaddata
from SongService import songservice

# Load song data using the loader
loader = Loaddata('cleaned_data_moods.csv')
loader.load_songs_from_csv()

# Initialize the song service with the loaded songs
service = songservice(loader.songs)

class SOAPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Get content length for reading the request body
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Parse SOAP request
        envelope = ET.fromstring(post_data)
        body = envelope.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')

        # Process request based on SOAP action
        response_body = self.process_request(body)

        # Send SOAP response
        self.send_response(200)
        self.send_header('Content-Type', 'text/xml')
        self.end_headers()
        self.wfile.write(response_body.encode())

    def process_request(self, body):
        # Extract the method name from the SOAP request
        method = body[0].tag.split('}')[-1]  # Get the method name after the namespace
        if method == "GetSongs":
            return self.get_songs_response()
        elif method == "RecommendSongs":
            mood = body[0].find("mood").text
            limit = int(body[0].find("limit").text)
            return self.recommend_songs_response(mood, limit)
        else:
            return self.fault_response("Unknown method")

    def get_songs_response(self):
        # Use the song service to get all songs
        songs = service.get_songs()
        response = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Body>
                <GetSongsResponse>
                    {}
                </GetSongsResponse>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>"""
        songs_xml = "".join(
            f"<song><name>{s[0]}</name><artist>{s[1]}</artist><release_date>{s[2]}</release_date></song>"
            for s in songs
        )
        return response.format(songs_xml)

    def recommend_songs_response(self, mood, limit):
        # Use the song service to recommend songs
        songs = service.recommend_songs(mood, limit)
        response = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Body>
                <RecommendSongsResponse>
                    {}
                </RecommendSongsResponse>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>"""
        songs_xml = "".join(
            f"<song><name>{song.name}</name><artist>{song.artist}</artist></song>"
            for song in songs
        )
        return response.format(songs_xml)

    def fault_response(self, message):
        # Generate a SOAP fault response
        return f"""<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Body>
                <SOAP-ENV:Fault>
                    <faultcode>SOAP-ENV:Client</faultcode>
                    <faultstring>{message}</faultstring>
                </SOAP-ENV:Fault>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>"""

# Start the server
if __name__ == "__main__":
    server_address = ('', 8082)
    httpd = HTTPServer(server_address, SOAPHandler)
    print("SOAP server running on http://127.0.0.1:8082")
    httpd.serve_forever()
