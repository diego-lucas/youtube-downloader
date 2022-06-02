from tkinter import *
from pytube import YouTube
from urllib.request import urlopen
from PIL import ImageTk, Image
import io
import os
from functools import partial

class Application:
    def __init__(self, master=None):

        global youtube_logo

        self.container1 = Frame(master)
        self.container1["pady"] = 10
        self.container1.pack()

        self.container2 = Frame(master)
        self.container2["padx"] = 10
        self.container2.pack()

        self.container3 = Frame(master)
        self.container3["pady"] = 10
        self.container3["padx"] = 10
        self.container3.pack()

        self.container4 = Frame(self.container3)
        self.container4.grid(row=1,column=2)

        self.container5 = Frame(master)
        self.container5["pady"] = 10
        self.container5["padx"] = 10
        self.container5.pack()

        self.container6 = Frame(master)
        self.container6["pady"] = 10
        self.container6["padx"] = 10
        self.container6.pack()
        
        self.labelLogo = Label(self.container1)
        youtube_logo = PhotoImage(file="images/youtube-logo.png")
        self.labelLogo["image"] = youtube_logo
        self.labelLogo.pack()

        self.labelURL = Label(self.container2)
        self.labelURL["text"] = "Link:"
        self.labelURL["font"] = ("Ubuntu", 14)
        self.labelURL.grid(row=1, column=1, padx=(0, 20))

        self.inputURL = Entry(self.container2)
        self.inputURL["font"] = "Ubuntu"
        self.inputURL["width"] = 50
        self.inputURL.grid(row=1, column=2, padx=(0, 20))

        self.btnSearch = Button(self.container2)
        self.btnSearch["text"] = "Search"
        self.btnSearch["font"] = ("Ubuntu", 14)
        self.btnSearch["width"] = 10
        self.btnSearch.bind("<Button-1>", self.handdle_search)
        self.btnSearch.grid(row=1, column=3)

        self.video_title = Message(self.container4)
        self.video_title["font"] = ("Ubuntu", 15)
        self.video_title["width"] = 500

        self.views_label = Label(self.container4)
        self.views_label["font"] = ("Ubuntu", 12)

        self.media_type = StringVar()
        self.R1 = Radiobutton(
            self.container5,
            text="Video",
            variable=self.media_type,
            value="video",
            command=self.handle_selection,
            font=("Ubuntu",12)
        )
        self.R2 = Radiobutton(
            self.container5,
            text="Audio",
            variable=self.media_type,
            value="audio",
            command=self.handle_selection,
            font=("Ubuntu",12)
        )
        self.media_type.set("video")

        self.input_download_path = Entry(self.container5)
        self.input_download_path["font"] = "Ubuntu"
        self.input_download_path["width"] = 50
        self.input_download_path.insert(0, self.get_download_folder())

        
    def get_download_folder(self):
        user = os.getlogin()
        download_folder = "C:/Users/" + user + "/Downloads"
        return download_folder
        
    def handle_selection(self):
        
        global download_button_image

        if self.media_type.get() == "video":
            self.streams = self.yt.streams.filter(type="video", file_extension="mp4", progressive=True, video_codec="avc1")
        else:
            self.streams = self.yt.streams.filter(type="audio")

        # If container exists, destroy
        try:
            self.streams_container.destroy()
        except:
            pass

        self.streams_container = Frame(self.container6)

        row, column = 1, 1

        download_button_image = PhotoImage(file="images/download-button.png")

        for stream in self.streams:
            
            if column == 5:
                row += 1
                column = 1

            stream_element = Frame(self.streams_container)
            download_button = Button(stream_element, image=download_button_image, compound = RIGHT, padx=10)

            if self.media_type.get() == "video":
                download_button["text"] = stream.resolution
            else:
                download_button["text"] = stream.abr

            download_button["command"] = partial(self.handdle_download, stream.itag)

            download_button.grid(row=1, column=2)
            stream_element.grid(row=row, column=column)

            column += 1

        self.streams_container.grid(row=1, column=1)

    def handdle_download(self, itag):
        stream = self.yt.streams.get_by_itag(itag)
        download_folder = self.input_download_path.get()
        stream.download(download_folder)

    def handdle_search(self, event):

        url = self.inputURL.get().strip()
        self.yt = YouTube(url)

        self.video_title["text"] = self.yt.title

        image_byt = urlopen(self.yt.thumbnail_url).read()
        im = Image.open(io.BytesIO(image_byt))
        im = im.resize((200,150), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
        self.thumbnail_image = Label(self.container3, image=photo)
        self.thumbnail_image.image = photo

        self.views_label["text"] = "{:,}".format(self.yt.views).replace(',','.') + " visualizações"
        
        self.handle_selection()
        self.set_video_visible()

    def set_video_visible(self):

        self.thumbnail_image.grid(row=1,column=1)
        self.video_title.grid(row=1, column=1)
        self.views_label.grid(row=2,column=1, sticky=W)
        self.input_download_path.grid(row=1, column=1)
        self.R1.grid(row=1, column=2)
        self.R2.grid(row=1, column=3)
        self.streams_container.grid(row=2, column=1)


root = Tk()
root.title("YouTube Downloader")
root.iconbitmap("images/favicon.ico")
Application(root)
root.mainloop()