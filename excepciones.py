"""Excepciones personalizadas del sistema Software FJ.

Este módulo centraliza los errores controlados relacionados con
clientes, servicios, reservas, operaciones y registro de eventos.
"""


class ErrorSoftwareFJ(Exception):
    """Representa un error controlado del sistema Software FJ."""


class ErrorValidacion(ErrorSoftwareFJ):
    """Indica que un dato no cumple las reglas de validación."""


class ErrorParametroFaltante(ErrorValidacion):
    """Indica que falta un dato obligatorio de una operación."""


class ErrorCliente(ErrorValidacion):
    """Representa errores de validación de datos de clientes."""


class ErrorClienteDuplicado(ErrorCliente):
    """Indica que ya existe un cliente con la misma identificación."""


class ErrorServicio(ErrorSoftwareFJ):
    """Representa un error relacionado con los servicios."""


class ErrorParametroServicio(ErrorServicio, ErrorValidacion):
    """Indica que un parámetro del servicio es inválido."""


class ErrorServicioNoDisponible(ErrorServicio):
    """Indica que el servicio solicitado no está disponible."""


class ErrorCalculo(ErrorServicio):
    """Indica valores o resultados inconsistentes en un costo."""


class ErrorReserva(ErrorSoftwareFJ):
    """Representa un error relacionado con una reserva."""


class ErrorOperacionNoPermitida(ErrorSoftwareFJ):
    """Indica que una operación incumple las reglas del sistema."""


class ErrorEstadoReserva(ErrorReserva, ErrorOperacionNoPermitida):
    """Indica una operación incompatible con el estado de una reserva."""


class ErrorRegistro(ErrorSoftwareFJ):
    """Indica un fallo al configurar el registro de eventos."""


# Compatibilidad con los nombres anteriores del proyecto.
SoftwareFJError = ErrorSoftwareFJ
ClienteInvalidoError = ErrorCliente
ServicioNoDisponibleError = ErrorServicioNoDisponible
ReservaInvalidaError = ErrorReserva
CalculoInconsistenteError = ErrorCalculo
