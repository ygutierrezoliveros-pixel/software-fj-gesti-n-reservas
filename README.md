# Software FJ

Sistema Integral de Gestión de Clientes, Servicios y Reservas.

Proyecto para el curso Programación 213023_511 de la
Universidad Nacional Abierta y a Distancia (UNAD).

## Objetivo

Aplicación orientada a objetos para gestionar clientes, servicios y reservas,
con validaciones, excepciones personalizadas y registro de eventos y errores.
Los datos del negocio se conservan en listas en memoria; los archivos se usan
únicamente para logs.

## Clases implementadas

- `EntidadBase`: contrato abstracto para las entidades.
- `Cliente`: datos de identificación y contacto con validaciones.
- `Servicio`: contrato común y cálculo del costo.
- `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`: servicios concretos.
- `Reserva`: relación entre un cliente y un servicio, con control de estados.
- `GestorSoftwareFJ`: administración en memoria de clientes, servicios y reservas.

## Cálculo de costos

La tarifa base se cobra por unidad de duración (horas para asesoría):

```text
costo = tarifa_base * duracion * (1 - descuento) * (1 + impuesto)
```

`impuesto` y `descuento` se expresan como proporciones: `0.19` equivale a 19 %
y `0.10` equivale a 10 %. El descuento debe estar entre 0 (incluido) y 1
(excluido); el impuesto debe ser no negativo. La duración y la tarifa deben ser
positivas y finitas. El equipo se cobra por unidad alquilada y unidad de
duración; las unidades disponibles determinan si el servicio puede reservarse.

## Estados de las reservas

- `PENDIENTE` puede pasar a `CONFIRMADA` o `CANCELADA`.
- `CONFIRMADA` puede pasar a `CANCELADA`.
- `CANCELADA` es terminal: no puede confirmarse ni cancelarse de nuevo.
- El procesamiento calcula el costo de una reserva confirmada sin cambiar su
  estado.

## Calendario y capacidad

Las reservas pueden incluir fecha y hora de entrada/salida, cantidad de
personas y modalidad (`POR_HORAS`, `DIA_COMPLETO` o `NOCHE_COMPLETA`). Al
indicar el horario, la duración se calcula automáticamente en horas. Los
horarios exactos de día y noche los define quien crea la reserva; el sistema no
presupone una hora universal de entrada o salida.

Las salas y lugares con capacidad limitan tanto las personas de cada reserva
como el aforo total de reservas simultáneas. Las asesorías personalizadas
admiten una persona por cita y no se pueden solapar para el mismo servicio. Las
reservas canceladas dejan de ocupar capacidad.

Ejemplo:

```python
from datetime import datetime
from reserva import ModalidadReserva

reserva = gestor.crear_reserva(
    "R-10",
    "C-1",
    "S-1",
    fecha_hora_entrada=datetime(2026, 12, 1, 18, 0),
    fecha_hora_salida=datetime(2026, 12, 2, 8, 0),
    cantidad_personas=4,
    modalidad=ModalidadReserva.NOCHE_COMPLETA,
)
```

## Ejecución

Requiere Python 3.12 o posterior y no necesita bibliotecas externas.

Ejecuta la simulación de operaciones válidas e inválidas:

```bash
python main.py
```

La simulación ejecuta al menos 10 operaciones válidas completas, además de
operaciones inválidas para demostrar las validaciones. Reporta las operaciones
ejecutadas, completadas y rechazadas, así como el número de clientes, servicios
y reservas que permanecen en memoria. Los errores inesperados se registran y
se informan sin impedir que se intenten las operaciones posteriores.

## Registro de eventos

El logger registra operaciones y errores en:

```text
logs/software_fj.log
```

No se deben registrar datos personales completos ni información sensible.
