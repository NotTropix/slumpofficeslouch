from pytube import YouTube, Search
import os

def download_music(music):
    # Search for the video
    search_results = Search(music).results

    if len(search_results) > 0:
        # Extract the URL of the first search result
        video_url = "https://www.youtube.com" + search_results[0].watch_url

        # Download the video using pytube
        yt = YouTube(video_url)
        stream = yt.streams.filter(only_audio=True).first()
        music_file = stream.download()

        # Rename the file to have a .mp3 extension
        mp4_filename = music_file.split(".")[0] + ".mp4"
        mp3_filename = music_file.split(".")[0] + ".mp3"
        os.rename(mp4_filename, mp3_filename)

        return mp3_filename
    else:
        return None
