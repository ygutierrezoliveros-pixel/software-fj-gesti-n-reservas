"""Reservas que relacionan un cliente con un servicio."""

import math
from datetime import datetime
from enum import StrEnum
from numbers import Integral, Real

from cliente import Cliente
from excepciones import ErrorEstadoReserva, ErrorReserva
from servicio import Servicio


class ModalidadReserva(StrEnum):
    POR_HORAS = "POR_HORAS"
    DIA_COMPLETO = "DIA_COMPLETO"
    NOCHE_COMPLETA = "NOCHE_COMPLETA"


PENDIENTE = "PENDIENTE"
CONFIRMADA = "CONFIRMADA"
CANCELADA = "CANCELADA"


class Reserva:
    """Reserva con transiciones PENDIENTE→CONFIRMADA/CANCELADA.

    Una reserva confirmada también puede cancelarse. Una reserva cancelada
    es terminal y no admite nuevas confirmaciones ni cancelaciones.
    """

    def __init__(
        self,
        identificador: str,
        cliente: Cliente,
        servicio: Servicio,
        duracion: float | None = None,
        *,
        fecha_hora_entrada: datetime | None = None,
        fecha_hora_salida: datetime | None = None,
        cantidad_personas: int = 1,
        modalidad: ModalidadReserva | str = ModalidadReserva.POR_HORAS,
    ) -> None:
        if not isinstance(identificador, str) or not identificador.strip():
            raise ErrorReserva("El identificador debe ser un texto no vacío.")
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("La reserva requiere un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("La reserva requiere un servicio válido.")

        modalidad_validada = self._validar_modalidad(modalidad)
        intervalo = self._validar_intervalo(
            fecha_hora_entrada,
            fecha_hora_salida,
        )
        if intervalo is None:
            if modalidad_validada != ModalidadReserva.POR_HORAS:
                raise ErrorReserva(
                    "Las modalidades de día y noche requieren fecha y horas "
                    "de entrada y salida."
                )
            if duracion is None:
                raise ErrorReserva(
                    "La reserva requiere una duración o un horario completo."
                )
            duracion_validada = self._validar_duracion(duracion)
        else:
            duracion_calculada = (
                intervalo[1] - intervalo[0]
            ).total_seconds() / 3600
            if duracion is not None:
                duracion_indicada = self._validar_duracion(duracion)
                if not math.isclose(
                    duracion_indicada,
                    duracion_calculada,
                    rel_tol=1e-9,
                    abs_tol=1e-9,
                ):
                    raise ErrorReserva(
                        "La duración debe coincidir con las horas entre "
                        "la entrada y la salida."
                    )
            duracion_validada = self._validar_duracion(duracion_calculada)

        personas_validadas = self._validar_cantidad_personas(
            cantidad_personas
        )
        cliente.validar()
        servicio.validar_parametros()
        servicio.validar_disponibilidad()
        capacidad = servicio.capacidad_maxima_reserva
        if capacidad is not None and personas_validadas > capacidad:
            raise ErrorReserva(
                f"La reserva supera la capacidad de {capacidad} personas "
                f"del servicio '{servicio.nombre}'."
            )

        self._identificador = identificador.strip()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion_validada
        self._fecha_hora_entrada = fecha_hora_entrada
        self._fecha_hora_salida = fecha_hora_salida
        self._cantidad_personas = personas_validadas
        self._modalidad = modalidad_validada
        self._estado = PENDIENTE

    @staticmethod
    def _validar_modalidad(
        modalidad: ModalidadReserva | str,
    ) -> ModalidadReserva:
        try:
            return ModalidadReserva(modalidad)
        except (TypeError, ValueError) as error:
            raise ErrorReserva(
                "La modalidad debe ser POR_HORAS, DIA_COMPLETO "
                "o NOCHE_COMPLETA."
            ) from error

    @staticmethod
    def _validar_intervalo(
        entrada: datetime | None,
        salida: datetime | None,
    ) -> tuple[datetime, datetime] | None:
        if entrada is None and salida is None:
            return None
        if not isinstance(entrada, datetime) or not isinstance(
            salida, datetime
        ):
            raise ErrorReserva(
                "La entrada y la salida deben ser fechas y horas válidas."
            )
        if (entrada.utcoffset() is None) != (salida.utcoffset() is None):
            raise ErrorReserva(
                "La entrada y la salida deben usar la misma zona horaria."
            )
        if salida <= entrada:
            raise ErrorReserva(
                "La salida debe ser posterior a la entrada."
            )
        return entrada, salida

    @staticmethod
    def _validar_cantidad_personas(cantidad: int) -> int:
        if isinstance(cantidad, bool) or not isinstance(cantidad, Integral):
            raise ErrorReserva(
                "La cantidad de personas debe ser un entero positivo."
            )
        if cantidad <= 0:
            raise ErrorReserva(
                "La cantidad de personas debe ser un entero positivo."
            )
        return int(cantidad)

    @staticmethod
    def _validar_duracion(duracion: Real) -> float:
        if isinstance(duracion, bool) or not isinstance(duracion, Real):
            raise ErrorReserva("La duración debe ser un número positivo.")
        try:
            duracion_validada = float(duracion)
        except (OverflowError, ValueError) as error:
            raise ErrorReserva("La duración debe ser finita.") from error
        if not math.isfinite(duracion_validada) or duracion_validada <= 0:
            raise ErrorReserva("La duración debe ser un número positivo y finito.")
        return duracion_validada

    @property
    def identificador(self) -> str:
        return self._identificador

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        return self._servicio

    @property
    def duracion(self) -> float:
        return self._duracion

    @property
    def fecha_hora_entrada(self) -> datetime | None:
        return self._fecha_hora_entrada

    @property
    def fecha_hora_salida(self) -> datetime | None:
        return self._fecha_hora_salida

    @property
    def cantidad_personas(self) -> int:
        return self._cantidad_personas

    @property
    def modalidad(self) -> ModalidadReserva:
        return self._modalidad

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar(self) -> None:
        if self._estado != PENDIENTE:
            raise ErrorEstadoReserva(
                f"No se puede confirmar una reserva en estado {self._estado}."
            )
        self._cliente.validar()
        self._servicio.validar_parametros()
        self._servicio.validar_disponibilidad()
        self._validar_duracion(self._duracion)
        self._estado = CONFIRMADA

    def cancelar(self) -> None:
        if self._estado not in (PENDIENTE, CONFIRMADA):
            raise ErrorEstadoReserva(
                f"No se puede cancelar una reserva en estado {self._estado}."
            )
        self._estado = CANCELADA

    def procesar(
        self,
        *,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        if self._estado != CONFIRMADA:
            raise ErrorEstadoReserva(
                "Solo se puede procesar una reserva confirmada."
            )
        self._cliente.validar()
        self._servicio.validar_parametros()
        self._servicio.validar_disponibilidad()
        return self._servicio.calcular_costo(
            self._duracion,
            impuesto=impuesto,
            descuento=descuento,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "identificador": self.identificador,
            "cliente": self.cliente.get_identificacion(),
            "servicio": self.servicio.identificador,
            "duracion": self.duracion,
            "fecha_hora_entrada": (
                self.fecha_hora_entrada.isoformat()
                if self.fecha_hora_entrada is not None
                else None
            ),
            "fecha_hora_salida": (
                self.fecha_hora_salida.isoformat()
                if self.fecha_hora_salida is not None
                else None
            ),
            "cantidad_personas": self.cantidad_personas,
            "modalidad": self.modalidad.value,
            "estado": self.estado,
        }
