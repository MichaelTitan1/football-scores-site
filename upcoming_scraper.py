import requests
import json

# Your site URL on PythonAnywhere
WEBHOOK_URL = "https://michael1.pythonanywhere.com/update-data/"

# Simulated match data (replace this later with real scraping or API logic)
def fetch_fixtures():
    return {
        "upcoming": [
            {
                "team1": "Chelsea",
                "team2": "Arsenal",
                "time": "20:00",
                "status": "NS"
            }
        ],
        "results": [
            {
                "team1": "Man Utd",
                "team2": "Liverpool",
                "score": "2:1",
                "status": "FT"
            }
        ],
        "live": [
            {
                "team1": "Barcelona",
                "team2": "Atletico",
                "score": "1:0",
                "status": "1H"
            }
        ]
    }

def send_to_site(data):
    try:
        res = requests.post(WEBHOOK_URL, json=data)
        print("Sent to website:", res.status_code)
    except Exception as e:
        print("Failed:", e)

if __name__ == "__main__":
    data = fetch_fixtures()
    send_to_site(data)
