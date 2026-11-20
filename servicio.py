"""Contrato y cálculo compartido para los servicios del sistema."""

import math
from abc import abstractmethod
from numbers import Real

from base import EntidadBase
from excepciones import (
    ErrorCalculo,
    ErrorParametroServicio,
    ErrorServicioNoDisponible,
)


class Servicio(EntidadBase):
    """Define el contrato común de los servicios reservables.

    El costo aplica primero el descuento y luego el impuesto:
    tarifa_base * duracion * (1 - descuento) * (1 + impuesto).
    Impuesto y descuento se expresan como proporciones entre cero y uno;
    el impuesto puede ser mayor que uno, pero el descuento debe ser menor
    que uno para que el costo resultante siga siendo positivo.
    """

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: Real,
        disponibilidad: bool = True,
    ) -> None:
        self._identificador = self._validar_texto(
            identificador, "identificador"
        )
        self._nombre = self._validar_texto(nombre, "nombre")
        self._tarifa_base = self._validar_tarifa(tarifa_base)
        if not isinstance(disponibilidad, bool):
            raise ErrorParametroServicio(
                "La disponibilidad debe ser un valor booleano."
            )
        self._disponibilidad = disponibilidad

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ErrorParametroServicio(f"El {campo} debe ser un texto no vacío.")
        return valor.strip()

    @staticmethod
    def _convertir_numero(valor: Real, campo: str) -> float:
        if isinstance(valor, bool) or not isinstance(valor, Real):
            raise ErrorParametroServicio(f"El {campo} debe ser numérico.")
        try:
            numero = float(valor)
        except (OverflowError, ValueError) as error:
            raise ErrorParametroServicio(f"El {campo} no es válido.") from error
        if not math.isfinite(numero):
            raise ErrorParametroServicio(f"El {campo} debe ser finito.")
        return numero

    @classmethod
    def _validar_tarifa(cls, tarifa: Real) -> float:
        numero = cls._convertir_numero(tarifa, "La tarifa")
        if numero <= 0:
            raise ErrorParametroServicio("La tarifa debe ser positiva.")
        return numero

    @property
    def identificador(self) -> str:
        return self._identificador

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponibilidad(self) -> bool:
        return self._disponibilidad

    @property
    def capacidad_maxima_reserva(self) -> int | None:
        return None

    @disponibilidad.setter
    def disponibilidad(self, disponibilidad: bool) -> None:
        if not isinstance(disponibilidad, bool):
            raise ErrorParametroServicio(
                "La disponibilidad debe ser un valor booleano."
            )
        self._disponibilidad = disponibilidad

    def validar_parametros(self) -> None:
        self._validar_texto(self._identificador, "identificador")
        self._validar_texto(self._nombre, "nombre")
        self._validar_tarifa(self._tarifa_base)
        if not isinstance(self.disponibilidad, bool):
            raise ErrorParametroServicio(
                "La disponibilidad debe ser un valor booleano."
            )

    def validar_disponibilidad(self) -> None:
        """Rechaza operaciones que requieren un servicio disponible."""
        if not self.disponibilidad:
            raise ErrorServicioNoDisponible(
                f"El servicio '{self.nombre}' no está disponible."
            )

    def validar(self) -> None:
        self.validar_parametros()

    def to_dict(self) -> dict[str, object]:
        return {
            "identificador": self.identificador,
            "nombre": self.nombre,
            "tarifa_base": self.tarifa_base,
            "disponibilidad": self.disponibilidad,
        }

    @abstractmethod
    def calcular_costo(
        self,
        duracion: float,
        *,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        self.validar_parametros()
        self.validar_disponibilidad()
        duracion_validada = self._convertir_numero(duracion, "La duración")
        if duracion_validada <= 0:
            raise ErrorParametroServicio("La duración debe ser positiva.")

        impuesto_validado = self._validar_tasa(
            impuesto, "El impuesto", minimo=0.0
        )
        descuento_validado = self._validar_tasa(
            descuento, "El descuento", minimo=0.0, maximo_exclusivo=1.0
        )
        costo = (
            self.tarifa_base
            * duracion_validada
            * (1.0 - descuento_validado)
            * (1.0 + impuesto_validado)
        )
        if not math.isfinite(costo) or costo <= 0:
            raise ErrorCalculo("El cálculo produjo un costo inconsistente.")
        return float(costo)

    @classmethod
    def _validar_tasa(
        cls,
        valor: Real,
        campo: str,
        *,
        minimo: float,
        maximo_exclusivo: float | None = None,
    ) -> float:
        try:
            tasa = cls._convertir_numero(valor, campo)
        except ErrorParametroServicio as error:
            raise ErrorCalculo(str(error)) from error
        if tasa < minimo or (
            maximo_exclusivo is not None and tasa >= maximo_exclusivo
        ):
            raise ErrorCalculo(f"{campo} está fuera del rango permitido.")
        return tasa

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible del servicio."""
