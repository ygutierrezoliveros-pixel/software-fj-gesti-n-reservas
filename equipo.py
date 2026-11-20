"""Servicio de alquiler de equipos."""

from numbers import Integral

from excepciones import ErrorParametroServicio
from servicio import Servicio


class AlquilerEquipo(Servicio):
    """Alquiler por equipo y unidad de duración; las unidades se validan."""

    def __init__(
        self,
        identificador: str,
        tipo_equipo: str,
        tarifa_base: float,
        unidades_disponibles: int,
    ) -> None:
        unidades = self._validar_unidades(unidades_disponibles)
        tipo_validado = self._validar_texto(tipo_equipo, "tipo de equipo")
        super().__init__(
            identificador,
            tipo_validado,
            tarifa_base,
            disponibilidad=unidades > 0,
        )
        self._tipo_equipo = tipo_validado
        self._unidades_disponibles = int(unidades)

    @staticmethod
    def _validar_unidades(unidades: int) -> int:
        if (
            isinstance(unidades, bool)
            or not isinstance(unidades, Integral)
            or unidades < 0
        ):
            raise ErrorParametroServicio(
                "Las unidades disponibles deben ser un entero no negativo."
            )
        return int(unidades)

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    @property
    def unidades_disponibles(self) -> int:
        return self._unidades_disponibles

    @property
    def disponibilidad(self) -> bool:
        return self.unidades_disponibles > 0

    def validar_parametros(self) -> None:
        super().validar_parametros()
        self._validar_unidades(self._unidades_disponibles)
        self._validar_texto(self._tipo_equipo, "tipo de equipo")

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
            f"Alquiler de {self.tipo_equipo} "
            f"(unidades disponibles: {self.unidades_disponibles}; "
            f"tarifa por unidad y duración: {self.tarifa_base:.2f})."
        )

    def to_dict(self) -> dict[str, object]:
        return {
            **super().to_dict(),
            "tipo_equipo": self.tipo_equipo,
            "unidades_disponibles": self.unidades_disponibles,
        }
