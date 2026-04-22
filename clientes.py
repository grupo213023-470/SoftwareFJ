from tkinter import *

def abrir_clientes():

    ventana = Toplevel()
    ventana.title("Clientes")
    ventana.geometry("400x350")

    Label(
        ventana,
        text="REGISTRO CLIENTES",
        font=("Arial",16,"bold")
    ).pack(pady=15)

    Label(ventana,text="Nombre").pack()
    Entry(ventana,width=35).pack()

    Label(ventana,text="Correo").pack()
    Entry(ventana,width=35).pack()

    Label(ventana,text="Teléfono").pack()
    Entry(ventana,width=35).pack()

    Button(
        ventana,
        text="Guardar",
        width=20
    ).pack(pady=20)