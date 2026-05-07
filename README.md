# SoftwareFJ
# Sistema Integral de Gestión de Clientes, Servicios y Reservas

## Índice
* [Descripción del Proyecto](#descripción-del-proyecto) 
* [Objetivo General](#objetivo-general)
* [Modulo Clientes](#modulo-clientes)
* [Modulo Servicios ( sin asignar )](#modulo-servicios)
* [Modulo Reservas ( sin asignar )](#modulo-reservas)
* [Modulo Logs (Registro de excepciones)](#modulo-logs)


## Integrantes del Proyecto

- ARMANDO GUILLERMO TROUT GARCIA
- JESUS DANIEL GUZMAN CARMONA

## Tutora
- Ing.  MAIRA ALEJANDRA DIAZ MEJIA  

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **Sistema Integral de Gestión de Clientes, Servicios y Reservas** para la Universidad Nacional Abierta y a Distancia - UNAD para el curso de Programación 213023A_2201 - Grupo 213023_470 - Periodo 16-01 - 2026, implementado en **Python** bajo el paradigma de **Programación Orientada a Objetos (POO)** y **sin uso de bases de datos**.

El sistema permite administrar clientes, servicios y reservas mediante estructuras en memoria, listas internas y archivos para el registro de eventos y errores.

La solución fue diseñada para ser:

- Modular  
- Escalable  
- Robusta  
- Mantenible  
- Extensible  

Además, implementa manejo avanzado de excepciones para garantizar la continuidad operativa ante errores.

---

## Objetivo General

Desarrollar una aplicación orientada a objetos capaz de gestionar clientes, servicios y reservas de forma segura y eficiente, aplicando correctamente los principios fundamentales de POO y técnicas avanzadas de manejo de errores.

---

## Tecnologías Utilizadas

- Python 3.11.4
- Programación Orientada a Objetos
- Manejo de excepciones
- Interfaz gráfica usando Tkinter

---

## Principios de POO Aplicados

Abstracción, Herencia, Polimorfismo, Encapsulación.



---
## Sobrecarga de Métodos

El sistema incluye variantes de cálculo como:

- Costo base
- Costo con impuestos
- Costo con descuento
- Costo con parámetros opcionales

---

## Manejo de Excepciones Implementado

Se aplican estructuras como:

```python
try / except
try / except / else
try / except / finally
```
---

# Estructura del Sistema

---
### Modulo Clientes

Módulo desarrollado en **Python + Tkinter** para la gestión de clientes dentro del sistema principal.

## Funcionalidades

- Registrar clientes
- Editar clientes
- Eliminar clientes
- Buscar clientes
- Ver detalle del cliente
- Selección de país desde API externa
- Validaciones de datos
- Registro de eventos y errores en archivo logs

## Programación Orientada a Objetos

### Clase `Cliente`
Representa la entidad cliente.

**Encapsulación aplicada:**

- `__id`
- `__fecha`
- `__nombre`
- `__apellido`
- `__documento`
- `__correo`
- `__telefono`

Acceso controlado mediante `@property` y setters.

### Clase `GestorClientes`

Administra la lista en memoria de clientes.

Métodos:

- `agregar()`
- `obtener()`
- `obtener_todos()`
- `eliminar()`
- `buscar()`

## Validaciones

- Nombre obligatorio
- Apellido obligatorio
- Documento mínimo 6 caracteres
- Teléfono mínimo 7 caracteres
- Correo con formato válido

---

### Modulo Servicios (Clase Abstracta)

Base para los servicios ofrecidos por Software FJ.

#### Servicios Especializados

- Reserva de salas
- Alquiler de equipos
- Asesorías especializadas

Cada uno implementa:

- Cálculo de costos
- Descripción personalizada
- Validación de parámetros

---
### Modulo Reserva

Relaciona:

- Cliente
- Servicio
- Duración
- Estado

Funciones:

- Confirmar reserva
- Cancelar reserva
- Procesar reserva





---

### Modulo logs

Gestiona el registro de eventos y errores del sistema, además de mostrar una ventana gráfica para consultar los logs.

### Funciones principales

- **Logger.registrar_evento(mensaje, modulo)**  
  Guarda eventos normales del sistema en `logs.txt`.

- **Logger.registrar_error(excepcion, modulo, detalle_extra)**  
  Registra excepciones capturadas con información detallada.

- **abrir_logs()**  
  Abre una ventana modal en Tkinter para visualizar el archivo de logs, con opciones de:
  - Actualizar registros
  - Limpiar logs (con confirmación)
  - Scroll vertical y horizontal

### Archivo generado

- **logs.txt**  
  Contiene los registros en formato JSON, una línea por evento.

### Ejemplo de uso

```python
from logs import Logger, abrir_logs

try:
    x = int("abc")
except Exception as e:
    Logger.registrar_error(e, "Clientes", "Conversión inválida")

Logger.registrar_evento("Cliente Creado", "Clientes")
```