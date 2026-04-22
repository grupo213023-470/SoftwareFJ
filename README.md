# SoftwareFJ
# Sistema Integral de Gestión de Clientes, Servicios y Reservas

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **Sistema Integral de Gestión de Clientes, Servicios y Reservas** para la Universidad Nacional Abierta y a Distancia - UNAD para el curso de Programación 213023A_2201 - Periodo 16-01 - 2026, implementado en **Python** bajo el paradigma de **Programación Orientada a Objetos (POO)** y **sin uso de bases de datos**.

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

- Python 3.x
- Programación Orientada a Objetos
- Archivos `.txt` / `.log`
- Manejo de excepciones
- Consola / Interfaz gráfica (según implementación)

---

## Principios de POO Aplicados

### Abstracción
Uso de clases abstractas para definir estructuras generales del sistema.

### Herencia
Clases derivadas que especializan comportamientos comunes.

### Polimorfismo
Métodos sobrescritos para cálculos, validaciones y descripciones de servicios.

### Encapsulación
Protección de atributos sensibles mediante getters, setters y validaciones internas.

---

## Estructura del Sistema

### Clase Abstracta Base
Representa entidades generales del sistema.

### Cliente
Gestiona información personal del cliente:

- Nombre
- Documento
- Teléfono
- Correo electrónico

Incluye validaciones estrictas.

### Servicio (Clase Abstracta)

Base para los servicios ofrecidos por Software FJ.

#### Servicios Especializados

- Reserva de salas
- Alquiler de equipos
- Asesorías especializadas

Cada uno implementa:

- Cálculo de costos
- Descripción personalizada
- Validación de parámetros

### Reserva

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
