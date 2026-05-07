from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
from logs import Logger


# ==========================================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================================
class ErrorReserva(Exception):
    pass


class ErrorDuracion(ErrorReserva):
    pass


# ==========================================================
# CLASE RESERVA
# ==========================================================
class Reserva:

    contador = 1

    def __init__(self, cliente, servicio, horas):
        self.__id = Reserva.contador
        Reserva.contador += 1

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"
        self.fecha = datetime.now()

    @property
    def id(self):
        return self.__id

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, valor):
        if not valor.strip():
            raise ErrorReserva("El cliente es obligatorio.")
        self.__cliente = valor.strip().title()

    @property
    def servicio(self):
        return self.__servicio

    @servicio.setter
    def servicio(self, valor):
        if not valor.strip():
            raise ErrorReserva("El servicio es obligatorio.")
        self.__servicio = valor.strip().title()

    @property
    def horas(self):
        return self.__horas

    @horas.setter
    def horas(self, valor):
        try:
            valor = int(valor)

            if valor <= 0:
                raise ErrorDuracion("Las horas deben ser mayores que cero.")

            self.__horas = valor

        except ValueError as error:
            raise ErrorDuracion("Las horas deben ser un número entero.") from error

    def confirmar(self):
        if self.estado == "Cancelada":
            raise ErrorReserva("No se puede confirmar una reserva cancelada.")
        self.estado = "Confirmada"

    def cancelar(self):
        if self.estado in ["Confirmada", "Procesada"]:
            raise ErrorReserva(
                "No se puede cancelar una reserva confirmada o procesada."
            )

        self.estado = "Cancelada"

    def procesar(self):
        if self.estado == "Cancelada":
            raise ErrorReserva("No se puede procesar una reserva cancelada.")

        self.estado = "Procesada"


# ==========================================================
# GESTOR DE RESERVAS
# ==========================================================
class GestorReservas:

    __lista = []

    @classmethod
    def agregar(cls, reserva):
        cls.__lista.append(reserva)

    @classmethod
    def obtener_todos(cls):
        return cls.__lista

    @classmethod
    def obtener(cls, indice):
        return cls.__lista[indice]

    @classmethod
    def eliminar(cls, indice):
        del cls.__lista[indice]


# ==========================================================
# VENTANA RESERVAS
# ==========================================================
def ventana_reservas():

    def limpiar():
        txt_cliente.delete(0, END)
        txt_servicio.delete(0, END)
        txt_horas.delete(0, END)

    def cargar_tabla():
        tabla.delete(*tabla.get_children())

        for i, reserva in enumerate(GestorReservas.obtener_todos()):
            tabla.insert(
                "",
                END,
                iid=i,
                values=(
                    reserva.id,
                    reserva.cliente,
                    reserva.servicio,
                    reserva.horas,
                    reserva.estado,
                    "Confirmar",
                    "Cancelar",
                    "Procesar",
                    "Eliminar"
                )
            )

    def guardar():

        try:
            nueva = Reserva(
                txt_cliente.get(),
                txt_servicio.get(),
                txt_horas.get()
            )

            GestorReservas.agregar(nueva)

            Logger.registrar_evento(
                "Reserva creada correctamente",
                "Reservas"
            )

        except Exception as error:
            Logger.registrar_error(
                error,
                "Reservas",
                "Error al crear reserva"
            )

            messagebox.showerror("Error", str(error))

        else:
            messagebox.showinfo(
                "Éxito",
                "Reserva registrada correctamente."
            )

            cargar_tabla()
            limpiar()

        finally:
            print("Proceso de reserva finalizado.")

    def click_tabla(evento):

        fila = tabla.identify_row(evento.y)
        columna = tabla.identify_column(evento.x)

        if not fila:
            return

        indice = int(fila)
        reserva = GestorReservas.obtener(indice)

        try:
            if columna == "#6":
                reserva.confirmar()

                Logger.registrar_evento(
                    "Reserva confirmada",
                    "Reservas"
                )

            elif columna == "#7":
                reserva.cancelar()

                Logger.registrar_evento(
                    "Reserva cancelada",
                    "Reservas"
                )

            elif columna == "#8":
                reserva.procesar()

                Logger.registrar_evento(
                    "Reserva procesada",
                    "Reservas"
                )

            elif columna == "#9":
                GestorReservas.eliminar(indice)

                Logger.registrar_evento(
                    "Reserva eliminada",
                    "Reservas"
                )

            cargar_tabla()

        except Exception as error:
            Logger.registrar_error(
                error,
                "Reservas",
                "Error al actualizar reserva"
            )

            messagebox.showerror("Error", str(error))

    ventana = Toplevel()
    ventana.title("Reservas")
    ventana.geometry("1050x580")
    ventana.configure(bg="#f4f6f8")

    Label(
        ventana,
        text="GESTIÓN DE RESERVAS",
        font=("Arial", 18, "bold"),
        bg="#f4f6f8"
    ).pack(pady=15)

    marco = LabelFrame(
        ventana,
        text=" Información de la Reserva ",
        padx=15,
        pady=15,
        bg="white"
    )

    marco.pack(
        padx=15,
        pady=10,
        fill="x"
    )

    Label(marco, text="Cliente", bg="white").grid(row=0, column=0, sticky="w")
    txt_cliente = Entry(marco, width=35)
    txt_cliente.grid(row=0, column=1, padx=8, pady=5)

    Label(marco, text="Servicio", bg="white").grid(row=1, column=0, sticky="w")
    txt_servicio = Entry(marco, width=35)
    txt_servicio.grid(row=1, column=1, padx=8, pady=5)

    Label(marco, text="Horas", bg="white").grid(row=2, column=0, sticky="w")
    txt_horas = Entry(marco, width=35)
    txt_horas.grid(row=2, column=1, padx=8, pady=5)

    Button(
        ventana,
        text="Guardar Reserva",
        width=25,
        bg="#1976d2",
        fg="white",
        command=guardar
    ).pack(pady=10)

    columnas = (
        "ID",
        "Cliente",
        "Servicio",
        "Horas",
        "Estado",
        "Confirmar",
        "Cancelar",
        "Procesar",
        "Eliminar"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings",
        height=14
    )

    for columna in columnas:
        tabla.heading(columna, text=columna)

    tabla.column("ID", width=50)
    tabla.column("Cliente", width=180)
    tabla.column("Servicio", width=180)
    tabla.column("Horas", width=80)
    tabla.column("Estado", width=120)
    tabla.column("Confirmar", width=100)
    tabla.column("Cancelar", width=100)
    tabla.column("Procesar", width=100)
    tabla.column("Eliminar", width=100)

    tabla.pack(
        padx=15,
        pady=10,
        fill="both",
        expand=True
    )

    tabla.bind("<Button-1>", click_tabla)

    cargar_tabla()