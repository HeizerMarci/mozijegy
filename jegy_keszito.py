from fpdf import FPDF
from datetime import datetime
import os
import platform
import temp_data
import random

def simple_ascii_fix(text):
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ö": "o", "ő": "o",
        "ú": "u", "ü": "u", "ű": "u", "Á": "A", "É": "E", "Í": "I",
        "Ó": "O", "Ö": "O", "Ő": "O", "Ú": "U", "Ü": "U", "Ű": "U"
    }
    for h, a in replacements.items():
        text = text.replace(h, a)
    return text



def jegy():
    data = temp_data.load_data()
    movie = data["selected_movie"]
    customer = data["customer_data"]
            
    print(len(movie["seats"]))
    for i in range(0,len(movie["seats"])):    
        try:
            seats = movie["seats"]
            seat_text = ", ".join([f"{sor + 1}. sor {oszlop + 1}. szek" for sor, oszlop in seats])
            seat = seats[i]
            print(seats)

            mozijegy = FPDF('P', 'mm', 'A4')
            mozijegy.add_page()
            mozijegy.set_draw_color(225, 165, 0)
            mozijegy.set_line_width(5)

            # Border lines
            mozijegy.line(0, 1, 210, 2)
            mozijegy.line(0, 1, 0, 400)
            mozijegy.line(210, 1, 210, 400)
            mozijegy.line(0, 295, 210, 295)
            mozijegy.line(17, 40, 193, 40)
            mozijegy.line(17, 100, 193, 100)
            mozijegy.line(17, 175, 193, 175)
            mozijegy.line(17, 200, 193, 200)

            # Images
            mozijegy.image('images/qr-code.png', x=135, y=105, h=60, w=60, type="PNG")
            mozijegy.image('images/popcorn.png', x=140, y=12.5, h=30, w=30, type="PNG")
            mozijegy.image('images/soda.png', x=155.5, y=7.5, h=40, w=40, type="PNG")
            mozijegy.image('images/logo.png', x=150, y=227, h=40, w=40, type="PNG")

            # TEREM / SOR / SZÉK
            mozijegy.set_text_color(225, 165, 0)
            mozijegy.set_font("Arial", "B", 32.5)
            mozijegy.text(17, 117.5, "TEREM")
            mozijegy.text(17, 137.5, "SOR")
            mozijegy.text(17, 157.5, "SZEK")

            mozijegy.set_text_color(0, 0, 0)
            mozijegy.text(75, 117.5, simple_ascii_fix(f"{movie['terem_szam']}. terem"))
            mozijegy.text(75, 137.5, str(seat[0] + 1))
            mozijegy.text(75, 157.5, str(seat[1] + 1))

            # Cím és fejléc
            mozijegy.set_text_color(225, 165, 0)
            mozijegy.set_font("Arial", "B", 23.5)
            mozijegy.text(15, 20, "VASARLAS")
            mozijegy.text(15, 30, "AZONOSITO")

            mozijegy.set_text_color(0, 0, 0)
            mozijegy.set_font("Arial", "", 23.5)
            mozijegy.text(90.25, 30, f"{random.randint(100000000, 999999999)}")

            mozijegy.set_text_color(225, 165, 0)
            mozijegy.set_font("Arial", "B", 23.5)
            mozijegy.text(15, 52.5, "ELOADAS")

            mozijegy.set_text_color(0, 0, 0)
            mozijegy.set_font("Arial", "", 23.5)
            mozijegy.text(75, 52.5, simple_ascii_fix(f"{movie['title']}"))
            mozijegy.text(15, 67.5, simple_ascii_fix(f"{movie['day']} {movie['time']}"))
            mozijegy.text(15, 82.5, "Zsoma Cinema")

            # Ár és jegytípus
            mozijegy.set_font("Arial", "", 17.5)
            mozijegy.text(15, 185, "Diakjegy")
            mozijegy.text(75, 185, "1131334647402001")
            mozijegy.text(150, 185, "2 100.00 Ft")

            # Cégadatok
            mozijegy.set_font("Arial", "B", 12.5)
            mozijegy.text(15, 240, "CEGNEV:")
            mozijegy.text(15, 250, "Szekhely:")
            mozijegy.text(15, 260, "ADOSZAM:")

            mozijegy.set_text_color(225, 165, 0)
            mozijegy.text(45, 240, "zsoma Cinema Kft.")
            mozijegy.text(45, 250, "8200. Veszprem Iskola utca 4.")
            mozijegy.text(45, 260, "8511670549")

            mozijegy.set_font("Arial", "B", 15)
            mozijegy.text(10.5, 272.5, "KOSZONJUK, HOGY A ZSOMA CINEMA-BAN MOZIZOL! :)")
            mozijegy.text(27.5, 280, "JO SZORAKOZAST, KELLEMES MOZIELMENYT KIVANUNK!")

            # Save and open PDF
            mozijegy.output('mozijegy.pdf')

            if platform.system() == "Windows":
                os.startfile('mozijegy.pdf')
            elif platform.system() == "Darwin":
                os.system("open mozijegy.pdf")
            else:
                os.system("xdg-open mozijegy.pdf")

        except Exception as e:
            print("Hiba a jegy generalasakor:", e)

jegy()
