import temp_data
import sqlite3
from customtkinter import *
from tkinter import messagebox
import subprocess
import sys
import os
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

c.execute("SELECT sor, oszlop FROM terem WHERE film_id=? AND terem_szam=?", (film_id, terem_szam))
reserved_seats_raw = c.fetchall()
reserved_seats = {(int(sor), int(oszlop)) for sor, oszlop in reserved_seats_raw}
print("[DEBUG] RESERVED SEATS:", reserved_seats_raw)

conn.close()

# === Székek kezelése ===
def toggle(i, j):
    if (i, j) in selected:
        selected.remove((i, j))
        buttons[i][j].configure(fg_color=TertiaryColor, text_color="white")
    else:
        selected.append((i, j))
        buttons[i][j].configure(fg_color="#70FF99", text_color="black")

# === Székek rácsba rendezése ===
frame = CTkFrame(root, fg_color=SecondaryColor)
frame.pack(pady=20)

for i in range(5):
    row = []
    for j in range(8):
        seat_pos = (i, j)
        if seat_pos in reserved_seats:
            btn = CTkButton(frame, text=f"{i+1},{j+1}", width=60, height=40,
                            fg_color="red", text_color="white", state=DISABLED, corner_radius=8)
        else:
            btn = CTkButton(frame, text=f"{i+1},{j+1}", width=60, height=40,
                            fg_color=TertiaryColor, text_color="white", corner_radius=8,
                            command=lambda i=i, j=j: toggle(i, j))
        btn.grid(row=i, column=j, padx=5, pady=5)
        row.append(btn)
    buttons.append(row)

# === Mentés gomb ===
def mentes():
    if not selected:
        messagebox.showerror("Hiba", "Legalább egy széket ki kell választani!")
        return

    try:
        conn = sqlite3.connect("mozi.db")
        c = conn.cursor()

        for seat in selected:
            sor, oszlop = seat
            c.execute("SELECT * FROM terem WHERE film_id=? AND sor=? AND oszlop=?", (film_id, sor, oszlop))
            if c.fetchone():
                messagebox.showwarning("Foglalás", f"A(z) {sor+1}. sor {oszlop+1}. szék már foglalt!")
                continue

            c.execute("INSERT INTO terem (film_id, sor, oszlop, terem_szam) VALUES (?, ?, ?, ?)",
                      (film_id, sor, oszlop, terem_szam))

        conn.commit()
        conn.close()

        data["selected_movie"]["seats"] = selected
        temp_data.save_data(data)

        print("[INFO] Seats successfully saved and written to temp_data.json.")
        root.destroy()
        subprocess.Popen([sys.executable, "adat_beolvasas.py"])

    except Exception as e:
        print("[ERROR] Failed to save seats:", e)
        messagebox.showerror("Adatbázis hiba", f"Hiba a mentés során: {e}")

CTkButton(root, text="Foglalás mentése", command=mentes,
          fg_color=QuinaryColor, hover_color="#00D9C0", text_color="black",
          font=("Orbitron", 14), corner_radius=20, height=45, width=300).pack(pady=15)

root.mainloop()
