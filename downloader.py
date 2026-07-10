from yt_dlp import YoutubeDL, DownloadError

def download_video(url):
    try:
        ydl_opts={
            "format": "bv+ba/b"
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            return "Download Completed!"
    except DownloadError:
        return "Invalid URL"
if __name__ =="__main__":
    result=download_video("https://www.youtube.com/watch?v=k7OooFaXW5Q")
    print(result)