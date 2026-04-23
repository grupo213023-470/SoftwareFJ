from tkinter import *
from tkinter import messagebox
import json
from datetime import datetime
import traceback
import os


# =====================================================
# CLASE LOGGER
# Guarda errores y eventos en logs.txt en formato JSON
# =====================================================
class Logger:

    ARCHIVO_LOG = "logs.txt"  # Archivo donde se guardan los logs

    @staticmethod  # staticmethod para poder llamar sin crear instancia
    def registrar_error(excepcion, modulo="Sistema", detalle_extra=""):
        """
        Guarda errores del sistema
        """
        log = {
            "tipo": "ERROR",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modulo": modulo,
            "excepcion": type(excepcion).__name__,
            "mensaje": str(excepcion),
            "detalle": detalle_extra,
            "traceback": traceback.format_exc()
        }

        with open(Logger.ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(log, ensure_ascii=False) + "\n")

    @staticmethod 
    def registrar_evento(mensaje, modulo="Sistema"):
        """
        Guarda eventos normales
        """
        log = {
            "tipo": "INFO",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modulo": modulo,
            "mensaje": mensaje
        }

        with open(Logger.ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(log, ensure_ascii=False) + "\n")


# =====================================================
# VENTANA PARA MOSTRAR LOGS
# =====================================================
def ventana_logs():

    # Crear ventana secundaria
    ventana = Toplevel()
    ventana.title("Logs del Sistema")
    ventana.geometry("800x500")
    
    ventana.transient()
    ventana.grab_set()
    ventana.focus_force() # Asegura que la ventana tenga el foco al abrirse

    # Título principal
    Label(
        ventana,
        text="LOGS DEL SISTEMA",
        font=("Arial", 16, "bold")
    ).pack(pady=10)

    # =================================================
    # FRAME CONTENEDOR DEL TEXT Y SCROLLS
    # =================================================
    frame_texto = Frame(ventana)
    frame_texto.pack(padx=10, pady=5, fill=BOTH, expand=True)

    # Scroll vertical
    scroll_y = Scrollbar(frame_texto, orient=VERTICAL)

    # Scroll horizontal
    scroll_x = Scrollbar(frame_texto, orient=HORIZONTAL)

    # Caja de texto
    area_texto = Text(
        frame_texto,
        wrap=NONE,
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set
    )

    # Configurar scrollbars
    scroll_y.config(command=area_texto.yview)
    scroll_x.config(command=area_texto.xview)

    # Posicionar elementos
    scroll_y.pack(side=RIGHT, fill=Y)
    scroll_x.pack(side=BOTTOM, fill=X)
    area_texto.pack(side=LEFT, fill=BOTH, expand=True)

    # =================================================
    # FUNCIÓN CARGAR LOGS
    # =================================================
    def cargar_logs():

        area_texto.config(state="normal")
        area_texto.delete("1.0", END)

        try:
            if os.path.exists(Logger.ARCHIVO_LOG):

                with open(Logger.ARCHIVO_LOG, "r", encoding="utf-8") as archivo:

                    lineas = archivo.readlines()

                    if not lineas:
                        area_texto.insert(END, "No hay registros.")

                    for linea in lineas:

                        try:
                            dato = json.loads(linea)

                            texto = (
                                f"[{dato.get('fecha')}] "
                                f"{dato.get('tipo')} - "
                                f"{dato.get('modulo')} -> "
                                f"{dato.get('mensaje', dato.get('detalle', ''))}\n"
                            )

                            area_texto.insert(END, texto)

                        except:
                            area_texto.insert(END, linea)

            else:
                area_texto.insert(END, "Archivo logs.txt no existe.")

        except Exception as e:

            messagebox.showerror("Error", str(e))
            Logger.registrar_error(e, "Logs", "Error al cargar logs")

        area_texto.config(state="disabled")

    # =================================================
    # FUNCIÓN LIMPIAR LOGS
    # =================================================
    def limpiar_logs():

        respuesta = messagebox.askyesno(
            "Confirmación",
            "¿Seguro que deseas borrar todos los logs?"
        )

        if respuesta:

            try:
                # Vaciar archivo
                with open(Logger.ARCHIVO_LOG, "w", encoding="utf-8") as archivo:
                    archivo.write("")

                # Registrar evento nuevo
                Logger.registrar_evento(
                    "Archivo de logs limpiado",
                    "Logs"
                )

                # Recargar pantalla
                cargar_logs()

            except Exception as e:
                messagebox.showerror("Error", str(e))
                Logger.registrar_error(
                    e,
                    "Logs",
                    "Error al limpiar logs"
                )

    # =================================================
    # FRAME BOTONES
    # =================================================
    frame_botones = Frame(ventana)
    frame_botones.pack(pady=8)

    # Botón actualizar
    Button(
        frame_botones,
        text="Actualizar",
        font=("Arial", 11, "bold"),
        width=18,
        command=cargar_logs
    ).pack(side=LEFT, padx=5)

    # Botón limpiar
    Button(
        frame_botones,
        text="Limpiar",
        font=("Arial", 11, "bold"),
        width=18,
        command=limpiar_logs
    ).pack(side=LEFT, padx=5)

    # Cargar al abrir ventana
    cargar_logs()