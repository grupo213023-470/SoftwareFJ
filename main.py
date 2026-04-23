from tkinter import *
from clientes import ventana_clientes
from servicios import ventana_servicios
from reservas import ventana_reservas
from logs import ventana_logs

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