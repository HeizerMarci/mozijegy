# rowgrid.py (főprogram)

from customtkinter import *
from PIL import Image, ImageTk
from tkinter import Frame, Label
from tkinter.ttk import Combobox
import os
import subprocess
import temp_data
import sys

set_appearance_mode("dark")

PrimaryColor = "#1E1E2F"
SecondaryColor = "#2C2C3C"
TertiaryColor = "#3C3C4F"
QuaternaryColor = "#E0E0E0"
QuinaryColor = "#00FFF5"

class MovieCard(CTkFrame):
    def __init__(self, master, data, **kwargs):
        super().__init__(master, corner_radius=12, fg_color=TertiaryColor, **kwargs)
        self.data = data
        self.configure(height=200)
        self.grid_propagate(False)
        self.columnconfigure(1, weight=1)

        poster_path = data['image']
        img = Image.open(poster_path).resize((130, 180))
        self.photo = ImageTk.PhotoImage(img)
        poster = CTkLabel(self, image=self.photo, text="")
        poster.grid(row=0, column=0, padx=10, pady=10, rowspan=3)

        title = CTkLabel(self, text=data['title'], font=("Orbitron", 20, "bold"), anchor="w", text_color=QuinaryColor)
        title.grid(row=0, column=1, sticky="w", padx=10)

        info_text = f"{data['rating']} | {data['genre']} | {data['duration']} min | {data['format']}"
        info = CTkLabel(self, text=info_text, font=("Consolas", 13), anchor="w", text_color=QuaternaryColor)
        info.grid(row=1, column=1, sticky="w", padx=10)

        times_frame = CTkFrame(self, fg_color="transparent")
        times_frame.grid(row=2, column=1, sticky="w", padx=10, pady=(0, 10))
        for i, time in enumerate(data['showtimes'].split(',')):
            def make_callback(t=time.strip()):
                return lambda: self.select_movie_time(t)
            time_btn = CTkButton(times_frame, text=time.strip(), width=70, height=30,
                                 font=("Orbitron", 12), fg_color=QuinaryColor,
                                 hover_color="#00D9C0", text_color="black",
                                 corner_radius=30, command=make_callback())
            time_btn.grid(row=0, column=i, padx=5)

    def select_movie_time(self, time):
        selected_movie = {
            "title": self.data['title'],
            "day": self.data['day'],
            "time": time,
            "format": self.data['format'],
            "genre": self.data['genre'],
            "duration": self.data['duration'],
            "terem_szam": 1
        }
        import temp_data
        temp_data.save_data({"selected_movie": selected_movie})
        # Indítjuk a helyfoglaló ablakot
        subprocess.Popen([sys.executable, "ulohelyek.py"])
        self.winfo_toplevel().destroy()

class MovieDisplay(CTkFrame):
    def __init__(self, master, movie_file, **kwargs):
        super().__init__(master, **kwargs)
        self.movie_file = movie_file
        self.movies = self.load_movies()

        days = self.get_unique_days()
        self.day_select = CTkComboBox(self, values=days, command=self.update_display, font=("Segoe UI", 14), state="readonly")
        self.day_select.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.day_select.set(days[0])

        self.scrollable = CTkScrollableFrame(self, fg_color="transparent", width=1100, height=600)
        self.scrollable.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        self.update_display(self.day_select.get())

    def load_movies(self):
        movies = []
        if not os.path.exists(self.movie_file):
            print("Movie file not found!")
            return movies
        with open(self.movie_file, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(";")
                data = {}
                for part in parts:
                    if "=" in part:
                        key, value = part.split("=", 1)
                        data[key.strip()] = value.strip()
                movies.append(data)
        return movies

    def get_unique_days(self):
        days = sorted(set(movie["day"] for movie in self.movies))
        return days if days else ["N/A"]

    def update_display(self, selected_day):
        for widget in self.scrollable.winfo_children():
            widget.destroy()

        filtered = [m for m in self.movies if m["day"] == selected_day]
        for i, movie in enumerate(filtered):
            card = MovieCard(self.scrollable, movie)
            card.pack(padx=10, pady=10, fill="x")

class FilmAblak:
    def __init__(self, cim):
        self.root = CTk(fg_color=PrimaryColor)
        self.root.title(f"{cim}")
        self.root.geometry('1250x1000')
        self.root.minsize(1250, 1000)
        self.root.maxsize(1250, 1000)

        self.kepek = ["./kep3.jpg", "./kep4.jpg", "./kep5.jpg"]
        self.kepekkesz = []
        for img_path in self.kepek:
            img = Image.open(img_path).resize((1000, 250))
            img = ImageTk.PhotoImage(img)
            self.kepekkesz.append(img)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=7)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=18)

        row1 = Frame(self.root, bg=SecondaryColor)
        row1.grid(row=0, column=0, columnspan=3, sticky="nsew")
        Label(row1, text="🎬 ZSOMA Cinema", bg=SecondaryColor, fg="white", font=("Orbitron", 16)).grid(sticky="nsew")

        self.hanyadik = 0
        row2 = Frame(self.root, bg=PrimaryColor)
        row2.grid(row=1, column=0, columnspan=3, sticky="nsew")
        row2.grid_columnconfigure(0, weight=1)
        row2.grid_rowconfigure(0, weight=1)
        self.mylable = Label(row2, image=self.kepekkesz[self.hanyadik], bd=0, bg=PrimaryColor)
        self.mylable.grid(row=0, column=0, sticky="n")

        def kovetkezo(irany):
            if irany == 1:
                self.hanyadik = (self.hanyadik + 1) % len(self.kepekkesz)
            else:
                self.hanyadik = (self.hanyadik - 1) % len(self.kepekkesz)
            self.mylable.config(image=self.kepekkesz[self.hanyadik])

        import threading, time
        def timer():
            while True:
                time.sleep(5)
                self.root.after(0, lambda: kovetkezo(1))

        threading.Thread(target=timer, daemon=True).start()

        row3 = Frame(self.root, bg=SecondaryColor)
        row3.grid(row=2, column=1, columnspan=1, sticky="nsew")
        Label(row3, text="", bg=SecondaryColor, fg="white", font=("Orbitron", 16)).grid(sticky="nsew")

        row4 = CTkFrame(self.root, fg_color=SecondaryColor)
        row4.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)
        row4.grid_propagate(False)
        row4.columnconfigure(0, weight=1)
        row4.rowconfigure(0, weight=1)

        self.movie_display = MovieDisplay(row4, "movies.txt")
        self.movie_display.grid(row=0, column=0, sticky="nsew")

        col1 = CTkFrame(self.root, fg_color=PrimaryColor)
        col1.grid(column=0, row=3, sticky="nsew")
        CTkLabel(col1, text="", text_color=QuinaryColor, font=("Orbitron", 16)).pack(pady=10)

        col2 = CTkFrame(self.root, fg_color=PrimaryColor)
        col2.grid(column=2, row=3, sticky="nsew")
        CTkLabel(col2, text="", text_color=QuinaryColor, font=("Orbitron", 16)).pack(pady=10)

    def futtat(self):
        self.root.mainloop()

def megnyitas():
    app = FilmAblak("VIJOS")
    app.futtat()

if __name__ == "__main__":
    megnyitas()
