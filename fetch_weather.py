import os
import time
import hmac
import hashlib
import json
import urllib.request

# Umgebungsvariablen aus GitHub Secrets laden
API_KEY = os.environ.get("WL_API_KEY")
API_SECRET = os.environ.get("WL_API_SECRET")
STATION_ID = "33008" # Die ID von LSZK

if not API_KEY or not API_SECRET:
    print("Fehler: API Key oder Secret fehlen.")
    exit(1)

# Signatur generieren
timestamp = int(time.time())
msg = f"api-key={API_KEY}&station-id={STATION_ID}&t={timestamp}"
signature = hmac.new(
    API_SECRET.encode('utf-8'), 
    msg.encode('utf-8'), 
    hashlib.sha256
).hexdigest()

url = f"[https://api.weatherlink.com/v2/current/](https://api.weatherlink.com/v2/current/){STATION_ID}?api-key={API_KEY}&t={timestamp}&api-signature={signature}"

# Daten abrufen und in Datei speichern
try:
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        
        # In eine JSON Datei speichern
        with open('lszk_weather.json', 'w') as f:
            json.dump(data, f, indent=4)
            
    print("Wetterdaten erfolgreich aktualisiert und gespeichert.")
except Exception as e:
    print(f"Fehler beim Abruf: {e}")
    exit(1)
