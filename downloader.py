from yt_dlp import YoutubeDL, DownloadError
import os

def download_video(url, format_id=None):
    chosen_format = "bv+ba/b" if format_id is None else f"{format_id}+ba"

    yt_opts = { "format": chosen_format}
    try:
         with YoutubeDL(yt_opts) as ydl:
            ydl.download([url])
            return "Download Completed!"
    except DownloadError:
        return "Download Error, Invalid URL. Please Insert Correct url"
    
def get_url_info(url):
      try:
        with YoutubeDL() as ydl:
            info = ydl.extract_info(url,download=False)
            
            Title =  info["title"]
            minute = info["duration"]//60
            second = info["duration"]%60
            url_info = {
                "Title": Title,
                "Duration": f"{minute}:{second:02}"
            }
            return url_info
    
      except DownloadError:
        return {"error": "Invalid URL or unable to fetch video info"}
      
def get_video_format(url):
    try:
         with YoutubeDL() as ydl:
            info = ydl.extract_info(url,download=False)
            formats = info["formats"]
    
            video_formats= []
            for fmt in formats:
                if fmt.get("vcodec") != 'none':
                    video_formats.append(fmt)
            videos=[]
            for vformat in video_formats:
                videos.append((vformat["format_id"], vformat.get("resolution"), vformat.get("height")))
            return videos

    except DownloadError:
        return []

def get_top_resolution(video_formats, limit=3):
    sorted_formats = sorted(video_formats, key=lambda item: item[2], reverse=True)

    seen_heights = set()
    top_formats = []

    for fmt in sorted_formats:
        height = fmt[2]
        if height not in seen_heights:
            seen_heights.add(height)
            top_formats.append(fmt)
        if len(top_formats) == limit:
            break

    return top_formats

def download_audio(url):

    yt_opts={
        "format" : "ba",
        "postprocessors" : [{
            "key": "FFmpegExtractAudio",
            "preferredcodec" : "mp3"
        }]
    }
    try:
        with YoutubeDL(yt_opts) as ydl:
            ydl.download([url])
            return "Download Completed!"
    except DownloadError:
        return "Download Error, Invalid URL. Please Insert Correct url"

def get_playlist_info(url):
    ydl_opts = {"extract_flat":True}
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url,download=False)

        playlists=[]
        for deets in info["entries"]:
            if deets.get("duration") is None:
                 vid_info = {
                    "title" : deets.get("title","Unavailable") ,
                    "duration" : "Unavailable",
                    "url" : deets.get("url", "Unavailable")
                }
                 playlists.append(vid_info)
            else:
                minute =deets["duration"]//60
                second = deets["duration"]%60
                title = deets["title"]
                vid_info = {
                    "title" : title,
                    "duration" : f"{minute}:{second:02}",
                    "url" : deets["url"]
                }
                playlists.append(vid_info)

        return playlists
           
    
    except DownloadError:
        return []

def download_playlist(url):
    videos = get_playlist_info(url)
    result =[]
    for video in videos:
        if video["url"] is None or video["url"]=="Unavailable":
            continue
        vid_info={
            "title" : video.get("title"), "result" :  download_video(video["url"])
        }
        result.append(vid_info)
    return result



if __name__ == "__main__":
    link = "https://www.youtube.com/playlist?list=PLFwiwtqJ9Si_uR82Q3LoALjDwEI97a6Cn"
  
    results = download_playlist(link)
    for r in results:
        print(r)
       


   
    