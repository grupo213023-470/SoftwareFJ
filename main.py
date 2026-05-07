from tkinter import *
from clientes import ventana_clientes
from servicios import ventana_servicios
from reservas import ventana_reservas
from logs import ventana_logs
from tkinter import messagebox


# FUNCION ABOUT
def mostrar_about():
    messagebox.showinfo(
        "About",
        "Sistema Software FJ\n\n"        
        "Integrantes del Grupo: 213023_470\n"
        "       \n"
        "- ARMANDO GUILLERMO TROUT GARCIA\n"        
        "- JESUS DANIEL GUZMAN CARMONA\n"
        "       \n"
        "Versión 1.0  -  UNAD 2026       \n"       
    )   
    
    
# VENTANA PRINCIPAL  

root = Tk()
root.title("Sistema Software FJ")
root.geometry("500x450")


# ===== MENU SUPERIOR =====
barra_menu = Menu(root)

menu_about = Menu(barra_menu, tearoff=0)

menu_about.add_command(
    label="Integrantes",
    command=mostrar_about
)

barra_menu.add_cascade(
    label="About",
    menu=menu_about
)

root.config(menu=barra_menu)

# =========================

Label(
    root,
    text="MENÚ PRINCIPAL",
    font=("Arial",18,"bold")
).pack(pady=20)

Button(
    root,
    text="Clientes",
    width=25,
    height=2,
    command=ventana_clientes 
).pack(pady=10)

Button(
    root,
    text="Servicios",
    width=25,
    height=2,
    command=ventana_servicios
).pack(pady=10)

Button(
    root,
    text="Reservas",
    width=25,
    height=2,
    command=ventana_reservas
).pack(pady=10)

Button(
    root,
    text="Logs",
    width=25,
    height=2,
    command=ventana_logs
).pack(pady=10)


root.mainloop()