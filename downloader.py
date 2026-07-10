from yt_dlp import YoutubeDL

def download_video(url):
    with YoutubeDL() as ydl:
        ydl.download([url])
    return ("Download Complete!")

if __name__ =="__main__":
    download_video("https://www.youtube.com/watch?v=9ijHd0knEww")
