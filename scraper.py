import requests
from bs4 import BeautifulSoup

def fetch_5fm_history_html():
    url = "https://player.listenlive.co/71331/en/songhistory"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.5993.118 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print("Error fetching 5FM page:", e)
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Find song history container (adjust selectors if needed)
    # Inspect the page in browser to confirm structure
    songs = []

    # Example: look for divs/spans containing title and artist
    for item in soup.select(".song-history-item"):  # adjust selector
        title_tag = item.select_one(".song-title")  # adjust selector
        artist_tag = item.select_one(".song-artist")  # adjust selector
        title = title_tag.get_text(strip=True) if title_tag else "Unknown Title"
        artist = artist_tag.get_text(strip=True) if artist_tag else "Unknown Artist"
        songs.append((title, artist))

    if not songs:
        print("No songs found on 5FM page.")
        return

    print("Last songs played on 5FM:\n")
    for title, artist in songs:
        print(f"{title} – {artist}")

if __name__ == "__main__":
    fetch_5fm_history_html()
