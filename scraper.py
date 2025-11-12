from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# 5FM static page (example)
FIVE_FM_URL = "http://listen.5fm.co.za/listen5fm/"

# Metro FM live stream page (dynamic)
METRO_FM_URL = "https://www.metrofm.co.za/metro-fm/listen-live/"

def get_5fm_nowplaying():
    from requests import get
    from bs4 import BeautifulSoup

    try:
        response = get(FIVE_FM_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        song_element = soup.select_one("#td-player-bar__nowplaying__trackinfo__track-name span")
        artist_element = soup.select_one("#td-player-bar__nowplaying__trackinfo__artist-name span")

        if song_element and artist_element:
            print(f"5FM Now Playing: {artist_element.text.strip()} - {song_element.text.strip()}")
        else:
            print("5FM: No song/artist found")
    except Exception as e:
        print(f"Error fetching 5FM: {e}")

def get_metrofm_nowplaying():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(METRO_FM_URL)
        time.sleep(5)  # wait for page JS to load

        soup = BeautifulSoup(driver.page_source, "html.parser")
        # Update this selector when you see the correct song/artist element
        song_element = soup.select_one(".now-playing-song")
        artist_element = soup.select_one(".now-playing-artist")

        if song_element and artist_element:
            print(f"Metro FM Now Playing: {artist_element.text.strip()} - {song_element.text.strip()}")
        else:
            print("Metro FM: No song/artist found (page might be dynamic)")

        driver.quit()
    except Exception as e:
        print(f"Error fetching Metro FM: {e}")

if __name__ == "__main__":
    get_5fm_nowplaying()
    get_metrofm_nowplaying()
