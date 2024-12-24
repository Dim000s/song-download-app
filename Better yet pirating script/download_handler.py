from youtube_search import YoutubeSearch
import yt_dlp

def get_track_ytlink(track_name):
  url = "https://www.youtube.com/watch?v="
  track_id = YoutubeSearch(search_terms=track_name, max_results=1).to_dict()[0]['id']
  track_link = url + track_id
  return track_link

def download_audio(link, path):
  ydl_options = {
  'extract_audio': True,
  'format': 'bestaudio/best',
  'outtmpl': path,
  'quiet': True,
  'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]}
  try:
    with yt_dlp.YoutubeDL(ydl_options) as video:
      print("openend")
      video.download(link)    
  except Exception:
    with open("failed_downloads.txt", '+a') as f:
      print("failed type shi")
      f.write(path)
    return f"Failed in downloading {path}"
  else:
    return f"Downloaded {path}"
