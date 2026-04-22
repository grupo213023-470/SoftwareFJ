from tkinter import *
from clientes import abrir_clientes
from servicios import abrir_servicios
from reservas import abrir_reservas
from logs import abrir_logs

root = Tk()
root.title("Sistema Software FJ")
root.geometry("500x450")

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
    command=abrir_clientes
).pack(pady=10)

Button(
    root,
    text="Servicios",
    width=25,
    height=2,
    command=abrir_servicios
).pack(pady=10)

Button(
    root,
    text="Reservas",
    width=25,
    height=2,
    command=abrir_reservas
).pack(pady=10)

Button(
    root,
    text="Logs",
    width=25,
    height=2,
    command=abrir_logs
).pack(pady=10)


root.mainloop()