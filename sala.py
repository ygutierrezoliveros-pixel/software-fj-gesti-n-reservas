"""Servicio de reserva de salas."""

from numbers import Integral

from excepciones import ErrorParametroServicio
from servicio import Servicio


class ReservaSala(Servicio):
    """Servicio de sala; la tarifa se cobra por unidad de duración."""

    def __init__(
        self,
        identificador: str,
        nombre: str,
        tarifa_base: float,
        capacidad: int,
        disponibilidad: bool = True,
    ) -> None:
        if (
            isinstance(capacidad, bool)
            or not isinstance(capacidad, Integral)
            or capacidad <= 0
        ):
            raise ErrorParametroServicio(
                "La capacidad debe ser un entero positivo."
            )
        super().__init__(identificador, nombre, tarifa_base, disponibilidad)
        self._capacidad = int(capacidad)

    @property
    def capacidad(self) -> int:
        return self._capacidad

    @property
    def capacidad_maxima_reserva(self) -> int:
        return self.capacidad

    def validar_parametros(self) -> None:
        super().validar_parametros()
        if (
            isinstance(self._capacidad, bool)
            or not isinstance(self._capacidad, int)
            or self._capacidad <= 0
        ):
            raise ErrorParametroServicio(
                "La capacidad debe ser un entero positivo."
            )

    def calcular_costo(
        self,
        duracion: float,
        *,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        return super().calcular_costo(
            duracion,
            impuesto=impuesto,
            descuento=descuento,
        )

    def describir(self) -> str:
        return (
            f"Sala {self.nombre} (capacidad: {self.capacidad}; "
            f"tarifa por unidad: {self.tarifa_base:.2f})."
        )

    def to_dict(self) -> dict[str, object]:
        return {**super().to_dict(), "capacidad": self.capacidad}
