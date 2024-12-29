import requests

class SoapClient:
    def __init__(self, url):
        self.url = url
        self.headers = {"Content-Type": "text/xml; charset=utf-8"}
    
    def send_request(self, action, body):
        """Send a SOAP request."""
        envelope = f"""<?xml version="1.0" encoding="UTF-8"?>
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Body>
                {body}
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>"""
        
        print(f"Sending SOAP request to {self.url} with action {action}...")
        response = requests.post(self.url, data=envelope, headers=self.headers)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Error: {response.status_code}\n{response.text}")
    
    def get_songs(self):
        """Request to get all songs."""
        body = "<GetSongs/>"
        return self.send_request(action="GetSongs", body=body)
    
    def recommend_songs(self, mood, limit):
        """Request to recommend songs."""
        body = f"""
        <RecommendSongs>
            <mood>{mood}</mood>
            <limit>{limit}</limit>
        </RecommendSongs>
        """
        return self.send_request(action="RecommendSongs", body=body)


# Example Usage
if __name__ == "__main__":
    soap_url = "http://127.0.0.1:8082/"
    client = SoapClient(soap_url)
    
    try:
        # Get all songs
        print("Fetching all songs...")
        songs_response = client.get_songs()
        print("Response from GetSongs:\n", songs_response)
        
        # Recommend songs based on mood
        print("\nFetching recommended songs...")
        mood = "happy"
        limit = 3
        recommend_response = client.recommend_songs(mood, limit)
        print("Response from RecommendSongs:\n", recommend_response)
    
    except Exception as e:
        print("Error:", e)
