from yt_dlp import YoutubeDL, DownloadError


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
                videos.append((vformat["format_id"], vformat.get("resolution")))
            return videos

    except DownloadError:
        return []

if __name__ == "__main__":
    link = "https://www.youtube.com/watch?v=wKS_WD2kTc4"
    print(get_video_format(link))

    vid_resolution = input("Pick the format id you want to download (leave blank if highest settings)")

    print(download_video(link,None)) if vid_resolution == "" else  print(download_video(link,vid_resolution))
       


   
    