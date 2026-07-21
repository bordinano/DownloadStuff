import customtkinter as ctk
from downloader import (
    get_url_info,
    get_video_format,
    get_top_resolution,
    download_video,
    download_audio,
)
import threading

color_inactive = "blue"
color_active = "green"
dynamic_buttons = []
selected_mode = None

ctk.set_default_color_theme("blue")


def update_info_label():
    url = url_entry.get()
    result = get_url_info(url)
    if "error" in result:
        label.configure(text=result["error"])
    else:
        label.configure(
            text=f"Title: {result['Title']}, \nDuration: {result['Duration']}"
        )
    return url, result


def fetch_mp4info():

    url, result = update_info_label()

    for btn in dynamic_buttons:
        btn.destroy()
    dynamic_buttons.clear()

    if "error" not in result:
        url_format = get_video_format(url)
        top_resolution = get_top_resolution(url_format)
        for index, fmt in enumerate(top_resolution):
            format_id = fmt[0]
            resolution = fmt[1]
            btn = ctk.CTkButton(
                frame,
                text=resolution,
                command=lambda fid=format_id: start_download_video(url, fid)
            )

            btn.place(relx=0.2 + (index * 0.3), rely=0.6, anchor=ctk.CENTER)
            dynamic_buttons.append(btn)


def fetch_mp3info():

    url, result = update_info_label()

    for a_btn in dynamic_buttons:
        a_btn.destroy()
    dynamic_buttons.clear()

    if "error" not in result:
        btn = ctk.CTkButton(
            frame, text="Download Mp3", command=lambda: start_download_audio(url)
        )
        btn.place(relx=0.5, rely=0.6, anchor=ctk.CENTER)
        dynamic_buttons.append(btn)


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

    if selected_mode == 1:
        fetch_mp3info()
    elif selected_mode == 2:
        fetch_mp4info()


def start_download_video(url, fid):
    progress_bar.set(0)
    progress_bar.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    
    def run_download():
        result = download_video(url, fid, progress_hook=gui_progress_hook)
        status_label.configure(text=result)
    thread = threading.Thread(target=run_download)
    thread.start()

def start_download_audio(url):
    progress_bar.set(0)
    progress_bar.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    def run_download():
        result = download_audio(url, progress_hook=gui_progress_hook)
        status_label.configure(text=result)
    thread = threading.Thread(target=run_download)
    thread.start()


def gui_progress_hook(status):
    if status.get("status") == "downloading":
        percent = status.get("_percent")
        progress_bar.set(percent / 100)
    elif status.get("status") == "finished":
        progress_bar.set(1)


app = ctk.CTk()
app.title("Youtube Downloader")
app.geometry("500x400")


frame = ctk.CTkFrame(
    app, width=300, height=500, fg_color="blue", border_color="red", border_width=3
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


app.mainloop()
