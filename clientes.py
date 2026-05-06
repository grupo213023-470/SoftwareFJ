from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import re
import requests
from logs import Logger


# ==========================================================
# EXCEPCIONES
# ==========================================================
class ErrorCliente(Exception): 
    pass


class ErrorCorreo(ErrorCliente):
    pass


class ErrorDocumento(ErrorCliente):
    pass


class ErrorTelefono(ErrorCliente):
    pass


# ==========================================================
# CLASE CLIENTE
# ==========================================================
class Cliente:

    contador = 1

    def __init__(
        self,
        nombre,
        apellido,
        documento,
        correo,
        telefono,
        empresa="",
        direccion="",
        departamento="",
        ciudad="",
        pais=""
    ):

        # ENCAPSULACIÓN
        self.__id = Cliente.contador
        Cliente.contador += 1

        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

        self.empresa = empresa
        self.direccion = direccion
        self.departamento = departamento
        self.ciudad = ciudad
        self.pais = pais

        self.__fecha = datetime.now()

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor.strip():
            raise ErrorCliente("Nombre obligatorio.")
        self.__nombre = valor.title()

    @property
    def apellido(self):
        return self.__apellido

    @apellido.setter
    def apellido(self, valor):
        if not valor.strip():
            raise ErrorCliente("Apellido obligatorio.")
        self.__apellido = valor.title()

    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if len(valor.strip()) < 6:
            raise ErrorDocumento("Documento mínimo 6 caracteres.")
        self.__documento = valor.strip()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):

        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$' # expresión regular básica para validar formato de correo

        if not re.match(patron, valor):
            raise ErrorCorreo("Correo inválido.")

        self.__correo = valor.lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if len(valor.strip()) < 7:
            raise ErrorTelefono("Teléfono mínimo 7 caracteres.")
        self.__telefono = valor.strip()

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def actualizar(
        self,
        nombre,
        apellido,
        documento,
        correo,
        telefono,
        empresa,
        direccion,
        departamento,
        ciudad,
        pais
    ):

        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.empresa = empresa
        self.direccion = direccion
        self.departamento = departamento
        self.ciudad = ciudad
        self.pais = pais

    def detalle(self):

        return f"""
                Nombre: {self.nombre}
                Apellido: {self.apellido}
                Documento: {self.documento}
                Correo: {self.correo}
                Teléfono: {self.telefono}
                Empresa: {self.empresa}
                Dirección: {self.direccion}
                Departamento: {self.departamento}
                Ciudad: {self.ciudad}
                País: {self.pais}
                Fecha Registro: {self.__fecha.strftime('%d/%m/%Y %H:%M:%S')}
                """


# ==========================================================
# GESTOR
# ==========================================================
class GestorClientes:

    __lista = []

    @classmethod
    def agregar(cls, cliente):
        cls.__lista.append(cliente)

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

        for cliente in cls.__lista:

            if (
                texto in cliente.nombre.lower()
                or texto in cliente.apellido.lower()
                or texto in cliente.documento.lower()
            ):
                resultados.append(cliente)

        return resultados


