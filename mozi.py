import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Window, Style

# Alapvető beállítások
root = Window(themename="cosmo")
root.geometry("800x600")
root.title("Mozi Jegy Foglalás")

# Filmek adatai
films = [
    {"cim": "Film1", "hossz": "148 perc", "szabad": 12},
    {"cim": "Film2", "hossz": "169 perc", "szabad": 8},
    {"cim": "Film3", "hossz": "152 perc", "szabad": 5},
    {"cim": "Film4", "hossz": "110 perc", "szabad": 30},
]

# Helyválasztás fül
def helyvalasztas_tab(tab):
    frame = ttk.Frame(tab)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Terem székeinek elrendezése
    seats_frame = ttk.Frame(frame)
    seats_frame.pack(pady=20)

    # Székek (például 5x5-ös elrendezés)
    for row in range(5):
        for col in range(5):
            seat = ttk.Button(seats_frame, text=f"{row*5+col+1}", width=5, bootstyle="secondary")
            seat.grid(row=row, column=col, padx=5, pady=5)
            seat.bind("<Button-1>", lambda e, seat=seat: select_seat(seat))

    # Kiválasztott székek listája
    selected_seats_label = ttk.Label(frame, text="Kiválasztott székek: ", font=("Arial", 10))
    selected_seats_label.pack(pady=10)

    selected_seats_list = tk.Listbox(frame, height=5)
    selected_seats_list.pack(pady=10)

    def select_seat(seat):
        seat_number = seat.cget("text")
        if seat.cget("bootstyle") == "secondary":
            seat.config(bootstyle="success")
            selected_seats_list.insert(tk.END, seat_number)
        else:
            seat.config(bootstyle="secondary")
            selected_seats_list.delete(selected_seats_list.get(0, tk.END).index(seat_number))

# Jegyválasztás fül
def jegyvalasztas_tab(tab):
    frame = ttk.Frame(tab)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Jegyek száma
    ticket_count_label = ttk.Label(frame, text="Jegyek száma: ", font=("Arial", 10))
    ticket_count_label.pack(pady=10)

    ticket_count_spinbox = ttk.Spinbox(frame, from_=1, to=10, width=5)
    ticket_count_spinbox.pack(pady=10)

# Fizetés fül
def fizetes_tab(tab):
    frame = ttk.Frame(tab)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Összeg
    total_label = ttk.Label(frame, text="Összeg: 0 Ft", font=("Arial", 12, "bold"))
    total_label.pack(pady=20)

    # Fizetési módok
    payment_method_label = ttk.Label(frame, text="Fizetési mód: ", font=("Arial", 10))
    payment_method_label.pack(pady=10)

    payment_methods = ["Készpénz", "Kártya", "Online"]
    payment_method_combobox = ttk.Combobox(frame, values=payment_methods, state="readonly")
    payment_method_combobox.set(payment_methods[0])
    payment_method_combobox.pack(pady=10)

    # Fizetés gomb
    pay_button = ttk.Button(frame, text="Fizetés", bootstyle="success")
    pay_button.pack(pady=20)

# Fő fül
def main_tab():
    tab_control = ttk.Notebook(root)
    tab_control.pack(fill="both", expand=True)

    helyvalasztas = ttk.Frame(tab_control)
    tab_control.add(helyvalasztas, text="Helyválasztás")
    helyvalasztas_tab(helyvalasztas)

    jegyvalasztas = ttk.Frame(tab_control)
    tab_control.add(jegyvalasztas, text="Jegyválasztás")
    jegyvalasztas_tab(jegyvalasztas)

    fizetes = ttk.Frame(tab_control)
    tab_control.add(fizetes, text="Fizetés")
    fizetes_tab(fizetes)

# Főablak indítása
main_tab()
root.mainloop()
