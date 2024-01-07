import tkinter as tk
import customtkinter as ctk
from pytube import YouTube
import threading

def download_vedio(url,title,finishLabel, progressBar, progressper):
    yt = YouTube(url, on_progress_callback= lambda stream, chunk, bytes_remaining: on_progress(stream, chunk, bytes_remaining, progressBar, progressper))
    video = yt.streams.get_lowest_resolution()
    title.configure(text=yt.title, text_color="white")
    title.update()
    video.download()
    finishLabel.configure(text="Downloaded Successfully",text_color="green")

def startDownload(link,title, finishLabel, progressBar, progressper):
    url=link.get()
    finishLabel.configure(text="Downloading...",text_color="white")
    finishLabel.update()
    progressper.configure(text="0%")
    progressper.update()
    progressBar.set(0)
    progressBar.update()

    try:
        thread=threading.Thread(target=download_vedio, args=(url,title,finishLabel,progressBar,progressper))
        thread.start()
    except Exception as e:
        finishLabel.configure(text="Error: Invalid", text_color="red")
        # print(e)

def on_progress(stream, chunk, bytes_remaining, progressBar, progressper):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_compeletion = bytes_downloaded / total_size
        per = str(int(percentage_of_compeletion*100))+"%"
        progressBar.set(percentage_of_compeletion)
        progressper.configure(text=per)
        progressBar.update()
        progressper.update()


def main():
    # System Settings
    ctk.set_appearance_mode( "System" )
    ctk.set_default_color_theme( "blue" )

    #main app
    app = ctk.CTk()
    app.geometry( "720x480" )
    app.title( "Youtube Downloader" )

    # Adding UI Elements
    title = ctk.CTkLabel( app, text="Insert a youtube link" )
    title.pack( padx=10, pady=10 )
    
    # link
    link = tk.StringVar()
    url_var = ctk.CTkEntry( app, width=350, textvariable=link )
    url_var.pack(padx=10, pady=10)

    #adding progress bar
    progressper=ctk.CTkLabel(app, text="0%")
    progressper.pack(padx=10, pady=10)
    progressBar = ctk.CTkProgressBar( app, width=400 )
    progressBar.pack(padx=10, pady=10)
    progressBar.set(0)

    # Download Button
    finishLabel = ctk.CTkLabel( app, text="" )
    finishLabel.pack(padx=10, pady=10)
    Button = ctk.CTkButton( app, text="Download", command=lambda : startDownload(link,title,finishLabel,progressBar,progressper) )
    Button.pack(padx=10, pady=10)

    # Run app
    app.mainloop()

if __name__ == "__main__":
    main()





