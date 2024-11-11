from tkinter import Tk, Text, Button, END, messagebox
from fpdf import FPDF
import time

class PDFGenerator:
    def __init__(self,master):
        self.master = master
        self.master.title('PDF GENERATOR')
        self.text_area = Text(master, font=('Arial',12), height=10,width=50)
        self.text_area.pack(pady=20)
        Button(master, text='Generate PDF', command= self.generate_pdf, font=('Arial,16')).pack()

    def generate_pdf(self):
        text = self.text_area.get("1.0", END).strip()  
        if text:  
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            timestamp = time.strftime("%Y%m%d_%H%M%S")  # Definir correctamente la variable timestamp
            filename = f"pruebaPDF_{timestamp}.pdf"  # Usar el timestamp aquí
        
            pdf.multi_cell(0, 10, text)
            pdf.output(filename)
            self.text_area.delete("1.0", END)
            messagebox.showinfo("OK", "PDF generado exitosamente.")
        else:
            messagebox.showwarning("Error", "El área de texto está vacía. Ingrese texto para generar el PDF.")

            
root = Tk()
app = PDFGenerator(root)
root.mainloop()