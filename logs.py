from tkinter import *

def abrir_logs():

    ventana = Toplevel()
    ventana.title("Logs")
    ventana.geometry("500x400")

    Label(
        ventana,
        text="LOGS DEL SISTEMA",
        font=("Arial",16,"bold")
    ).pack(pady=15)

    Text(
        ventana,
        width=55,
        height=18
    ).pack()