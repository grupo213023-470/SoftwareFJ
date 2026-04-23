from tkinter import *

def ventana_servicios():

    ventana = Toplevel()
    ventana.title("Servicios")
    ventana.geometry("400x350")

    Label(
        ventana,
        text="REGISTRO SERVICIOS",
        font=("Arial",16,"bold")
    ).pack(pady=15)

    Label(ventana,text="Nombre Servicio").pack()
    Entry(ventana,width=35).pack()

    Label(ventana,text="Tipo").pack()
    Entry(ventana,width=35).pack()

    Label(ventana,text="Precio").pack()
    Entry(ventana,width=35).pack()

    Button(
        ventana,
        text="Guardar",
        width=20
    ).pack(pady=20)