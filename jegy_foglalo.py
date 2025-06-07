# jegy_foglalo.py
import customtkinter as ctk
import temp_data
import jegy_keszito
from tkinter import messagebox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class JegyfoglaloApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Jegyfoglaló rendszer")
        self.geometry("600x400")
        
        self.data = temp_data.load_data()
        
        # Foglalások listája
        self.listbox = ctk.CTkListbox(self, width=400, height=200)
        self.listbox.pack(pady=20)
        
        self.load_foglalasok()
        
        # Gombok
        self.btn_jegy = ctk.CTkButton(self, text="Jegy generálás", command=self.jegy_generalas)
        self.btn_jegy.pack(pady=10)
        
        self.btn_torles = ctk.CTkButton(self, text="Foglalás törlése", command=self.foglalas_torles)
        self.btn_torles.pack(pady=10)
        
    def load_foglalasok(self):
        self.listbox.delete(0, 'end')
        data = self.data
        if not data or "selected_movie" not in data:
            self.listbox.insert('end', "Nincs foglalás.")
            return
        
        movie = data["selected_movie"]
        seats = movie.get("seats", [])
        for i, seat in enumerate(seats):
            self.listbox.insert('end', f"{i+1}. sor {seat[0]+1}, szék {seat[1]+1}")
    
    def jegy_generalas(self):
        if not self.data:
            messagebox.showinfo("Info", "Nincs foglalás, amihez jegyet készíthetne.")
            return
        jegy_keszito.jegy()
    
    def foglalas_torles(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Figyelem", "Válassz ki egy foglalást a törléshez!")
            return
        
        seat_index = selected_index[0]
        
        movie = self.data.get("selected_movie", {})
        seats = movie.get("seats", [])
        
        if 0 <= seat_index < len(seats):
            del seats[seat_index]
            temp_data.save_data(self.data)
            self.load_foglalasok()
            messagebox.showinfo("Siker", "Foglalás törölve.")
        else:
            messagebox.showerror("Hiba", "Érvénytelen foglalás kiválasztva.")
        

if __name__ == "__main__":
    app = JegyfoglaloApp()
    app.mainloop()
