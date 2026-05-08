from tkinter import *
from tkinter import ttk, messagebox
from abc import ABC, abstractmethod
from logs import Logger


# ==========================================================
# EXCEPCIONES PERSONALIZADAS
# ==========================================================
class ErrorServicio(Exception):
    pass


class ErrorPrecio(ErrorServicio):
    pass


class ErrorDisponibilidad(ErrorServicio):
    pass


class ErrorTipoServicio(ErrorServicio):
    pass


# ==========================================================
# CLASE ABSTRACTA SERVICIO
# ==========================================================
class Servicio(ABC):

    contador = 1

    def __init__(self, nombre, precio_base, disponible=True):
        self.__id = Servicio.contador
        Servicio.contador += 1

        self.nombre = nombre
        self.precio_base = precio_base
        self.disponible = disponible

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor.strip():
            raise ErrorServicio("El nombre del servicio es obligatorio.")
        self.__nombre = valor.strip().title()

    @property
    def precio_base(self):
        return self.__precio_base

    @precio_base.setter
    def precio_base(self, valor):
        try:
            valor = float(valor)

            if valor <= 0:
                raise ErrorPrecio("El precio debe ser mayor que cero.")

            self.__precio_base = valor

        except ValueError as error:
            raise ErrorPrecio("El precio debe ser un número válido.") from error

    @property
    def disponible(self):
        return self.__disponible

    @disponible.setter
    def disponible(self, valor):
        self.__disponible = bool(valor)

    @abstractmethod
    def calcular_costo(self, duracion=1, descuento=0, impuesto=0):
        pass

    @abstractmethod
    def descripcion(self):
        pass

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ErrorDisponibilidad("El servicio no está disponible.")

    def validar_parametros_costo(self, duracion, descuento, impuesto):
        """
        Valida los parámetros usados para calcular el costo del servicio.
        """
        if duracion <= 0:
            raise ErrorServicio("La duración debe ser mayor que cero.")

        if descuento < 0:
            raise ErrorServicio("El descuento no puede ser negativo.")

        if impuesto < 0:
            raise ErrorServicio("El impuesto no puede ser negativo.")


# ==========================================================
# SERVICIO 1: RESERVA DE SALA
# ==========================================================
class ReservaSala(Servicio):

    def __init__(self, nombre, precio_base, capacidad, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.capacidad = capacidad

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor):
        try:
            valor = int(valor)

            if valor <= 0:
                raise ErrorServicio("La capacidad debe ser mayor que cero.")

            self.__capacidad = valor

        except ValueError as error:
            raise ErrorServicio("La capacidad debe ser un número entero.") from error

    def calcular_costo(self, duracion=1, descuento=0, impuesto=0):
        self.validar_disponibilidad()
        self.validar_parametros_costo(duracion, descuento, impuesto)

        costo = self.precio_base * duracion
        costo -= costo * (descuento / 100)
        costo += costo * (impuesto / 100)

        return costo

    def descripcion(self):
        return f"Sala: {self.nombre} | Capacidad: {self.capacidad} personas"


