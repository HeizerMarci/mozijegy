import temp_data
import sqlite3
from customtkinter import *
from tkinter import messagebox
import subprocess
import sys
import hashlib

set_appearance_mode("dark")

PrimaryColor = "#1E1E2F"
SecondaryColor = "#2C2C3C"
TertiaryColor = "#3C3C4F"
QuaternaryColor = "#E0E0E0"
QuinaryColor = "#00FFF5"

root = CTk()
root.title("Szék kiválasztása")
root.geometry("600x450")
root.configure(fg_color=PrimaryColor)
root.resizable(False, False)

buttons = []
selected = []

data = temp_data.load_data()
movie = data["selected_movie"]

def stable_id(text):
    return int(hashlib.md5(text.encode()).hexdigest()[:8], 16) % 100000

film_id = stable_id(movie["title"] + movie["day"])
terem_szam = movie["terem_szam"]

conn = sqlite3.connect("mozi.db")
c = conn.cursor()

c.execute("SELECT film_id, sor, oszlop, terem_szam FROM terem")
all_rows = c.fetchall()
print("[DEBUG] DB CONTENTS:")
for row in all_rows:
    print(f"  FILM_ID={row[0]}, SOR={row[1]}, OSZLOP={row[2]}, TEREM={row[3]}")

c.execute("SELECT szerelonev, oradij FROM szerelo")
szerelok = c.fetchall()

c.execute("SELECT * FROM terem WHERE film_id=? AND terem_szam=?", (film_id, terem_szam))
foglalasok = c.fetchall()

def toggle_button(btn):
    if btn in selected:
        selected.remove(btn)
        btn.configure(fg_color=SecondaryColor)
    else:
        selected.append(btn)
        btn.configure(fg_color=QuinaryColor)

def foglalas_mentese():
    for btn in selected:
        hely = btn.cget("text")
        sor = hely[0]
        oszlop = int(hely[1:])
        c.execute("INSERT INTO foglalasok (film_id, sor, oszlop, terem_szam) VALUES (?, ?, ?, ?)",
                  (film_id, sor, oszlop, terem_szam))
    conn.commit()
    messagebox.showinfo("Siker", "Helyfoglalás mentve!")

    # Itt indítjuk a jegy generálót
    subprocess.Popen([sys.executable, "jegy_foglalo.py"])

    root.destroy()

def init_buttons():
    for i in range(1, 8):
        for j in range(1, 10):
            hely = f"{chr(64+i)}{j}"
            btn = CTkButton(root, text=hely, width=40, height=40, fg_color=SecondaryColor,
                            hover_color=QuinaryColor, corner_radius=5, command=lambda b=btn: toggle_button(b))
            btn.grid(row=i, column=j, padx=5, pady=5)
            buttons.append(btn)

    # Foglalt helyek jelzése pirossal (példa)
    for foglalt in foglalasok:
        sor_foglalt = foglalt[1]
        oszlop_foglalt = foglalt[2]
        hely_foglalt = f"{sor_foglalt}{oszlop_foglalt}"
        # Meg kell alakítani, hogy megfeleljen az aktuális betű+szám formátumnak, pl. 'A1'
        hely_foglalt = f"{sor_foglalt}{oszlop_foglalt}"
        for btn in buttons:
            if btn.cget("text") == hely_foglalt:
                btn.configure(fg_color="#ff4d4d", state="disabled")

init_buttons()

mentes_btn = CTkButton(root, text="Foglalás Mentése", fg_color=QuinaryColor, hover_color="#00D9C0",
                       text_color="black", font=("Orbitron", 16), command=foglalas_mentese)
mentes_btn.grid(row=8, column=0, columnspan=11, pady=10)

root.mainloop()
