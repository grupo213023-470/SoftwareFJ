from tkinter import *

def abrir_reservas():

    ventana = Toplevel()
    ventana.title("Reservas")
    ventana.geometry("400x400")

    Label(
        ventana,
        text="GESTIÓN RESERVAS",
        font=("Arial",16,"bold")
    ).pack(pady=15)

    Label(ventana,text="Cliente").pack()
    Entry(ventana,width=35).pack()

    Label(ventana,text="Servicio").pack()
    Entry(ventana,width=35).pack()

    Label(ventana,text="Horas").pack()
    Entry(ventana,width=35).pack()

    Label(ventana,text="Estado").pack()
    Entry(ventana,width=35).pack()

    Button(
        ventana,
        text="Guardar",
        width=20
    ).pack(pady=20)