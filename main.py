import tkinter as tk
import customtkinter as ctk
from pytube import YouTube
import threading
from tkinter.filedialog import askdirectory

def download_vedio(url,title,finishLabel, progressBar, progressper, resulation,clear_Button):
    try:
        yt = YouTube(url, on_progress_callback= lambda stream, chunk, bytes_remaining: on_progress(stream, chunk, bytes_remaining, progressBar, progressper))
        video = yt.streams.get_by_resolution(resulation)
        if video is None:
            finishLabel.configure(text="Resulation Does Not Exist", text_color="red")
            finishLabel.update()
            return
        title.configure(text=yt.title, text_color="white")
        title.update()
        path=askdirectory(initialdir=".")
        video.download(output_path=path ,filename=yt.title+"_"+resulation+".mp4")
        finishLabel.configure(text="Downloaded Successfully",text_color="green")
        finishLabel.update()
        clear_Button.configure(state=ctk.NORMAL)
    except Exception as e:
        finishLabel.configure(text="Error: Invalid", text_color="red")
        # print(e)

def startDownload(link,title, finishLabel, progressBar, progressper,res_combo,clear_Button):

    clear_Button.configure(state=ctk.DISABLED)

    resulation=res_combo.get()
    url=link.get()
    finishLabel.configure(text="Downloading...",text_color="white")
    finishLabel.update()
    progressper.configure(text="0%")
    progressper.update()
    progressBar.set(0)
    progressBar.update()

    try:
        thread=threading.Thread(target=download_vedio, args=(url,title,finishLabel,progressBar,progressper,resulation,clear_Button))
        thread.start()
    except Exception as e:
        finishLabel.configure(text="Error: Invalid", text_color="red")
        # print(e)
    # clear_Button.configure(state=ctk.NORMAL)

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

    # Combo Box for resolution
    resolutions = ["360p", "720p", "1080p"]
    res_combo = ctk.CTkComboBox( app, values=resolutions )
    res_combo.pack(padx=10, pady=10)

    finishLabel = ctk.CTkLabel( app, text="" )
    finishLabel.pack(padx=10, pady=10)
    # Download Button
    button_frame = ctk.CTkFrame( app )
    button_frame.pack(padx=10, pady=10)
    # Clear Button
    clear_Button = ctk.CTkButton( button_frame, text="Clear", command=lambda : link.set("") )
    clear_Button.pack(side=ctk.LEFT ,padx=10, pady=10)
    # Download Button
    Button = ctk.CTkButton( button_frame, text="Download", command=lambda : startDownload(link,title,finishLabel,progressBar,progressper,res_combo,clear_Button) )
    Button.pack(side=ctk.LEFT , padx=10, pady=10)





    # Run app
    app.mainloop()

if __name__ == "__main__":
    main()





