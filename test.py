def startDownload(link, title, finishLabel, progressBar, progressper):
    url = link.get()
    finishLabel.configure(text="Downloading...")
    last_update = [0]  # Use a mutable type like list to hold the last update value

    def on_progress(stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size
        per = int(percentage_of_completion * 100)

        # Update only every 5%
        if per - last_update[0] >= 5:
            print(f"{per}%")
            last_update[0] = per

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        video = yt.streams.get_highest_resolution()
        title.configure(text=yt.title, fg="white")
        video.download()
        finishLabel.configure(text="Downloaded Successfully")
    except Exception as e:
        finishLabel.configure(text=str(e))