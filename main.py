import tkinter as tk
import customtkinter as ctk
from pytube import YouTube, Playlist
import threading
from tkinter.filedialog import askdirectory


def download_vedio(url,title,finishLabel, progressBar, progressper, resulation,clear_Button,download_cnt):
    try:
        download_cnt.configure(text="0/1")
        download_cnt.update()
        yt = YouTube(url, on_progress_callback= lambda stream, chunk, bytes_remaining: on_progress(stream, chunk, bytes_remaining, progressBar, progressper,clear_Button))
        path=askdirectory(initialdir=".")
        title.configure(text=yt.title, text_color="white")
        title.update()
        video = yt.streams.get_by_resolution(resulation)
        if video is None:
            finishLabel.configure(text="Resulation Does Not Exist", text_color="red")
            finishLabel.update()
            return
        video.download(output_path=path ,filename=yt.title+"_"+resulation+".mp4")
        finishLabel.configure(text="Downloaded Successfully",text_color="green")
        finishLabel.update()
        download_cnt.configure(text="1/1")
        download_cnt.update()
    except Exception as e:
        finishLabel.configure(text="Error: Invalid", text_color="red")
        # print(e)
    finally:
        clear_Button.configure(state=ctk.NORMAL)

def download_playlist(url,title,finishLabel, progressBar, progressper, resulation,clear_Button,download_cnt):
    
    try:
        playlist=Playlist(url)
        urls=playlist.video_urls
        print(urls)
    except Exception as e:
        finishLabel.configure(text="Error: Invalid", text_color="red")
        clear_Button.configure(state=ctk.NORMAL)
        # print(e)
        return
    path=askdirectory(initialdir=".")
    #get all vedios urls
    download_cnt.configure(text="0/"+str(len(urls)))
    for index,surl in enumerate(urls):
        print(index)
        print(surl)
        try:
            finishLabel.configure(text="Downloading...",text_color="white")
            finishLabel.update()
            progressper.configure(text="0%")
            progressper.update()
            progressBar.set(0)
            progressBar.update()
            yt = YouTube(surl, on_progress_callback= lambda stream, chunk, bytes_remaining: on_progress(stream, chunk, bytes_remaining, progressBar, progressper,clear_Button))
            title.configure(text=yt.title, text_color="white")
            title.update()
            video = yt.streams.get_by_resolution(resulation)
            if video is None:
                finishLabel.configure(text="Resulation Does Not Exist", text_color="red")
                finishLabel.update()
                continue
            video.download(output_path=path ,filename=yt.title+"_"+resulation+".mp4")
            finishLabel.configure(text="Downloaded Successfully",text_color="green")
            finishLabel.update()
            download_cnt.configure(text=str(index+1)+"/"+str(len(urls)))
            download_cnt.update()
        except Exception as e:
            finishLabel.configure(text="Error: Invalid", text_color="red")
            # print(e)
    clear_Button.configure(state=ctk.NORMAL)
        

def raise_exception():
    raise Exception("Download Cancelled")

def startDownload(link,title, finishLabel, progressBar, progressper,res_combo,clear_Button,playlist_var,download_cnt):

    clear_Button.configure(state=ctk.DISABLED)
    playlist=playlist_var.get()
    resulation=res_combo.get()
    url=link.get()
    if url=="":
        finishLabel.configure(text="Error: Invalid", text_color="red")
        clear_Button.configure(state=ctk.NORMAL)
        return
    finishLabel.configure(text="Downloading...",text_color="white")
    finishLabel.update()
    progressper.configure(text="0%")
    progressper.update()
    progressBar.set(0)
    progressBar.update()

    #modify clear button
    # clear_Button.configure(text="Cancel",command=raise_exception )

    if playlist==1:
        try:
            thread=threading.Thread(target=download_playlist, args=(url,title,finishLabel,progressBar,progressper,resulation,clear_Button,download_cnt))
            thread.start()
            
        except Exception as e:
            clear_Button.configure(state=ctk.NORMAL)
            finishLabel.configure(text="Error: Invalid", text_color="red")
            # print(e)
    else:
        try:
            thread=threading.Thread(target=download_vedio, args=(url,title,finishLabel,progressBar,progressper,resulation,clear_Button,download_cnt))
            thread.start()
        except Exception as e:
            clear_Button.configure(state=ctk.NORMAL)
            finishLabel.configure(text="Error: Invalid", text_color="red")
        # print(e)

def on_progress(stream, chunk, bytes_remaining, progressBar, progressper,clear_Button):
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
    
    #link - playlist frame
    link_frame = ctk.CTkFrame( app )
    link_frame.pack(padx=10, pady=10)
    # link
    link = tk.StringVar()
    url_var = ctk.CTkEntry( link_frame, width=350, textvariable=link )
    url_var.pack(side=ctk.LEFT,padx=10, pady=10)
    # playlist check box
    playlist_var = tk.IntVar()
    playlist_check = ctk.CTkCheckBox( link_frame, text="Playlist", variable=playlist_var )
    playlist_check.pack(side=ctk.LEFT,padx=10, pady=10)

    # progress bar - download cnt frame
    progress_frame = ctk.CTkFrame( app )
    progress_frame.pack(padx=10, pady=10,fill=tk.X)


    #adding progress bar
    empty_label = ctk.CTkLabel( progress_frame, text="" )
    empty_label.pack(side=ctk.LEFT,padx=160, pady=10)
    progressper=ctk.CTkLabel(progress_frame, text="0%")
    progressper.pack(side=ctk.LEFT,padx=10, pady=10)
    download_cnt = ctk.CTkLabel( progress_frame, text="10/10" )
    download_cnt.pack(side=ctk.RIGHT,padx=10, pady=10)
    progressBar = ctk.CTkProgressBar( app, width=400 )
    progressBar.pack(padx=10, pady=10)
    progressBar.set(0)

    # Combo Box for resolution
    resolutions = ["144p","240p","360p","480p", "720p", "1080p"]
    res_combo = ctk.CTkComboBox( app, values=resolutions )
    res_combo.set("720p")
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
    Button = ctk.CTkButton( button_frame, text="Download", command=lambda : startDownload(link,title,finishLabel,progressBar,progressper,res_combo,clear_Button,playlist_var,download_cnt) )
    Button.pack(side=ctk.LEFT , padx=10, pady=10)


    # Run app
    app.mainloop()

if __name__ == "__main__":
    main()