# ==========================================================
# SERVICIO 2: ALQUILER DE EQUIPO
# ==========================================================
class AlquilerEquipo(Servicio):

    def __init__(self, nombre, precio_base, tipo_equipo, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.tipo_equipo = tipo_equipo

    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    @tipo_equipo.setter
    def tipo_equipo(self, valor):
        if not valor.strip():
            raise ErrorServicio("El tipo de equipo es obligatorio.")
        self.__tipo_equipo = valor.strip().title()

    def calcular_costo(self, duracion=1, descuento=0, impuesto=0):
        self.validar_disponibilidad()
        self.validar_parametros_costo(duracion, descuento, impuesto)

        costo = self.precio_base * duracion
        costo -= costo * (descuento / 100)
        costo += costo * (impuesto / 100)

        return costo

    def descripcion(self):
        return f"Equipo: {self.nombre} | Tipo: {self.tipo_equipo}"


# ==========================================================
# SERVICIO 3: ASESORÍA ESPECIALIZADA
# ==========================================================
class AsesoriaEspecializada(Servicio):

    def __init__(self, nombre, precio_base, especialidad, disponible=True):
        super().__init__(nombre, precio_base, disponible)
        self.especialidad = especialidad

    @property
    def especialidad(self):
        return self.__especialidad

    @especialidad.setter
    def especialidad(self, valor):
        if not valor.strip():
            raise ErrorServicio("La especialidad es obligatoria.")
        self.__especialidad = valor.strip().title()

    def calcular_costo(self, duracion=1, descuento=0, impuesto=0):
        self.validar_disponibilidad()
        self.validar_parametros_costo(duracion, descuento, impuesto)

        costo = self.precio_base * duracion
        costo -= costo * (descuento / 100)
        costo += costo * (impuesto / 100)

        return costo

    def descripcion(self):
        return f"Asesoría: {self.nombre} | Especialidad: {self.especialidad}"


# ==========================================================
# GESTOR DE SERVICIOS
# ==========================================================
class GestorServicios:

    __lista = []

    @classmethod
    def agregar(cls, servicio):
        cls.__lista.append(servicio)

    @classmethod
    def obtener_todos(cls):
        return cls.__lista

    @classmethod
    def obtener(cls, indice):
        return cls.__lista[indice]

    @classmethod
    def eliminar(cls, indice):
        del cls.__lista[indice]

    @classmethod
    def buscar(cls, texto):
        texto = texto.lower()
        resultados = []

        for servicio in cls.__lista:
            if texto in servicio.nombre.lower():
                resultados.append(servicio)

        return resultados


# ==========================================================
# VENTANA SERVICIOS
# ==========================================================
def ventana_servicios():

    def limpiar():
        txt_nombre.delete(0, END)
        txt_precio.delete(0, END)
        txt_extra.delete(0, END)
        combo_tipo.set("")
        combo_disponible.set("Sí")

    def cargar_tabla(lista=None):
        tabla.delete(*tabla.get_children())

        if lista is None:
            lista = GestorServicios.obtener_todos()

        for i, servicio in enumerate(lista):
            disponibilidad = "Sí" if servicio.disponible else "No"

            tabla.insert(
                "",
                END,
                iid=i,
                values=(
                    servicio.id,
                    servicio.nombre,
                    servicio.__class__.__name__,
                    servicio.precio_base,
                    disponibilidad,
                    "Ver",
                    "Eliminar"
                )
            )

    def guardar():

        try:
            tipo = combo_tipo.get()
            disponible = combo_disponible.get() == "Sí"

            if tipo == "Reserva de sala":
                servicio = ReservaSala(
                    txt_nombre.get(),
                    txt_precio.get(),
                    txt_extra.get(),
                    disponible
                )

            elif tipo == "Alquiler de equipo":
                servicio = AlquilerEquipo(
                    txt_nombre.get(),
                    txt_precio.get(),
                    txt_extra.get(),
                    disponible
                )

            elif tipo == "Asesoría especializada":
                servicio = AsesoriaEspecializada(
                    txt_nombre.get(),
                    txt_precio.get(),
                    txt_extra.get(),
                    disponible
                )

            else:
                raise ErrorTipoServicio("Debe seleccionar un tipo de servicio.")

            GestorServicios.agregar(servicio)

            Logger.registrar_evento(
                "Servicio creado correctamente",
                "Servicios"
            )

        except Exception as error:
            Logger.registrar_error(
                error,
                "Servicios",
                "Error al crear servicio"
            )

            messagebox.showerror("Error", str(error))

        else:
            messagebox.showinfo(
                "Éxito",
                "Servicio registrado correctamente."
            )

            cargar_tabla()
            limpiar()

        finally:
            print("Proceso de registro de servicio finalizado.")

    def ver_servicio(servicio):

        try:
            costo = servicio.calcular_costo(
                duracion=2,
                descuento=5,
                impuesto=19
            )

            mensaje = (
                f"{servicio.descripcion()}\n\n"
                f"Precio base: ${servicio.precio_base:,.0f}\n"
                f"Duración evaluada: 2 horas\n"
                f"Descuento aplicado: 5%\n"
                f"Impuesto aplicado: 19%\n"
                f"Costo final calculado: ${costo:,.0f}"
            )

            Logger.registrar_evento(
                "Consulta de costo realizada correctamente",
                "Servicios"
            )

            messagebox.showinfo("Detalle Servicio", mensaje)

        except Exception as error:
            Logger.registrar_error(
                error,
                "Servicios",
                "Error al consultar servicio"
            )

            messagebox.showerror("Error", str(error))

    def eliminar_servicio(indice):

        if messagebox.askyesno(
            "Confirmar",
            "¿Desea eliminar este servicio?"
        ):
            try:
                GestorServicios.eliminar(indice)

                Logger.registrar_evento(
                    "Servicio eliminado correctamente",
                    "Servicios"
                )

                cargar_tabla()

            except Exception as error:
                Logger.registrar_error(
                    error,
                    "Servicios",
                    "Error al eliminar servicio"
                )

                messagebox.showerror("Error", str(error))

    def click_tabla(evento):

        fila = tabla.identify_row(evento.y)
        columna = tabla.identify_column(evento.x)

        if not fila:
            return

        indice = int(fila)
        servicio = GestorServicios.obtener(indice)

        if columna == "#6":
            ver_servicio(servicio)

        elif columna == "#7":
            eliminar_servicio(indice)

    def cambiar_etiqueta(evento=None):

        tipo = combo_tipo.get()

        if tipo == "Reserva de sala":
            lbl_extra.config(text="Capacidad")

        elif tipo == "Alquiler de equipo":
            lbl_extra.config(text="Tipo de equipo")

        elif tipo == "Asesoría especializada":
            lbl_extra.config(text="Especialidad")

        else:
            lbl_extra.config(text="Dato adicional")

    # ======================================================
    # DISEÑO DE VENTANA
    # ======================================================
    ventana = Toplevel()
    ventana.title("Servicios")
    ventana.geometry("900x620")
    ventana.configure(bg="#f4f6f8")

    Label(
        ventana,
        text="GESTIÓN DE SERVICIOS",
        font=("Arial", 18, "bold"),
        bg="#f4f6f8"
    ).pack(pady=15)

    marco = LabelFrame(
        ventana,
        text=" Información del Servicio ",
        padx=15,
        pady=15,
        bg="white"
    )

    marco.pack(
        padx=15,
        pady=10,
        fill="x"
    )

    Label(marco, text="Tipo", bg="white").grid(row=0, column=0, sticky="w")
    combo_tipo = ttk.Combobox(
        marco,
        width=30,
        state="readonly",
        values=[
            "Reserva de sala",
            "Alquiler de equipo",
            "Asesoría especializada"
        ]
    )
    combo_tipo.grid(row=0, column=1, padx=8, pady=5)
    combo_tipo.bind("<<ComboboxSelected>>", cambiar_etiqueta)

    Label(marco, text="Nombre", bg="white").grid(row=1, column=0, sticky="w")
    txt_nombre = Entry(marco, width=33)
    txt_nombre.grid(row=1, column=1, padx=8, pady=5)

    Label(marco, text="Precio base", bg="white").grid(row=2, column=0, sticky="w")
    txt_precio = Entry(marco, width=33)
    txt_precio.grid(row=2, column=1, padx=8, pady=5)

    lbl_extra = Label(marco, text="Dato adicional", bg="white")
    lbl_extra.grid(row=3, column=0, sticky="w")

    txt_extra = Entry(marco, width=33)
    txt_extra.grid(row=3, column=1, padx=8, pady=5)

    Label(marco, text="Disponible", bg="white").grid(row=4, column=0, sticky="w")
    combo_disponible = ttk.Combobox(
        marco,
        width=30,
        state="readonly",
        values=["Sí", "No"]
    )
    combo_disponible.grid(row=4, column=1, padx=8, pady=5)
    combo_disponible.set("Sí")

    Button(
        ventana,
        text="Guardar Servicio",
        width=25,
        bg="#1976d2",
        fg="white",
        command=guardar
    ).pack(pady=10)

    columnas = (
        "ID",
        "Nombre",
        "Tipo",
        "Precio",
        "Disponible",
        "Ver",
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
    tabla.column("Nombre", width=190)
    tabla.column("Tipo", width=180)
    tabla.column("Precio", width=100)
    tabla.column("Disponible", width=90)
    tabla.column("Ver", width=80)
    tabla.column("Eliminar", width=90)

    tabla.pack(
        padx=15,
        pady=10,
        fill="both",
        expand=True
    )

    tabla.bind("<Button-1>", click_tabla)

    cargar_tabla()