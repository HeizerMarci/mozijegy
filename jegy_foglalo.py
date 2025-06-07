import temp_data
from fpdf import FPDF
import os

def jegy_keszites():
    data = temp_data.load_data()
    movie = data.get("selected_movie", {})
    if not movie:
        print("Nincs foglalás adat!")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, "ZSOMA Cinema", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=18)
    pdf.cell(0, 15, f"Film: {movie.get('title', 'N/A')}", ln=True)
    pdf.cell(0, 15, f"Napon: {movie.get('day', 'N/A')}", ln=True)
    pdf.cell(0, 15, f"Időpont: {movie.get('time', 'N/A')}", ln=True)
    pdf.cell(0, 15, f"Terem: {movie.get('terem_szam', 'N/A')}", ln=True)

    # Ha van helyfoglalás rész, azokat is hozzá lehet adni
    foglalasok = data.get("foglalasok", [])
    if foglalasok:
        pdf.cell(0, 15, "Helyek:", ln=True)
        for hely in foglalasok:
            pdf.cell(0, 12, f"  {hely}", ln=True)

    save_path = os.path.join(os.getcwd(), "jegy.pdf")
    pdf.output(save_path)
    print(f"Jegy elkészült és elmentve ide: {save_path}")

if __name__ == "__main__":
    jegy_keszites()
