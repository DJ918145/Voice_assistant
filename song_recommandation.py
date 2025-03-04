import re
import requests
import vlc
import time
import yt_dlp
from youtubesearchpython import VideosSearch

# Your SerpAPI Key
SERPAPI_KEY = "910235f97337b5c8ebdcc958c54d95b36df07239a6848204620004b8391cd896"

def extract_song_name(user_input):
    """
    Extracts the song name from user input.
    Example: "Play Ve Mahi"
    """
    match = re.search(r"play (.+)", user_input, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def search_youtube(song_name):
    """
    Searches YouTube for the song and returns the video URL.
    """
    search = VideosSearch(song_name, limit=1)
    result = search.result()
    
    if "result" in result and len(result["result"]) > 0:
        video_url = "https://www.youtube.com/watch?v=" + result["result"][0]["id"]
        return video_url
    
    return None  # If no video found

def get_youtube_recommendations(song_name):
    """
    Fetches similar song recommendations from YouTube via SerpAPI.
    """
    search_query = f"Songs similar to {song_name} site:youtube.com"
    
    url = "https://serpapi.com/search"
    params = {
        "q": search_query,
        "engine": "google",
        "api_key": SERPAPI_KEY
    }

    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("❌ API Request Failed!")
        return []

    data = response.json()

    recommendations = []
    for result in data.get("organic_results", []):
        video_title = result.get("title")
        video_link = result.get("link")
        if video_title and video_link:
            recommendations.append(video_link)

    return recommendations[:3]  # Return top 3 recommended songs

def play_song(video_url):
    """
    Downloads the YouTube video audio and plays it using yt-dlp.
    """
    print(f"🎵 Playing: {video_url}")

    # yt-dlp options to download only audio
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'current_song.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Download the song
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    # Play using VLC
    player = vlc.MediaPlayer("current_song.mp3")
    player.play()

    # Wait a bit to ensure playback starts
    time.sleep(2)

    # Wait until the song finishes
    while player.is_playing():
        time.sleep(1)

def recommandation(user_input):
    # user_input = input("You: ")
    song_name = extract_song_name(user_input)

    if song_name:
        print(f"\n🎶 Playing '{song_name}'...\n")
        
        # Search and play the requested song
        video_url = search_youtube(song_name)
        if video_url:
            play_song(video_url)
            
            # Get recommendations after the song finishes
            recommendations = get_youtube_recommendations(song_name)
            if recommendations:
                print("\n🎵 Suggested next song:")
                next_song = recommendations[0]  # Play the first recommended song
                play_song(next_song)
            else:
                print("❌ No recommendations found.")
        else:
            print("❌ Could not find the song on YouTube.")
    else:
        print("❌ Please specify a song name in your request.")

if __name__ == "__main__":
    recommandation()
