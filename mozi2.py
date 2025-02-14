import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Window
import random


# Alapvető beállítások
root = Window(themename="cosmo")
root.geometry("800x400")
root.title("Mozi Jegy Foglalás")

# Filmek adatai
films = [
    {"cim": "Film1", "hossz": "148 perc", "szabad": 12},
    {"cim": "Film2", "hossz": "169 perc", "szabad": 8},
    {"cim": "Film3", "hossz": "152 perc", "szabad": 5},
    {"cim": "Film4", "hossz": "110 perc", "szabad": 30},
]

# Kiválasztott jegyek lista
selected_seats = []


# Filmek listájának megjelenítése
def show_films():
    for film in films:
        frame = ttk.Frame(root, padding=10, bootstyle="primary")
        frame.pack(pady=5, padx=10, fill="x")

        # Film címe (bal oldalt)
        title = ttk.Label(frame, text=film["cim"], font=("Arial", 12, "bold"), width=15, anchor="w")
        title.pack(side="left", padx=10)

        # Játékidő (középen)
        duration = ttk.Label(frame, text=film["hossz"], font=("Arial", 10), width=10, anchor="center")
        duration.pack(side="left", expand=True)

        # Szabad helyek száma (jobb oldalt)
        available = ttk.Label(frame, text=f"🪑: {film['szabad']}", font=("Arial", 10), width=10, anchor="center")
        available.pack(side="left", padx=10)

        # Foglalás gomb (jobb oldalt)
        button = ttk.Button(frame, text="Foglalás", bootstyle="success", command=lambda f=film: open_booking_window(f))
        button.pack(side="right", padx=10)


# Új ablak megnyitása a foglalás gomb megnyomásakor
def open_booking_window(film):
    # Új ablak létrehozása
    booking_window = tk.Toplevel()  # Itt tk.Toplevel() a helyes
    booking_window.title(f"Foglalás: {film['cim']}")
    booking_window.geometry("600x400")

    # Notebook (fülek) létrehozása
    notebook = ttk.Notebook(booking_window, bootstyle="primary")
    notebook.pack(fill="both", expand=True)

    # "Hely választás" fül
    seat_selection_frame = ttk.Frame(notebook)
    notebook.add(seat_selection_frame, text="Hely választás")

    # Terem székeinek megjelenítése (példa: 5 sor, 8 oszlop)
    rows, cols = 5, 8
    total_seats = rows * cols
    occupied_seats_count = total_seats - film['szabad']
    occupied_seats = random.sample(range(total_seats), occupied_seats_count)

    global selected_list  # Globálisan elérjük a selected_list változót

    selected_label = ttk.Label(seat_selection_frame, text="Kiválasztott jegyek:", font=("Arial", 12, "bold"))
    selected_label.grid(row=0, column=0, columnspan=8, pady=10)

    selected_list = ttk.Label(seat_selection_frame, text="\n".join(selected_seats), font=("Arial", 10))
    selected_list.grid(row=1, column=0, columnspan=8, pady=5)

    # Helyek gombjainak létrehozása
    for r in range(rows):
        for c in range(cols):
            seat_index = r * cols + c
            seat_text = f"{r + 1}-{c + 1}"

            if seat_index in occupied_seats:
                seat = ttk.Button(
                    seat_selection_frame,
                    text=seat_text,
                    bootstyle="danger",
                    state="disabled"  # Letiltva, mivel foglalt
                )
            else:
                seat = ttk.Button(
                    seat_selection_frame,
                    text=seat_text,
                    bootstyle="success",
                    state="normal",  # Aktiválva, mivel szabad
                )
                seat.config(command=lambda seat_text=seat_text, seat_button=seat: toggle_seat(seat_text, seat_button))

            seat.grid(row=r + 2, column=c, padx=5, pady=5)

    # Jegy választás fül
    ticket_selection_frame = ttk.Frame(notebook)
    notebook.add(ticket_selection_frame, text="Jegy választás")

    # Fizetés fül
    payment_frame = ttk.Frame(notebook)
    notebook.add(payment_frame, text="Fizetés")

    # Tovább gomb, ami csak akkor engedélyezett, ha van választott jegy
    continue_button = ttk.Button(seat_selection_frame, text="Tovább", bootstyle="primary", state="disabled",
                                 command=lambda: select_ticket_tab(notebook, ticket_selection_frame, film))
    continue_button.grid(row=rows + 2, column=0, columnspan=cols, pady=10)

    # Kiválasztott jegyek frissítése
    def update_selected_list():
        selected_list.config(text=" ,".join(selected_seats))

    # Jegy (szék) kiválasztása és eltávolítása a listából
    def toggle_seat(seat_text, seat_button):
        if seat_text in selected_seats:
            # Ha a szék már a listában van, töröljük
            selected_seats.remove(seat_text)
            seat_button.configure(bootstyle="success")  # Zöldre állítjuk a gombot
        else:
            # Ha a szék nincs a listában, hozzáadjuk
            selected_seats.append(seat_text)
            seat_button.configure(bootstyle="warning")  # Sárgára állítjuk a gombot

        # A kiválasztott jegyek lista frissítése
        update_selected_list()

        # A "Tovább" gomb engedélyezése
        if selected_seats:
            continue_button.configure(state="normal")
        else:
            continue_button.configure(state="disabled")

    # Tovább gomb aktiválása
    def select_ticket_tab(notebook, ticket_selection_frame, film):
        # Átváltunk a jegy választás fülre, ha van kiválasztott jegy
        if selected_seats:
            notebook.select(1)  # Index 1 a "Jegy választás" fül

            # Jegy típusok megjelenítése, ha van választott szék
            display_ticket_types(ticket_selection_frame, len(selected_seats))

    def display_ticket_types(ticket_selection_frame, seat_count):
        # Jegy típusok (diák, nyugdíjas, felnőtt)
        ticket_types = ["Diák", "Nyugdíjas", "Felnőtt"]

        # Jegy típusok kiírása
        for i, ticket_type in enumerate(ticket_types):
            if i < seat_count:
                # Képzeljünk el egy `Frame`-et, amit a gombokkal együtt használunk
                frame = ttk.Frame(ticket_selection_frame)
                frame.grid(row=i, column=0, padx=10, pady=5)

                # Jegy típus címke
                ttk.Label(frame, text=f"{ticket_type} jegy", font=("Arial", 12)).grid(row=0, column=0, padx=10)

                # Jegy száma
                count_label = ttk.Label(frame, text="0", font=("Arial", 10), width=5)
                count_label.grid(row=0, column=1, padx=10)

                # + és - gombok
                def increase(ticket_type=ticket_type):
                    if ticket_count["total"] < seat_count:  # Csak annyi jegy választható, amennyi hely van
                        ticket_count[ticket_type] += 1
                        ticket_count["total"] += 1
                        count_label.config(text=str(ticket_count[ticket_type]))

                def decrease(ticket_type=ticket_type):
                    if ticket_count[ticket_type] > 0:
                        ticket_count[ticket_type] -= 1
                        ticket_count["total"] -= 1
                        count_label.config(text=str(ticket_count[ticket_type]))

                # + és - gombok
                ttk.Button(frame, text="+", command=increase).grid(row=0, column=2, padx=10)
                ttk.Button(frame, text="-", command=decrease).grid(row=0, column=3, padx=10)

    # Jegyek számának nyilvántartása
    ticket_count = {"Diák": 0, "Nyugdíjas": 0, "Felnőtt": 0, "total": 0}


# Filmek megjelenítése
show_films()

root.mainloop()
