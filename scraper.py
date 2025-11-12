import requests

def fetch_5fm_history():
    url = "https://player.listenlive.co/71331/en/songhistory"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.5993.118 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # raise an error if request failed
    except requests.RequestException as e:
        print("Error fetching 5FM history:", e)
        return

    # Preview response to debug if it's not JSON
    if not response.text.strip():
        print("Empty response from 5FM endpoint.")
        return
    if not response.text.strip().startswith("{"):
        print("Unexpected response format (not JSON):")
        print(response.text[:500])  # show first 500 characters
        return

    try:
        data = response.json()
    except ValueError as e:
        print("Failed to decode JSON:", e)
        print("Response preview:", response.text[:500])
        return

    songs = data.get('songs', [])
    if not songs:
        print("No song/artist currently found for 5FM")
        return

    print("Last songs played on 5FM:\n")
    for s in songs:
        title = s.get('title', 'Unknown Title')
        artist = s.get('artist', 'Unknown Artist')
        print(f"{title} – {artist}")

if __name__ == "__main__":
    fetch_5fm_history()