# ==========================================================
# VENTANA PRINCIPAL
# ==========================================================
def ventana_clientes():

    ventanas_detalle = {}

    # ======================================================
    # FUNCIONES
    # ======================================================
    def mover_foco(evento):
        evento.widget.tk_focusNext().focus()
        return "break"

    # ------------------------------------------------------
    def cargar_paises():

        try:
            url = "https://countriesnow.space/api/v0.1/countries"
            respuesta = requests.get(url, timeout=10)
            datos = respuesta.json()

            paises = []

            for item in datos["data"]:
                paises.append(item["country"])

            combo_pais["values"] = sorted(paises)

        except Exception as error:

            Logger.registrar_error(
                error,
                "Clientes",
                "Error cargando países"
            )

            combo_pais["values"] = [
                "Colombia",
                "México",
                "Perú",
                "Chile"
            ]

    # ------------------------------------------------------
    def limpiar():

        for campo in campos:
            if isinstance(campo, ttk.Combobox):
                campo.set("")
            else:
                campo.delete(0, END)

    # ------------------------------------------------------
    def cargar_tabla(lista=None):

        tabla.delete(*tabla.get_children())

        if lista is None:
            lista = GestorClientes.obtener_todos()

        for i, cliente in enumerate(lista):

            tabla.insert(
                "",
                END,
                iid=i,
                values=(
                    cliente.nombre_completo(),
                    cliente.documento,
                    cliente.empresa,
                    "Ver",
                    "Editar",
                    "Eliminar"
                )
            )

    # ------------------------------------------------------
    def guardar():

        try:
            nuevo = Cliente(
                txt_nombre.get(),
                txt_apellido.get(),
                txt_documento.get(),
                txt_correo.get(),
                txt_telefono.get(),
                txt_empresa.get(),
                txt_direccion.get(),
                txt_departamento.get(),
                txt_ciudad.get(),
                combo_pais.get()
            )

            GestorClientes.agregar(nuevo)

            Logger.registrar_evento(
                "Clientes",
                "Cliente creado"
            )

            cargar_tabla()
            limpiar()

        except Exception as error:

            Logger.registrar_error(
                error,
                "Clientes",
                "Error guardando cliente"
            )

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ------------------------------------------------------
    def buscar(evento=None):

        texto = txt_buscar.get()

        if not texto.strip():
            cargar_tabla()
            return

        resultados = GestorClientes.buscar(texto)
        cargar_tabla(resultados)

    # ------------------------------------------------------
    def ver(cliente):

        if cliente.id in ventanas_detalle:

            if ventanas_detalle[
                cliente.id
            ].winfo_exists():

                ventanas_detalle[
                    cliente.id
                ].lift() # trae la ventana al frente

                return

        v = Toplevel() # nueva ventana para mostrar detalles
        v.title("Detalle Cliente")
        v.geometry("430x430") # tamaño fijo para evitar scroll

        ventanas_detalle[cliente.id] = v  # guarda referencia para evitar múltiples ventanas

        Label(
            v,
            text="DETALLE CLIENTE",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        Label(
            v,
            text=cliente.detalle(),
            justify=LEFT,
            font=("Consolas", 10)
        ).pack(padx=15)

    # ------------------------------------------------------
    def editar(indice):

        cliente = GestorClientes.obtener(indice) 

        v = Toplevel()
        v.title("Editar Cliente")
        v.geometry("420x520")

        entradas = {}

        campos_editar = [
            ("Nombre", cliente.nombre),
            ("Apellido", cliente.apellido),
            ("Documento", cliente.documento),
            ("Correo", cliente.correo),
            ("Teléfono", cliente.telefono),
            ("Empresa", cliente.empresa),
            ("Dirección", cliente.direccion),
            ("Departamento", cliente.departamento),
            ("Ciudad", cliente.ciudad),
            ("País", cliente.pais)
        ]

        for texto, valor in campos_editar:

            Label(v, text=texto).pack()
            caja = Entry(v, width=35)
            caja.pack()
            caja.insert(0, valor)

            entradas[texto] = caja

        def guardar_cambios():

            try:

                cliente.actualizar(
                    entradas["Nombre"].get(),
                    entradas["Apellido"].get(),
                    entradas["Documento"].get(),
                    entradas["Correo"].get(),
                    entradas["Teléfono"].get(),
                    entradas["Empresa"].get(),
                    entradas["Dirección"].get(),
                    entradas["Departamento"].get(),
                    entradas["Ciudad"].get(),
                    entradas["País"].get()
                )

                # registra evento de edición
                Logger.registrar_evento(
                    "Clientes",
                    "Cliente editado"
                )

                cargar_tabla()
                v.destroy()

            except Exception as error:

                Logger.registrar_error(
                    error,
                    "Clientes",
                    "Error editando cliente"
                )

                messagebox.showerror(
                    "Error",
                    str(error)
                )

        Button(
            v,
            text="Guardar Cambios",
            command=guardar_cambios
        ).pack(pady=10)

    # ------------------------------------------------------
    def eliminar(indice):

        if messagebox.askyesno(
            "Confirmar",
            "¿Eliminar cliente?"
        ):

            GestorClientes.eliminar(indice)
            cargar_tabla()

    # ------------------------------------------------------
    def click_tabla(evento):

        fila = tabla.identify_row(evento.y)
        columna = tabla.identify_column(evento.x)

        if not fila:
            return

        indice = int(fila)
        cliente = GestorClientes.obtener(indice)

        if columna == "#4":
            ver(cliente)

        elif columna == "#5":
            editar(indice)

        elif columna == "#6":
            eliminar(indice)

    # ======================================================
    # VENTANA
    # ======================================================
    ventana = Toplevel()
    ventana.title("Clientes")
    ventana.geometry("1120x760")
    ventana.configure(bg="#f4f6f8")

    # ======================================================
    # ESTILOS
    # ======================================================
    estilo = ttk.Style()
    estilo.theme_use("default")

    estilo.configure(
        "Treeview",
        rowheight=28,
        font=("Segoe UI", 10)
    )

    estilo.configure(
        "Treeview.Heading",
        font=("Segoe UI", 10, "bold")
    )

    # ======================================================
    Label(
        ventana,
        text="GESTIÓN DE CLIENTES",
        font=("Segoe UI", 18, "bold"),
        bg="#f4f6f8"
    ).pack(pady=10)

    # ======================================================
    # BUSCADOR
    # ======================================================
    marco_buscar = Frame(
        ventana,
        bg="#f4f6f8"
    )
    marco_buscar.pack(fill="x", padx=15)

    Label(
        marco_buscar,
        text="Buscar:",
        bg="#f4f6f8"
    ).pack(side=LEFT)

    txt_buscar = Entry(
        marco_buscar,
        width=35
    )
    txt_buscar.pack(side=LEFT, padx=5) # ENTER en el buscador filtra resultados
    txt_buscar.bind("<KeyRelease>", buscar) # filtrar resultados al escribir

    Button(
        marco_buscar,
        text="Mostrar Todos",
        command=cargar_tabla
    ).pack(side=LEFT)

    # ======================================================
    # FORMULARIO
    # ======================================================
    marco = LabelFrame(
        ventana,
        text=" Información Cliente ",
        padx=15,
        pady=15,
        bg="white"
    )

    marco.pack(
        padx=15,
        pady=10,
        fill="x"
    )

    marco.grid_columnconfigure(0, minsize=90)
    marco.grid_columnconfigure(1, minsize=220)
    marco.grid_columnconfigure(2, minsize=90)
    marco.grid_columnconfigure(3, minsize=220)

    Label(marco, text="Nombre", bg="white").grid(row=0, column=0, sticky="w")
    txt_nombre = Entry(marco, width=28)
    txt_nombre.grid(row=0, column=1, padx=5, pady=10)

    Label(marco, text="Apellido", bg="white").grid(row=0, column=2, sticky="w")
    txt_apellido = Entry(marco, width=28)
    txt_apellido.grid(row=0, column=3, padx=5, pady=10)

    Label(marco, text="Documento", bg="white").grid(row=1, column=0, sticky="w")
    txt_documento = Entry(marco, width=28)
    txt_documento.grid(row=1, column=1, padx=5, pady=10)

    Label(marco, text="Correo", bg="white").grid(row=1, column=2, sticky="w")
    txt_correo = Entry(marco, width=28)
    txt_correo.grid(row=1, column=3, padx=5, pady=10)

    Label(marco, text="Teléfono", bg="white").grid(row=2, column=0, sticky="w")
    txt_telefono = Entry(marco, width=28)
    txt_telefono.grid(row=2, column=1, padx=5, pady=10)

    Label(marco, text="Empresa", bg="white").grid(row=2, column=2, sticky="w")
    txt_empresa = Entry(marco, width=28)
    txt_empresa.grid(row=2, column=3, padx=5, pady=10)

    Label(marco, text="Dirección", bg="white").grid(row=3, column=0, sticky="w")
    txt_direccion = Entry(marco, width=28)
    txt_direccion.grid(row=3, column=1, columnspan=3, padx=5,sticky="we",pady=10)

    Label(marco, text="Departamento", bg="white").grid(row=4, column=0, sticky="w")
    txt_departamento = Entry(marco, width=28)
    txt_departamento.grid(row=4, column=1, padx=5, pady=10)

    Label(marco, text="Ciudad", bg="white").grid(row=4, column=2, sticky="w")
    txt_ciudad = Entry(marco, width=28)
    txt_ciudad.grid(row=4, column=3, padx=5, pady=10)

    Label(marco, text="País", bg="white").grid(row=5, column=0, sticky="w")
    combo_pais = ttk.Combobox(
        marco,
        width=26,
        state="readonly"
    )
    combo_pais.grid(row=5, column=1, padx=5, pady=10)

    Button(
        ventana,
        text="Guardar Cliente",
        width=24,
        bg="#1976d2",
        fg="white",
        command=guardar
    ).pack(pady=12)

    # ======================================================
    # TABLA
    # ======================================================
    columnas = (
        "Nombre",
        "Documento",
        "Empresa",
        "Ver",
        "Editar",
        "Eliminar"
    )

    tabla = ttk.Treeview(
        ventana,
        columns=columnas,
        show="headings",
        height=16
    )

    for col in columnas:
        tabla.heading(col, text=col)

    tabla.column("Nombre", width=260)
    tabla.column("Documento", width=170)
    tabla.column("Empresa", width=200)
    tabla.column("Ver", width=80)
    tabla.column("Editar", width=80)
    tabla.column("Eliminar", width=90)

    tabla.pack(padx=15, pady=10, fill="both")

    tabla.bind("<Button-1>", click_tabla)

    # ======================================================
    # ENTER CAMBIA FOCO
    # ======================================================
    campos = [
        txt_nombre,
        txt_apellido,
        txt_documento,
        txt_correo,
        txt_telefono,
        txt_empresa,
        txt_direccion,
        txt_departamento,
        txt_ciudad,
        combo_pais
    ]

    for campo in campos:
        campo.bind("<Return>", mover_foco) # ENTER mueve foco al siguiente campo

    combo_pais.bind(
        "<Return>",
        lambda e: guardar()
    )

    cargar_paises()
    cargar_tabla()