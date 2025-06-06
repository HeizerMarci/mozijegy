import temp_data
from customtkinter import *
from tkinter import messagebox
import subprocess
import sys

set_appearance_mode("dark")

PrimaryColor = "#1E1E2F"
SecondaryColor = "#2C2C3C"
TertiaryColor = "#3C3C4F"
QuaternaryColor = "#E0E0E0"
QuinaryColor = "#00FFF5"

postcode_to_city = {
    "8174": "Balatonkenese",
    "1051": "Budapest V.",
    "4024": "Debrecen",
    "7621": "Pécs",
    "8000": "Székesfehérvár",
    "6000": "Kecskemét",
    "3300": "Eger",
    "9400": "Sopron",
    "6720": "Szeged",
    "9021": "Győr"
}

def update_address_field(*args):
    postcode = postcode_entry.get().strip()
    city = postcode_to_city.get(postcode)
    if city:
        address_entry.delete(0, 'end')
        address_entry.insert(0, city)

root = CTk()
root.title("Foglaló adatai")
root.geometry("400x370")
root.configure(fg_color=PrimaryColor)
root.resizable(False, False)

CTkLabel(root, text="Név", text_color=QuinaryColor, font=("Segoe UI", 14)).grid(row=0, column=0, padx=10, pady=10, sticky="e")
CTkLabel(root, text="Irányízószám", text_color=QuinaryColor, font=("Segoe UI", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
CTkLabel(root, text="Város", text_color=QuinaryColor, font=("Segoe UI", 14)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
CTkLabel(root, text="Ház szám", text_color=QuinaryColor, font=("Segoe UI", 14)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
CTkLabel(root, text="Email", text_color=QuinaryColor, font=("Segoe UI", 14)).grid(row=4, column=0, padx=10, pady=10, sticky="e")
CTkLabel(root, text="Telefon +36", text_color=QuinaryColor, font=("Segoe UI", 14)).grid(row=5, column=0, padx=10, pady=10, sticky="e")

name_entry = CTkEntry(root, width=220, corner_radius=8, fg_color=TertiaryColor, text_color="white")
postcode_entry = CTkEntry(root, width=220, corner_radius=8, fg_color=TertiaryColor, text_color="white")
address_entry = CTkEntry(root, width=220, corner_radius=8, fg_color=TertiaryColor, text_color="white")
street_entry = CTkEntry(root, width=220, corner_radius=8, fg_color=TertiaryColor, text_color="white")
email_entry = CTkEntry(root, width=220, corner_radius=8, fg_color=TertiaryColor, text_color="white")
phone_entry = CTkEntry(root, width=220, corner_radius=8, fg_color=TertiaryColor, text_color="white")

name_entry.grid(row=0, column=1, padx=10, pady=10)
postcode_entry.grid(row=1, column=1, padx=10, pady=10)
address_entry.grid(row=2, column=1, padx=10, pady=10)
street_entry.grid(row=3, column=1, padx=10, pady=10)
email_entry.grid(row=4, column=1, padx=10, pady=10)
phone_entry.grid(row=5, column=1, padx=10, pady=10)

postcode_entry.bind("<KeyRelease>", update_address_field)

def submit():
    name = name_entry.get().strip()
    postcode = postcode_entry.get().strip()
    address = address_entry.get().strip()
    street = street_entry.get().strip()
    email = email_entry.get().strip()
    phone = f'+36{phone_entry.get().strip()}'

    if not name or not postcode or not address or not email or not phone:
        messagebox.showerror("Hiba", "Minden mező kitöltése kötelező!")
        return

    if "@" not in email or not email.endswith(".com"):
        messagebox.showerror("Hiba", "Érvénytelen Email cím!")
        return

    if not phone[3:].isdigit() or len(phone) != 12:
        messagebox.showerror("Hiba", "Érvénytelen Telefonszám!")
        return

    data = temp_data.load_data()
    data["customer_data"] = {
        "name": name,
        "postcode": postcode,
        "address": address,
        "street": street,
        "email": email,
        "phone": phone
    }
    temp_data.save_data(data)

    root.destroy()
    subprocess.Popen([sys.executable, "jegy_keszito.py"])

CTkButton(root, text="Tovább", command=submit, width=200, height=40,
          fg_color=QuinaryColor, hover_color="#00D9C0", text_color="black",
          font=("Orbitron", 14), corner_radius=20).grid(row=6, column=1, columnspan=2, pady=25)

root.mainloop()
