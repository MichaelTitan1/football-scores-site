from fastapi import FastAPI, HTTPException
import requests, os, json
from bs4 import BeautifulSoup

PA_URL = "https://michael1.pythonanywhere.com/api/update/upcoming/"
PA_TOKEN = os.getenv("PA_TOKEN")

app = FastAPI()

def scrape_upcoming():
    resp = requests.get("https://livescore.football-data.co.uk/", timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    matches = []
    for h2 in soup.find_all("h2"):
        league = h2.get_text(strip=True)
        table = h2.find_next_sibling("table")
        if not table: continue
        for row in table.select("tbody tr"):
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) < 4: continue
            time, home, status, away = cols[:4]
            matches.append({"league": league,"home": home,"away": away,"time": time,"status": status})
    return matches

@app.get("/scrape/upcoming")
def scrape_and_push():
    try:
        data = {"upcoming": scrape_upcoming()}
        headers = {"X-SCRAPER-TOKEN": PA_TOKEN}
        r = requests.post(PA_URL, json=data, headers=headers, timeout=10)
        r.raise_for_status()
        return {"status": "ok", "sent": len(data["upcoming"])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
