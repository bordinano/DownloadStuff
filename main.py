import customtkinter as ctk
from tkinter import filedialog
from downloader import (
    get_url_info,
    get_video_format,
    get_top_resolution,
    download_video,
    download_audio,
    is_playlist,
    get_playlist_info,
)
import threading

color_inactive = "blue"
color_active = "green"
dynamic_widgets = []
selected_mode = None
selected_folder = None
ctk.set_default_color_theme("blue")


def update_info_label():
    url = url_entry.get()
    result = get_url_info(url)
    if "error" in result:
        label.configure(text=result["error"])
    else:
        label.configure(text="")
    return url, result


def fetch_mp4info():

    url, result = update_info_label()

    for btn in dynamic_widgets:
        btn.destroy()
    dynamic_widgets.clear()

    if "error" not in result:
        url_format = get_video_format(url)
        top_resolution = get_top_resolution(url_format)
        card = ctk.CTkFrame(frame, width=260, height=310, fg_color="white")
        card.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        dynamic_widgets.append(card)

        info_label = ctk.CTkLabel(
            card,
            text=f"Title: {result['Title']}\nDuration: {result['Duration']}",
            text_color="black",
            wraplength=240,
            justify="left",
        )
        info_label.pack(pady=10, padx=10)
        for index, fmt in enumerate(top_resolution):
            format_id = fmt[0]
            resolution = fmt[1]
            btn = ctk.CTkButton(
                card,
                text=resolution,
                width=70,
                command=lambda fid=format_id: start_download_video(url, fid),
            )

            btn.pack(side="left", padx=5, pady=10)


def fetch_mp3info():

    url, result = update_info_label()

    for a_btn in dynamic_widgets:
        a_btn.destroy()
    dynamic_widgets.clear()

    if "error" not in result:
        card = ctk.CTkFrame(frame, width=380, height=160, fg_color="white")
        card.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        dynamic_widgets.append(card)

        top_row = ctk.CTkFrame(card, fg_color="white")
        top_row.pack(fill="x", pady=10, padx=10)

        info_label = ctk.CTkLabel(
            top_row,
            text=f"Title: {result['Title']}\nDuration: {result['Duration']}",
            text_color="black",
            wraplength=240,
            justify="left",
        )
        info_label.pack(side="left")

        btn = ctk.CTkButton(
            top_row,
            width=30,
            text="Download",
            command=lambda: start_download_audio(url),
        )
        btn.pack(side="right", padx=10)


def box_callback(button_number):
    global selected_mode
    mp3_btn.configure(fg_color=color_inactive)
    mp4_btn.configure(fg_color=color_inactive)

    if button_number == 1:
        mp3_btn.configure(fg_color=color_active)
    elif button_number == 2:
        mp4_btn.configure(fg_color=color_active)

    selected_mode = button_number


def conversion():
    url = url_entry.get()
    playlist = is_playlist(url)
    if selected_mode == 1:
        if playlist:
            fetch_playlist_info(url, audio_mode=True)
        else:
            fetch_mp3info()
    elif selected_mode == 2:
        if playlist:
            fetch_playlist_info(url, audio_mode=False)
        else:
            fetch_mp4info()


def start_download_video(url, fid=None):
    progress_bar.set(0)
    progress_bar.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def run_download():
        result = download_video(
            url, fid, progress_hook=gui_progress_hook, download_path=selected_folder
        )
        status_label.configure(text=result)

    thread = threading.Thread(target=run_download)
    thread.start()


def start_download_audio(url):
    progress_bar.set(0)
    progress_bar.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    def run_download():
        result = download_audio(
            url, progress_hook=gui_progress_hook, download_path=selected_folder
        )
        status_label.configure(text=result)

    thread = threading.Thread(target=run_download)
    thread.start()

def start_download_playlist(url,audio_mode):
    progress_bar

def gui_progress_hook(status):
    if status.get("status") == "downloading":
        percent = status.get("_percent")
        progress_bar.set(percent / 100)
    elif status.get("status") == "finished":
        progress_bar.set(1)


def select_folder():
    global selected_folder
    folder = filedialog.askdirectory()
    if folder != "":
        selected_folder = folder


def fetch_playlist_info(url, audio_mode):
    for widget in dynamic_widgets:
        widget.destroy()
    dynamic_widgets.clear()
    videos = get_playlist_info(url)

    scroll_frame = ctk.CTkScrollableFrame(
        frame, width=380, height=300, fg_color="white"
    )
    scroll_frame.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)
    dynamic_widgets.append(scroll_frame)

    for video in videos:
        row = ctk.CTkFrame(
            scroll_frame,
            fg_color="white",
            border_color="gray70",
            border_width=2,
            corner_radius=10,
        )
        row.pack(fill="x", pady=8, padx=8)

        row_label = ctk.CTkLabel(
            row,
            text=f"{video['title']} ({video['duration']})",
            text_color="black",
            wraplength=200,
            justify="left",
        )
        row_label.pack(side="left", padx=10, pady=15)
        if audio_mode:
            btn = ctk.CTkButton(
                row,
                width=30,
                text="Download",
                command=lambda vurl=video["url"]: start_download_audio(vurl),
            )
            btn.pack(side="right", padx=10)

        else:
            btn = ctk.CTkButton(
                row,
                width=30,
                text="Download",
                command=lambda vurl=video["url"]: start_download_video(vurl, None),
            )
            btn.pack(side="right", padx=10)
    if audio_mode:
        download_all = ctk.CTkButton(
            frame,
            text="Download All",
            command=lambda vurl=video["url"]: start_download_audio(vurl),
        )
        download_all.pack()
    else:
        download_all = ctk.CTkButton(
            frame,
            text="Download All",
            command=lambda vurl=video["url"]: start_download_video(vurl, None),
        )
        download_all.pack()


app = ctk.CTk()
app.title("Youtube Downloader")
app.geometry("480x650")


frame = ctk.CTkFrame(
    app, width=440, height=610, fg_color="blue", border_color="red", border_width=3
)
frame.pack(padx=20, pady=20)

mp3_btn = ctk.CTkButton(frame, text="MP3", command=lambda: box_callback(1), height=35)
mp3_btn.place(relx=0.25, rely=0.1, anchor=ctk.CENTER)

mp4_btn = ctk.CTkButton(frame, text="MP4", command=lambda: box_callback(2), height=35)
mp4_btn.place(relx=0.75, rely=0.1, anchor=ctk.CENTER)

url_entry = ctk.CTkEntry(frame, placeholder_text="Paste the URL here")
url_entry.place(relx=0.25, rely=0.2, anchor=ctk.CENTER)

convert = ctk.CTkButton(
    frame,
    text="CONVERT",
    command=conversion,
    corner_radius=10,
    width=15,
    height=30,
)
convert.place(relx=0.75, rely=0.2, anchor=ctk.CENTER)

label = ctk.CTkLabel(
    frame, text="Video will appear here", wraplength=260, justify="left"
)
label.place(relx=0.5, rely=0.35, anchor=ctk.CENTER)

status_label = ctk.CTkLabel(frame, text="", wraplength=260, justify="left")
status_label.place(relx=0.5, rely=0.7, anchor=ctk.CENTER)

progress_bar = ctk.CTkProgressBar(frame)
progress_bar.set(0)
progress_bar.place_forget()


folder_btn = ctk.CTkButton(frame, text="Choose Folder", command=select_folder)
folder_btn.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)


app.mainloop()
